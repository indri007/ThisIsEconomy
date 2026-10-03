#!/usr/bin/env python3
import os
import subprocess
import glob

ALL_REPOS = [
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/MiroFish", "MiroFish"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/oasis", "oasis"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/graphiti", "graphiti"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/zep", "zep"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/graphiti-zep-agent", "graphiti-zep-agent"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/tweetnlp", "tweetnlp"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/tweet-engagement-prediction", "tweet-engagement-prediction"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/Tweet-Popularity-Prediction", "Tweet-Popularity-Prediction"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/Awesome-DL-Information-Cascades-Modeling", "Awesome-DL-Information-Cascades-Modeling"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/Information-Diffusion-Datasets", "Information-Diffusion-Datasets"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/1Panel", "1Panel"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/Awesome-Free-Developer-Services", "Awesome-Free-Developer-Services"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/Awesome-Web-Hosting-2026-iSoumyaDey", "Awesome-Web-Hosting-2026-iSoumyaDey"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/Awesome-Web-Hosting-nuhmanpk", "Awesome-Web-Hosting-nuhmanpk"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/awesome-cloud-services", "awesome-cloud-services"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/awesome-hosting", "awesome-hosting"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/awesome-oracle-cloud-free-tier", "awesome-oracle-cloud-free-tier"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/awesome-selfhosted", "awesome-selfhosted"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/awesome-selfhosted-timokoessler", "awesome-selfhosted-timokoessler"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/caprover", "caprover"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/coolify", "coolify"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/dokploy", "dokploy"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/free-for-dev", "free-for-dev"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/free-tier-hub", "free-tier-hub"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/helmsman", "helmsman"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/lab-xyz-lab", "lab-xyz-lab"),
    ("/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas/openclaw-webtop", "openclaw-webtop"),
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
