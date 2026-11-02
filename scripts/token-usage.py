"""Count the Claude Code tokens spent on this repository, per date, migration day, model and agent.

Reads the session transcripts Claude Code keeps on this machine (~/.claude/projects/<this
repository's path>, subagents included) and writes totals only, no prompt or reply text, to
docs/dashboard/token-usage.json (tokens and the --tools counts per row), which scripts/spec-drift.py puts on the dashboard. The
transcripts live on the maintainer's machine, not in CI, so this runs locally and its output is
committed; the closing PR of each day refreshes it.

    python scripts/token-usage.py
    python scripts/token-usage.py --simulate   # what shorter sessions or capped tool output would save
    python scripts/token-usage.py --tools      # Bash results cap-output cut; Reads of files over 8,000 bytes
    python scripts/token-usage.py --tools --since 2026-11-01   # only the sessions that started since then

A reply is counted once, from its last line: a transcript repeats a reply's usage on every content
block it streamed, and the usage is complete only on the last of those lines, so replies are keyed
by message and request id and the last line per key wins. The day is the branch the session was on
(day-17/track-d-... is Day 17); anything else (main, tooling/, docs/) has no day. Claude Code
deletes transcripts after cleanupPeriodDays (30 by default), so an entry already in the file is
never lowered: each count keeps the larger of the file's and the transcripts'.
"""
import argparse
import collections
import datetime
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, os.pardir, "docs", "dashboard", "token-usage.json"))
FIELDS = ("input", "cache_write", "cache_read", "output", "replies")
TOOL_FIELDS = ("bash", "cut", "reads", "whole")
DAY_BRANCH = re.compile(r"^day-(\d+)/")
DATED = re.compile(r"-\d{8}$")
CUTS = (100_000, 200_000, 300_000)
CAPS = (2_000, 5_000)
TOOL_LIMIT = 8_000  # read-guard.py's LIMIT: a whole Read of a file over it is refused
CUT_AT = 3_000  # cap-output.py's KEEP: its cut marker follows the head, this many characters in


def long_path(path):
    # Windows refuses a path past MAX_PATH (260 characters) unless it is absolute and starts with
    # \\?\: open() raises, and glob skips a folder past the limit without a word. glob keeps the
    # prefix on every path it yields, so prefixing the root reaches every open. UNC paths are left as they are.
    if os.name != "nt" or path.startswith("\\\\"):
        return path
    return "\\\\?\\" + os.path.abspath(path)


def transcripts(root):
    # Claude Code names a project's folder after its path, every character but letters and digits
    # turned into "-"; a worktree of this repository, under its .claude/worktrees/, gets the same name
    # and "--". A sibling folder whose name only starts with this one's is another project.
    name = re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(os.path.join(HERE, os.pardir))).lower()
    for folder in glob.glob(os.path.join(long_path(root), "*")):
        base = os.path.basename(folder).lower()
        if base == name or base.startswith(name + "--"):
            yield from glob.glob(os.path.join(folder, "**", "*.jsonl"), recursive=True)


def agent(path):
    # A subagent's transcript, subagents/agent-<id>.jsonl, has its type in agent-<id>.meta.json beside it.
    meta = path[:-len(".jsonl")] + ".meta.json"
    if os.path.basename(os.path.dirname(path)) != "subagents":
        return "main"
    try:
        with open(meta, encoding="utf-8") as f:
            return json.load(f).get("agentType") or "unknown"
    except (OSError, ValueError):
        return "unknown"


def reply(entry):
    # The assistant message a line counts as a reply: it has usage and comes from a Claude model.
    msg = entry.get("message") or {}
    if entry.get("type") != "assistant" or not msg.get("usage") or not DATED.sub("", msg.get("model") or "").startswith("claude"):
        return None
    return msg


def row_key(entry, who):
    # The row a reply or a tool call counts toward: its local date, the day of its branch, its model and its agent.
    when = datetime.datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
    day = DAY_BRANCH.match(entry.get("gitBranch") or "")
    return (when.astimezone().date().isoformat(), int(day.group(1)) if day else None, DATED.sub("", entry["message"].get("model") or ""), who)


def tool_blocks(entry, calls, cut):
    # A line's tool calls by tool_use id, and each Bash result's cut test. A message spread over several
    # lines repeats its blocks: the last line wins, so a call counts once. A Bash result is cut by
    # cap-output.py when its text has the marker at CUT_AT.
    content = (entry.get("message") or {}).get("content")
    if not isinstance(content, list):
        return
    for b in content:
        if not isinstance(b, dict):
            continue
        if b.get("type") == "tool_use":
            calls[b.get("id")] = (b.get("name"), b.get("input") or {}, entry)
        elif b.get("type") == "tool_result" and calls.get(b.get("tool_use_id"), (None,))[0] == "Bash":
            cut[b.get("tool_use_id")] = tool_text(b.get("content")).find("\n[cut ") == CUT_AT


def read_size(name, args):
    # What a tool call adds to reads and whole: (1, whole) for a Read of a file over TOOL_LIMIT, else (0, 0).
    # A transcript keeps no size, so the file's size on disk now is read.
    if name != "Read" or size(args.get("file_path") or "") <= TOOL_LIMIT:
        return 0, 0
    return 1, int(not any(args.get(k) is not None for k in ("offset", "limit", "pages")))


def count(files):
    # The usage is complete only on a reply's last line, so the last line per key overwrites the others.
    replies, totals = {}, collections.defaultdict(lambda: dict.fromkeys(FIELDS + TOOL_FIELDS, 0))
    for path in files:
        who = agent(path)
        calls, cut = {}, {}
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except ValueError:
                    continue
                tool_blocks(entry, calls, cut)
                msg = reply(entry)
                if msg is not None:
                    replies[(msg.get("id"), entry.get("requestId"))] = (who, entry)
        for tid, (name, args, entry) in calls.items():
            if reply(entry) is None:
                continue
            t = totals[row_key(entry, who)]
            if tid in cut:
                t["bash"] += 1
                t["cut"] += int(cut[tid])
            reads, whole = read_size(name, args)
            t["reads"] += reads
            t["whole"] += whole
    for who, entry in replies.values():
        usage = entry["message"]["usage"]
        t = totals[row_key(entry, who)]
        t["input"] += usage.get("input_tokens", 0)
        t["cache_write"] += usage.get("cache_creation_input_tokens", 0)
        t["cache_read"] += usage.get("cache_read_input_tokens", 0)
        t["output"] += usage.get("output_tokens", 0)
        t["replies"] += 1
    return totals


def contexts(path):
    # A session's replies in order: the context each read (every input token, cached or not), and
    # whether a tool result came in since the reply before. A sidechain line is a subagent's.
    replies, tool = {}, False
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            msg = entry.get("message") or {}
            if entry.get("isSidechain"):
                continue
            if entry.get("type") == "user" and isinstance(msg.get("content"), list):
                tool = tool or any(isinstance(b, dict) and b.get("type") == "tool_result" for b in msg["content"])
            elif entry.get("type") == "assistant" and msg.get("usage"):
                u = msg["usage"]
                key = (msg.get("id"), entry.get("requestId"))
                context = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
                replies[key] = (context, replies[key][1] if key in replies else tool)
                tool = False
    return list(replies.values())


def simulate(files):
    # Every reply re-reads the whole context, so what a block adds is read once by each later reply.
    # A context that falls by more than 30% was compacted: the session goes on as a new segment.
    # Cut: whenever the context passes the size, start again from the segment's first context.
    # Cap: a tool result that added more than the cap adds only the cap, to that reply and every later one.
    # Both are upper bounds: a fresh session re-reads what it needs, and a capped result may be read again.
    s = dict(read=0, replies=0, sessions=0, cut=dict.fromkeys(CUTS, 0), cap=dict.fromkeys(CAPS, 0))
    for path in files:
        segments = []
        for context, tool in contexts(path):
            if not segments or context < 0.7 * segments[-1][-1][0]:
                segments.append([])
            segments[-1].append((context, tool))
        s["sessions"] += bool(segments)
        for seg in segments:
            for i, (context, tool) in enumerate(seg):
                s["read"] += context
                s["replies"] += 1
                if tool and i:
                    for cap in CAPS:
                        s["cap"][cap] += max(0, context - seg[i - 1][0] - cap) * (len(seg) - i)
            for cut in CUTS:
                saved = 0
                for context, _ in seg:
                    if context - saved > cut:
                        saved = context - seg[0][0]
                    s["cut"][cut] += saved
    return s


def moment(text):
    # A date or a time for --since, read as local time when it has no zone.
    return datetime.datetime.fromisoformat(text).astimezone()


def started(path):
    # A transcript's first timestamp: when its session started, or a subagent's run began.
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                stamp = json.loads(line).get("timestamp")
            except (ValueError, AttributeError):
                continue
            if stamp:
                return datetime.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    return None


def after(path, since):
    # Whether the transcript started at or after --since; without --since, every transcript counts.
    if since is None:
        return True
    start = started(path)
    return start is not None and start >= since


def size(path):
    try:
        return os.path.getsize(path)
    except OSError:
        return 0


def tool_text(content):
    if isinstance(content, list):
        return "".join(b.get("text", "") for b in content if isinstance(b, dict))
    return content if isinstance(content, str) else ""


def tools(files, since=None):
    s = dict(bash=0, cut=0, reads=0, whole=0)
    for path in files:
        if not after(path, since):
            continue
        calls, cut = {}, {}
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except ValueError:
                    continue
                tool_blocks(entry, calls, cut)
        s["bash"] += len(cut)
        s["cut"] += sum(cut.values())
        for name, args, _ in calls.values():
            reads, whole = read_size(name, args)
            s["reads"] += reads
            s["whole"] += whole
    return s


def report_tools(s):
    print(f"Bash results: {s['bash']:,}, cut by cap-output: {s['cut']:,} ({s['cut'] / max(s['bash'], 1):.1%})")
    print(f"Reads of files over {TOOL_LIMIT:,} bytes: {s['reads']:,}, whole {s['whole']:,}, ranged {s['reads'] - s['whole']:,}")


def report(s):
    print(f"main sessions:{s['sessions']}, {s['replies']:,} replies, {s['read'] / 1e6:,.1f}M context tokens read")
    for cut, saved in s["cut"].items():
        print(f"  fresh session whenever the context passes {cut // 1000}k: -{saved / max(s['read'], 1):.1%}")
    for cap, saved in s["cap"].items():
        print(f"  each tool result capped at {cap // 1000}k tokens: -{saved / max(s['read'], 1):.1%}")
    print("  upper bounds: a fresh session re-reads what it needs; a capped result may be read again")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--transcripts", default=os.path.join(os.path.expanduser("~"), ".claude", "projects"))
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--simulate", action="store_true",
                    help="print what fresh sessions or capped tool results would have saved; write nothing")
    ap.add_argument("--tools", action="store_true",
                    help="print the Bash results cap-output cut and the Reads of a file over 8,000 bytes; write nothing")
    ap.add_argument("--since", type=moment, metavar="DATE",
                    help="with --simulate or --tools: count only the sessions started at or after this date or time")
    args = ap.parse_args()
    if args.since and not (args.simulate or args.tools):
        ap.error("--since needs --simulate or --tools: token-usage.json is never written for part of the transcripts")
    if args.tools:
        report_tools(tools(transcripts(args.transcripts), args.since))
        return
    if args.simulate:
        report(simulate(p for p in transcripts(args.transcripts) if agent(p) == "main" and after(p, args.since)))
        return
    totals = count(transcripts(args.transcripts))
    if os.path.exists(args.out):
        with open(args.out, encoding="utf-8") as f:
            kept = json.load(f)
        for r in (r for r in kept if "agent" in r):
            t = totals[(r["date"], r["day"], r["model"], r["agent"])]
            for k in FIELDS:
                t[k] = max(t[k], r[k])
            for k in TOOL_FIELDS:
                t[k] = max(t[k], r.get(k, 0))
        # A row written before agents were counted holds every agent's tokens: what it has beyond
        # the agents counted for its date, day and model is kept as unknown, not given to one of them.
        for r in (r for r in kept if "agent" not in r):
            counted = [t for key, t in totals.items() if key[:3] == (r["date"], r["day"], r["model"])]
            t = totals[(r["date"], r["day"], r["model"], "unknown")]
            for k in FIELDS:
                t[k] += max(0, r[k] - sum(c[k] for c in counted))
    rows = [dict(date=d, day=n, model=m, agent=a, **t) for (d, n, m, a), t in totals.items()]
    rows.sort(key=lambda r: (r["date"], r["day"] or 0, r["model"], r["agent"]))
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("[\n" + ",\n".join(json.dumps(r, separators=(",", ":")) for r in rows) + "\n]\n")
    out = sum(r["output"] for r in rows)
    print(f"{args.out}: {len(rows)} rows, {rows[0]['date']} to {rows[-1]['date']}, {out:,} output tokens")


if __name__ == "__main__":
    main()
