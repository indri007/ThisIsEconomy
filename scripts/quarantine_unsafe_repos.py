#!/usr/bin/env python3
import os
import shutil

SOURCE_DIR = "/Users/jevin/Documents/tesis_mbg/cloned_repos/free_tier_paas"
QUARANTINE_DIR = "/Users/jevin/Documents/tesis_mbg/cloned_repos/_quarantine_system_daemons"

UNSAFE_REPOS = [
    "1Panel",
    "coolify",
    "caprover",
    "lab-xyz-lab",
    "openclaw-webtop"
]

os.makedirs(QUARANTINE_DIR, exist_ok=True)
print(f"Quarantine target directory: {QUARANTINE_DIR}")
print("=" * 60)

moved = []
for name in UNSAFE_REPOS:
    src = os.path.join(SOURCE_DIR, name)
    dst = os.path.join(QUARANTINE_DIR, name)
    if os.path.exists(src):
        try:
            shutil.move(src, dst)
            print(f"[QUARANTINED] {name} -> {dst}")
            moved.append((name, "MOVED_TO_QUARANTINE", True))
        except Exception as e:
            print(f"[ERROR] Moving {name}: {e}")
            moved.append((name, f"ERROR: {e}", False))
    else:
        print(f"[NOT FOUND / ALREADY MOVED] {name}")
        moved.append((name, "NOT_FOUND", True))

print("=" * 60)
print(f"Total quarantined: {sum(1 for _, _, ok in moved if ok)}/{len(UNSAFE_REPOS)}")
