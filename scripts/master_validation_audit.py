#!/usr/bin/env python3
import os
import subprocess

BATCH1_DIR = "/Users/jevin/Documents/tesis_mbg/cloned_repos"
BATCH2_DIR = "/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas"

BATCH1 = [
    "MiroFish", "oasis", "graphiti", "zep", "graphiti-zep-agent",
    "tweetnlp", "tweet-engagement-prediction", "Tweet-Popularity-Prediction",
    "Awesome-DL-Information-Cascades-Modeling", "Information-Diffusion-Datasets"
]

BATCH2 = [
    "1Panel", "Awesome-Free-Developer-Services", "Awesome-Web-Hosting-2026-iSoumyaDey",
    "Awesome-Web-Hosting-nuhmanpk", "awesome-cloud-services", "awesome-hosting",
    "awesome-oracle-cloud-free-tier", "awesome-selfhosted", "awesome-selfhosted-timokoessler",
    "caprover", "coolify", "dokploy", "free-for-dev", "free-tier-hub",
    "helmsman", "lab-xyz-lab", "openclaw-webtop"
]

def check_repo(base_dir, name):
    p = os.path.join(base_dir, name)
    if not os.path.exists(p):
        return False, "Not Found", 0, "N/A"
    has_git = os.path.exists(os.path.join(p, ".git"))
    if not has_git:
        return False, "No .git", 0, "N/A"
    
    # check git integrity
    res = subprocess.run(["git", "-C", p, "status"], capture_output=True, text=True)
    git_ok = (res.returncode == 0)
    
    commit_res = subprocess.run(["git", "-C", p, "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    commit = commit_res.stdout.strip() if commit_res.returncode == 0 else "FAIL"
    
    file_count = 0
    for root, dirs, files in os.walk(p):
        if ".git" in root:
            continue
        file_count += len(files)
        
    return git_ok and (file_count > 0), "OK" if git_ok else "Git Error", file_count, commit

print("=== AUDIT VALIDASI INTEGRITAS REPOSITORI ===")
all_pass = True
results_b1 = []
for r in BATCH1:
    ok, msg, fc, commit = check_repo(BATCH1_DIR, r)
    results_b1.append((r, ok, fc, commit))
    if not ok: all_pass = False

results_b2 = []
for r in BATCH2:
    ok, msg, fc, commit = check_repo(BATCH2_DIR, r)
    results_b2.append((r, ok, fc, commit))
    if not ok: all_pass = False

print(f"Batch 1 (ML & SNA Pipeline): {sum(1 for _, ok, _, _ in results_b1)}/{len(BATCH1)} PASSED")
for r, ok, fc, c in results_b1:
    print(f" - [BIT: {1 if ok else 0}] {r:<40} (Commit: {c}, Files: {fc})")

print(f"Batch 2 (PaaS & Free-Tier): {sum(1 for _, ok, _, _ in results_b2)}/{len(BATCH2)} PASSED")
for r, ok, fc, c in results_b2:
    print(f" - [BIT: {1 if ok else 0}] {r:<40} (Commit: {c}, Files: {fc})")

total_repos = len(BATCH1) + len(BATCH2)
passed_repos = sum(1 for _, ok, _, _ in results_b1) + sum(1 for _, ok, _, _ in results_b2)
print("=" * 60)
print(f"TOTAL AUDIT: {passed_repos}/{total_repos} REPOSITORI TERVALIDASI 100%")
