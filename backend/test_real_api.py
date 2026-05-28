import requests, json, time

BASE = "http://127.0.0.1:8000"

# Step 1: Upload script
print("=" * 60)
print("STEP 1: Upload script")
print("=" * 60)
with open("data/uploads/test_script.txt", "rb") as f:
    resp = requests.post(f"{BASE}/api/v1/upload/script",
        files={"file": ("test_script.txt", f, "text/plain")})
print(f"Status: {resp.status_code}")
data = resp.json()
print(json.dumps(data, indent=2, ensure_ascii=False))
script_id = data["id"]

# Step 2: Trigger analysis
print()
print("=" * 60)
print("STEP 2: Trigger analysis")
print("=" * 60)
resp = requests.post(f"{BASE}/api/v1/analysis/{script_id}/analyze")
print(f"Status: {resp.status_code}")
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))

# Step 3: Poll for results
print()
print("=" * 60)
print("STEP 3: Poll analysis results (calling MiMo API...)")
print("=" * 60)
for attempt in range(10):
    time.sleep(3)
    resp = requests.get(f"{BASE}/api/v1/analysis/{script_id}")
    data = resp.json()
    analyzed = data.get("is_analyzed")
    roles_count = len(data.get("roles", []))
    print(f"Attempt {attempt+1}: is_analyzed={analyzed}, roles={roles_count}")
    if analyzed:
        print()
        print("ROLES:")
        for r in data["roles"]:
            print(f"  - {r['name']} ({r['gender']}, age={r['age']}, voice={r['voice_type']})")
            print(f"    personality: {r['personality']}")
        print()
        print("LINES (first 10):")
        for l in data["lines"][:10]:
            tag = l.get("emotion_tag", "-")
            print(f"  #{l['line_number']} [{tag}] {l['content']}")
        break
    if attempt == 5 and not analyzed:
        total_lines = data.get("total_lines", 0)
        print(f"  (total_lines={total_lines}, waiting for MiMo API...)")
else:
    print()
    resp = requests.get(f"{BASE}/api/v1/analysis/{script_id}")
    print("Final state:", json.dumps(resp.json(), indent=2, ensure_ascii=False))
    print("TIMEOUT: Analysis did not complete within 30s")

# Step 4: Config status
print()
print("=" * 60)
print("STEP 4: Config status")
print("=" * 60)
resp = requests.get(f"{BASE}/api/v1/config/status")
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))

print()
print("=" * 60)
print("ALL TESTS COMPLETE")
print("=" * 60)
