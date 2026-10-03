#!/usr/bin/env python3
import os
import subprocess

BASE = "/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas"
dirs = sorted(os.listdir(BASE))

for idx, d in enumerate(dirs, 1):
    path = os.path.join(BASE, d)
    if not os.path.isdir(path):
        continue
    has_git = os.path.exists(os.path.join(path, ".git"))
    file_count = 0
    total_size = 0
    head_commit = "N/A"
    
    for root, subdirs, files in os.walk(path):
        if ".git" in root:
            continue
        file_count += len(files)
        for f in files:
            try:
                total_size += os.path.getsize(os.path.join(root, f))
            except Exception:
                pass
                
    try:
        res = subprocess.run(["git", "-C", path, "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
        if res.returncode == 0:
            head_commit = res.stdout.strip()
    except Exception:
        pass
        
    print(f"[{idx:02d}] {d:<35} | Git: {has_git} | Commit: {head_commit} | Files: {file_count:>5} | Size: {total_size/1024:>9.1f} KB")
