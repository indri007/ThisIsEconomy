#!/usr/bin/env python3
import os
import subprocess
import glob

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLONED_REPOS = os.path.join(PROJECT_ROOT, "cloned_repos")
FREE_TIER = os.path.join(CLONED_REPOS, "free_tier_paas")

ALL_REPOS = [
    (os.path.join(CLONED_REPOS, "MiroFish"), "MiroFish"),
    (os.path.join(CLONED_REPOS, "oasis"), "oasis"),
    (os.path.join(CLONED_REPOS, "graphiti"), "graphiti"),
    (os.path.join(CLONED_REPOS, "zep"), "zep"),
    (os.path.join(CLONED_REPOS, "graphiti-zep-agent"), "graphiti-zep-agent"),
    (os.path.join(CLONED_REPOS, "tweetnlp"), "tweetnlp"),
    (os.path.join(CLONED_REPOS, "tweet-engagement-prediction"), "tweet-engagement-prediction"),
    (os.path.join(CLONED_REPOS, "Tweet-Popularity-Prediction"), "Tweet-Popularity-Prediction"),
    (os.path.join(CLONED_REPOS, "Awesome-DL-Information-Cascades-Modeling"), "Awesome-DL-Information-Cascades-Modeling"),
    (os.path.join(CLONED_REPOS, "Information-Diffusion-Datasets"), "Information-Diffusion-Datasets"),
    (os.path.join(FREE_TIER, "1Panel"), "1Panel"),
    (os.path.join(FREE_TIER, "Awesome-Free-Developer-Services"), "Awesome-Free-Developer-Services"),
    (os.path.join(FREE_TIER, "Awesome-Web-Hosting-2026-iSoumyaDey"), "Awesome-Web-Hosting-2026-iSoumyaDey"),
    (os.path.join(FREE_TIER, "Awesome-Web-Hosting-nuhmanpk"), "Awesome-Web-Hosting-nuhmanpk"),
    (os.path.join(FREE_TIER, "awesome-cloud-services"), "awesome-cloud-services"),
    (os.path.join(FREE_TIER, "awesome-hosting"), "awesome-hosting"),
    (os.path.join(FREE_TIER, "awesome-oracle-cloud-free-tier"), "awesome-oracle-cloud-free-tier"),
    (os.path.join(FREE_TIER, "awesome-selfhosted"), "awesome-selfhosted"),
    (os.path.join(FREE_TIER, "awesome-selfhosted-timokoessler"), "awesome-selfhosted-timokoessler"),
    (os.path.join(FREE_TIER, "caprover"), "caprover"),
    (os.path.join(FREE_TIER, "coolify"), "coolify"),
    (os.path.join(FREE_TIER, "dokploy"), "dokploy"),
    (os.path.join(FREE_TIER, "free-for-dev"), "free-for-dev"),
    (os.path.join(FREE_TIER, "free-tier-hub"), "free-tier-hub"),
    (os.path.join(FREE_TIER, "helmsman"), "helmsman"),
    (os.path.join(FREE_TIER, "lab-xyz-lab"), "lab-xyz-lab"),
    (os.path.join(FREE_TIER, "openclaw-webtop"), "openclaw-webtop"),
]

def check_single_repo(path, name):
    if not os.path.exists(path):
        return {"name": name, "status": "FAIL", "reason": "Directory missing"}
    
    # 1. Git fsck check
    fsck = subprocess.run(["git", "-C", path, "fsck", "--no-dangling"], capture_output=True, text=True)
    fsck_ok = (fsck.returncode == 0)
    
    # 2. Check for private key leaks (id_rsa, *.pem without cert, etc.)
    suspicious_files = []
    for root, dirs, files in os.walk(path):
        if ".git" in root:
            continue
        for f in files:
            fl = f.lower()
            if fl in ["id_rsa", "id_ed25519", "id_ecdsa", ".env"]:
                # If .env exists, check if it's not just an example
                full_p = os.path.join(root, f)
                try:
                    with open(full_p, 'r', errors='ignore') as ef:
                        content = ef.read(500)
                        if "api_key" in content.lower() and not "your_" in content.lower() and not "example" in content.lower():
                            suspicious_files.append(f"Leaked secret potential: {f}")
                except Exception:
                    pass
            elif fl.endswith(".exe") or fl.endswith(".bat") or fl.endswith(".dll"):
                suspicious_files.append(f"Windows binary: {f}")

    # 3. Clean worktree check
    status = subprocess.run(["git", "-C", path, "status", "--porcelain"], capture_output=True, text=True)
    is_clean = (len(status.stdout.strip()) == 0)
    
    safe = fsck_ok and (len(suspicious_files) == 0)
    return {
        "name": name,
        "fsck_ok": fsck_ok,
        "is_clean": is_clean,
        "suspicious": suspicious_files,
        "safe": safe
    }

results = []
for p, n in ALL_REPOS:
    res = check_single_repo(p, n)
    results.append(res)

print(f"{'No':<3} | {'Repo':<36} | {'Git fsck':<8} | {'Clean Tree':<10} | {'Threats':<8} | {'Status'}")
print("-" * 80)
for idx, r in enumerate(results, 1):
    fsck_str = "PASS" if r["fsck_ok"] else "FAIL"
    clean_str = "CLEAN" if r["is_clean"] else "DIRTY"
    threat_str = "0 THREAT" if len(r["suspicious"]) == 0 else f"{len(r['suspicious'])} WARN"
    status_str = "AMAN (1)" if r["safe"] else "PERLU CEK (0)"
    print(f"{idx:02d}  | {r['name']:<36} | {fsck_str:<8} | {clean_str:<10} | {threat_str:<8} | {status_str}")
