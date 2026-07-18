import json

with open('/opt/data/lott-lab/ledger.json') as f:
    lottlab = json.load(f)

with open('/opt/data/projects/lott-lab/ledger.json') as f:
    projects = json.load(f)

print("=== LOTT-LAB (has results) ===")
for r in lottlab['rounds']:
    print(f"  Round {r['round_id']}: status={r['status']}, results={len(r['results'])} draws, tickets={len(r['tickets'])}")

print("\n=== PROJECTS (current actual) ===")
for r in projects['rounds']:
    print(f"  Round {r['round_id']}: status={r['status']}, results={len(r['results'])} draws, tickets={len(r['tickets'])}")

lottlab_rounds = {r['round_id']: r for r in lottlab['rounds']}

merged_rounds = []
for pr in projects['rounds']:
    rid = pr['round_id']
    if rid in lottlab_rounds:
        lr = lottlab_rounds[rid]
        if len(lr.get('results', [])) > len(pr.get('results', [])):
            print(f"\n  Using lottlab version for {rid} ({len(lr['results'])} results vs {len(pr.get('results',[]))})")
            merged_rounds.append(lr)
        else:
            merged_rounds.append(pr)
    else:
        merged_rounds.append(pr)

projects_ids = {r['round_id'] for r in projects['rounds']}
for rid, lr in lottlab_rounds.items():
    if rid not in projects_ids:
        print(f"\n  Adding missing round {rid} from lottlab")
        merged_rounds.append(lr)

merged_rounds.sort(key=lambda r: r['date'])

merged = {
    'created_at': projects['created_at'],
    'rounds': merged_rounds,
    'settings': projects.get('settings', lottlab.get('settings', {})),
    'version': max(projects.get('version', 1), lottlab.get('version', 1))
}

print(f"\n=== MERGED ===")
for r in merged['rounds']:
    print(f"  Round {r['round_id']}: status={r['status']}, results={len(r['results'])} draws, tickets={len(r['tickets'])}")

with open('/opt/data/projects/lott-lab/ledger.json', 'w') as f:
    json.dump(merged, f, indent=2)

print(f"\nWritten ({len(json.dumps(merged))} bytes)")
