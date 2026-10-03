#!/usr/bin/env python3
import os
import subprocess
import sys

REPOS = [
    ("free-for-dev", "https://github.com/ripienaar/free-for-dev.git"),
    ("free-tier-hub", "https://github.com/ePlus-DEV/free-tier-hub.git"),
    ("Awesome-Web-Hosting-2026-p32929", "https://github.com/p32929/Awesome-Web-Hosting-2026.git"),
    ("Awesome-Web-Hosting-2026-iSoumyaDey", "https://github.com/iSoumyaDey/Awesome-Web-Hosting-2026.git"),
    ("Awesome-Free-Developer-Services", "https://github.com/kebbbnnn/Awesome-Free-Developer-Services.git"),
    ("awesome-oracle-cloud-free-tier", "https://github.com/neitsab/awesome-oracle-cloud-free-tier.git"),
    ("awesome-hosting", "https://github.com/dalisoft/awesome-hosting.git"),
    ("awesome-cloud-services", "https://github.com/harsxv/awesome-cloud-services.git"),
    ("lab-xyz-lab", "https://github.com/lab-xyz/lab.git"),
    ("coolify", "https://github.com/coollabsio/coolify.git"),
    ("dokploy", "https://github.com/Dokploy/dokploy.git"),
    ("caprover", "https://github.com/caprover/caprover.git"),
    ("1Panel", "https://github.com/1Panel-dev/1Panel.git"),
    ("helmsman", "https://github.com/daboss2003/helmsman.git"),
    ("awesome-selfhosted", "https://github.com/awesome-selfhosted/awesome-selfhosted.git"),
    ("awesome-selfhosted-timokoessler", "https://github.com/timokoessler/awesome-selfhosted.git"),
    ("openclaw-webtop", "https://github.com/gitricko/openclaw-webtop.git"),
]

TARGET_DIR = "/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas"

def main():
    os.makedirs(TARGET_DIR, exist_ok=True)
    print(f"Target directory: {TARGET_DIR}")
    print("=" * 60)
    
    results = []
    for idx, (name, url) in enumerate(REPOS, 1):
        dest = os.path.join(TARGET_DIR, name)
        print(f"[{idx:02d}/{len(REPOS)}] Cloning {name}...")
        if os.path.exists(dest):
            print(f"    -> Destination '{dest}' already exists. Skipping.")
            results.append((name, "SKIPPED (Already exists)", True))
            continue
        
        cmd = ["git", "clone", "--depth", "1", url, dest]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"    -> Successfully cloned {name}.")
            results.append((name, "SUCCESS", True))
        except subprocess.CalledProcessError as e:
            err = e.stderr.strip()
            print(f"    -> ERROR cloning {name}: {err[:120]}")
            results.append((name, f"FAILED: {err[:80]}", False))
            
    print("=" * 60)
    print("Summary:")
    for name, status, ok in results:
        print(f" - {name:<35}: {status}")

if __name__ == "__main__":
    main()
