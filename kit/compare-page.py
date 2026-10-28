"""The 53-box comparison: jobmatch's data drawn by this repository's page, box by box.

kit/page/jobmatch-data.json is the data jobmatch's published page embeds, the value of its
`window.SPEC_DRIFT = ...;` line byte for byte, fetched once from
https://yusuprozimemet.github.io/jobmatch-microservices/ on 2026-10-28. kit/page/jobmatch-boxes.sha256
is what docs/dashboard/dashboard.js drew from it then: the error that stopped the page and what
went to console.error, then the sha256 of each box's HTML, SVG included, as `<sha256>  <box>`, one
box a line. (A box name beside its hash, `"token-bars": "<hash>"`, reads to a secret scanner as a
token given a value.)
The page is run in node on test_spec_drift.py's DRAW document, as the earlier PRs ran it by hand.

    python kit/compare-page.py          # names each box that differs from the saved run; exit 1 if any
    python kit/compare-page.py --write  # saves the boxes as drawn now as the saved run

A PR that means to change boxes runs it, lists the boxes it names, and commits the saved run
rewritten with --write: the diff of jobmatch-boxes.sha256 is one line per changed box.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DATA = os.path.join(HERE, "page", "jobmatch-data.json")
BOXES = os.path.join(HERE, "page", "jobmatch-boxes.sha256")

# The fields that moved from the page's constants into the data (CHANGES.md, Batches 1 and 2), as
# spec-drift.py now writes them for jobmatch at its source commit: phases and stops from its plan.md
# (its "### Phase N — <name>" headings, and the one day its list marks **Stop and evaluate.**).
LATER = dict(project="jobmatch-microservices",
             phases=["Make the split safe", "Modularise in place (no network yet)", "Gateway + JWT",
                     "Extract job-service", "Extract matching-service", "Extract application-service + events",
                     "Functions + uploads bucket", "ECS on Fargate"],
             stops=[28], break_line_from_pr=310)


def draw_js():
    spec = importlib.util.spec_from_file_location("test_spec_drift", os.path.join(ROOT, "scripts", "test_spec_drift.py"))
    tsd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tsd)
    return tsd.DRAW


def drawn():
    """Each box's sha256, and the error and console.error lines, as the page draws them now."""
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)
    data["meta"].update(LATER)
    out = json.loads(subprocess.run(["node", "-e", draw_js(), os.path.join(ROOT, "docs", "dashboard", "dashboard.js")],
                                    input=json.dumps(data), capture_output=True, encoding="utf-8", check=True).stdout)
    boxes = {k: hashlib.sha256(v.encode("utf-8")).hexdigest() for k, v in sorted(out["panels"].items())}
    return dict(error=out["error"], logged=out["logged"], boxes=boxes)


def write(now):
    with open(BOXES, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"error {json.dumps(now['error'])}\nlogged {json.dumps(now['logged'])}\n")
        f.writelines(f"{v}  {k}\n" for k, v in now["boxes"].items())


def read():
    """The saved run, in drawn()'s shape."""
    with open(BOXES, encoding="utf-8") as f:
        lines = f.read().splitlines()
    saved = {k: json.loads(v) for k, v in (line.split(" ", 1) for line in lines[:2])}
    saved["boxes"] = {k: v for v, k in (line.split("  ", 1) for line in lines[2:])}
    return saved


def differs(saved, now):
    """The boxes that differ, each with how: changed, new or gone; then error and logged, if they differ."""
    out = [(k, "changed" if k in saved["boxes"] else "new") for k in now["boxes"]
           if saved["boxes"].get(k) != now["boxes"][k]]
    out += [(k, "gone") for k in saved["boxes"] if k not in now["boxes"]]
    out += [(k, f"{saved[k]!r} -> {now[k]!r}") for k in ("error", "logged") if saved[k] != now[k]]
    return out


def main():
    now = drawn()
    if sys.argv[1:] == ["--write"]:
        write(now)
        print(f"saved {len(now['boxes'])} boxes to {os.path.relpath(BOXES, ROOT)}")
        return 0
    saved = read()
    diff = differs(saved, now)
    same = sum(saved["boxes"].get(k) == v for k, v in now["boxes"].items())
    print(f"{same} of {len(now['boxes'])} boxes the same; {len(diff)} differ"
          + "".join(f"{', ' if i else ': '}{box} ({how})" for i, (box, how) in enumerate(diff)))
    return 1 if diff else 0


if __name__ == "__main__":
    sys.exit(main())
