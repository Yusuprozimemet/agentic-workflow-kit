"""Replay the day closed, or the short spec landed, by a push, or an explicitly requested day on main;
with --all, every closed day on main, into the report the dashboard reads."""
import argparse
import subprocess
import sys
from pathlib import Path

from evidence import close_commit, closed_specs, closing_spec

EVIDENCE = str(Path(__file__).with_name("evidence.py"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", default="HEAD")
    parser.add_argument("--day", default="", help="optional day number to replay on main")
    parser.add_argument("--all", metavar="PATH", help="replay every closed day on main into this report")
    parser.add_argument("--cache", metavar="PATH", help="with --all: evidence.py's --cache, so a day replays "
                        "again only when something it reads has changed")
    args = parser.parse_args()
    if args.all:
        specs = closed_specs("main")
        if not specs:
            print("no closed day on main")
            return 0
        cache = ["--cache", args.cache] if args.cache else []
        return subprocess.call([sys.executable, EVIDENCE, *specs, "--ref", "main", "--json", args.all, *cache])
    try:
        commit = args.commit
        if args.day:
            if not args.day.isascii() or not args.day.isdecimal() or not 0 <= int(args.day) <= 99:
                raise ValueError("day must be a number from 0 to 99")
            day = f"{int(args.day):02d}"
            commit = close_commit(day, "main")
            if not commit:
                raise ValueError(f"day-{day}: no closing commit on main")
        spec = closing_spec(commit)
    except ValueError as error:
        print(f"FAIL  {error}")
        return 1
    if spec is None:
        print("not a closing commit")
        return 0
    return subprocess.call([sys.executable, EVIDENCE, spec, "--ref", "main", "--json", "evidence.json"])


if __name__ == "__main__":
    sys.exit(main())
