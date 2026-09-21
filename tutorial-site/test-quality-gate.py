import json
import subprocess
import tempfile
import os

with open("tutorial-site/assets/skills-data.json", "r", encoding="utf-8") as f:
    skills = json.load(f)

print(f"Testing {len(skills)} Mermaid diagrams with mmdc CLI...")

failures = []
for i, s in enumerate(skills):
    code = s.get("mermaid", "")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False, encoding="utf-8") as tmp:
        tmp.write(code)
        tmp_name = tmp.name

    out_svg = tmp_name + ".svg"
    res = subprocess.run(["mmdc", "-i", tmp_name, "-o", out_svg], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if os.path.exists(tmp_name): os.remove(tmp_name)
    if os.path.exists(out_svg): os.remove(out_svg)

    if res.returncode != 0:
        err_msg = res.stderr.decode("utf-8", errors="replace").strip()
        first_err = err_msg.split("\n")[0] if err_msg else "Unknown error"
        failures.append((s["id"], first_err, code))
        print(f"FAILED: [{s['id']}]: {first_err}")
    else:
        # print progress dot every 20
        if (i + 1) % 30 == 0:
            print(f"  Passed {i + 1}/{len(skills)}...")

print(f"\n--- Quality Gate Summary ---")
print(f"Total: {len(skills)}")
print(f"Pass: {len(skills) - len(failures)}")
print(f"Failures: {len(failures)}")

if failures:
    with open("tutorial-site/mermaid_failures.json", "w", encoding="utf-8") as f:
        json.dump([{"id": f[0], "error": f[1], "code": f[2]} for f in failures], f, indent=2, ensure_ascii=False)
    print("Saved failures to tutorial-site/mermaid_failures.json")
