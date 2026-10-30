"""Validate frozen replay cases and tally a person's judgments; never run the auditor."""
import argparse
from collections import Counter
from datetime import date
import hashlib
import json
from pathlib import Path
import re

KINDS = ('historical-defect', 'broken-check', 'cross-day', 'clean')
SPLITS = ('development', 'held-out')
SEVERITIES = ('blocking', 'major', 'minor')


def need(ok, message):
    if not ok:
        raise ValueError(message)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def hexed(value, length):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-fA-F]{%d}' % length, value)


def key(data, clean):
    need(isinstance(data, list), 'key must be a list')
    ids = []
    for f in data:
        need(all(text(f[k]) for k in ('id', 'statement', 'full')), 'invalid finding text')
        need(f['severity'] in SEVERITIES, 'invalid severity')
        need(f['partial'] is None or text(f['partial']), 'invalid partial rubric')
        ids.append(f['id'])
    need(len(ids) == len(set(ids)), 'duplicate finding ID')
    need(bool(data) != clean, 'clean key must be empty; other keys must have findings')
    return data


def development(c, base):
    p = Path(c['key'])
    root = (base / 'keys').resolve()
    need(not p.is_absolute() and (base / p).resolve().is_relative_to(root), 'key must be under keys/')
    return key(json.loads((base / p).read_bytes()), c['kind'] == 'clean')


def manifest(path):
    m = json.loads(path.read_bytes())
    need(type(m['version']) is int and m['version'] == 1 and isinstance(m['cases'], list), 'invalid manifest format')
    errors, seen = [], set()
    for c in m['cases']:
        label = c.get('id', '?') if isinstance(c, dict) else '?'
        try:
            need(isinstance(c['id'], str) and re.fullmatch(r'[\w-]+', c['id'], re.ASCII), 'invalid case ID')
            need(c['id'] not in seen, 'duplicate case ID')
            seen.add(c['id'])
            need(c['kind'] in KINDS, 'invalid kind')
            need(c['split'] in SPLITS, 'invalid split')
            need(text(c['source']['repo']) and hexed(c['source']['commit'], 40), 'invalid source/commit')
            need(all(text(c[k]) for k in ('spec', 'task', 'origin')), 'missing spec/task/origin')
            need(not Path(c['spec']).is_absolute() and '..' not in Path(c['spec']).parts, 'invalid spec path')
            if c['verified'] is not None:
                need(text(c['verified']['by']), 'missing verifier')
                date.fromisoformat(c['verified']['date'])
            if c['split'] == 'development':
                development(c, path.parent)
            else:
                need(set(c['key']) == {'sha256'} and hexed(c['key']['sha256'], 64), 'held-out key requires only sha256')
        except (ValueError, KeyError, TypeError, AttributeError, OSError) as e:
            errors.append(f'{label}: {e}')
    return m['cases'], errors


def tally(c, row, base, private):
    need(c['verified'] is not None, 'unverified case')
    if c['split'] == 'held-out':
        need(private is not None, 'held-out scoring requires --keys')
        raw = (private / (c['id'] + '.json')).read_bytes()
        need(hashlib.sha256(raw).hexdigest() == c['key']['sha256'].lower(), 'key sha256 mismatch')
        findings = key(json.loads(raw), c['kind'] == 'clean')
    else:
        findings = development(c, base)
    judged = row['findings']
    need(set(judged) == {f['id'] for f in findings}, 'unknown or unjudged key finding')
    need(all(v in ('full', 'partial', 'missed') for v in judged.values()), 'invalid judgment')
    need(all(judged[f['id']] != 'partial' or f['partial'] is not None for f in findings), 'partial credit unavailable')
    counts = Counter(judged.values())
    counts['missed blocking'] = sum(f['severity'] == 'blocking' and judged[f['id']] == 'missed' for f in findings)
    for extra in row['extras']:
        need(extra['severity'] in SEVERITIES and text(extra['evidence']), 'extra requires severity and evidence')
        need(extra['judgment'] in ('false-alarm', 'valid-outside-key', 'duplicate'), 'invalid extra judgment')
        counts[extra['judgment']] += 1
    need(text(row['output']) and all(type(row[k]) in (int, float) and 0 <= row[k] < float('inf')
         for k in ('minutes', 'tokens', 'review_minutes')), 'invalid run record')
    return counts


def report(label, n):
    full, partial, missed = (n[k] for k in ('full', 'partial', 'missed'))
    expected, matched = full + partial + missed, full + partial
    ratio = lambda a, b: f'{a / b:.6f}' if b else 'n/a'
    print(f'{label}: full={full} partial={partial} missed={missed}')
    print(f'  strict recall={ratio(full, expected)} lenient recall={ratio(matched, expected)}')
    print(f'  missed blocking={n["missed blocking"]}')
    print(f'  false alarms={n["false-alarm"]} precision={ratio(matched, matched + n["false-alarm"])}')
    print(f'  valid-outside-key={n["valid-outside-key"]}')


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=('check', 'score'))
    p.add_argument('judgments', nargs='?', type=Path)
    p.add_argument('--manifest', type=Path, default=Path(__file__).with_name('manifest.json'))
    p.add_argument('--keys', type=Path)
    a = p.parse_args(argv)
    try:
        cases, errors = manifest(a.manifest)
        if a.command == 'check':
            print('\n'.join(errors + [f'{len(cases)} cases' + (' (no cases)' if not cases else '')]))
            print(' '.join(f'{k}={sum(c.get("split" if k in SPLITS else "kind") == k for c in cases if isinstance(c, dict))}'
                           for k in (*SPLITS, *KINDS)))
            print('unverified: ' + ', '.join(str(c.get('id', '?')) for c in cases if isinstance(c, dict) and not c.get('verified')))
            return int(bool(errors))
        need(not errors, '; '.join(errors))
        need(a.judgments is not None, 'score requires JUDGMENTS')
        run = json.loads(a.judgments.read_bytes())
        need(hexed(run['kit_commit'], 40) and hexed(run['auditor_sha256'], 64) and text(run['model']), 'invalid run metadata')
        rows, total = [], Counter()
        need(isinstance(run['cases'], dict), 'run cases must be an object')
        for cid, row in run['cases'].items():
            need(cid in {c['id'] for c in cases}, f'{cid}: unknown case')
            try:
                counts = tally(next(c for c in cases if c['id'] == cid), row, a.manifest.parent, a.keys)
            except (ValueError, KeyError, TypeError, OSError) as e:
                raise ValueError(f'{cid}: {e}') from e
            rows.append((cid, counts))
            total.update(counts)
        for cid, counts in rows:
            report(cid, counts)
        report('total', total)
        return 0
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as e:
        print(f'refused: {e}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
