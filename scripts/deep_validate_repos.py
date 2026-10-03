#!/usr/bin/env python3
import os
import subprocess

REPOS = [
    ("MiroFish", "https://github.com/666ghj/MiroFish.git"),
    ("oasis", "https://github.com/camel-ai/oasis.git"),
    ("graphiti", "https://github.com/getzep/graphiti.git"),
    ("zep", "https://github.com/getzep/zep.git"),
    ("graphiti-zep-agent", "https://github.com/shivanshinigam/graphiti-zep-agent.git"),
    ("tweetnlp", "https://github.com/cardiffnlp/tweetnlp.git"),
    ("tweet-engagement-prediction", "https://github.com/felixpeters/tweet-engagement-prediction.git"),
    ("Tweet-Popularity-Prediction", "https://github.com/sagarjinde/Tweet-Popularity-Prediction.git"),
    ("Awesome-DL-Information-Cascades-Modeling", "https://github.com/ChenNed/Awesome-DL-Information-Cascades-Modeling.git"),
    ("Information-Diffusion-Datasets", "https://github.com/fuxiaG/Information-Diffusion-Datasets.git"),
]

BASE = "/Users/jevin/Documents/tesis_mbg/cloned_repos"

for idx, (name, url) in enumerate(REPOS, 1):
    path = os.path.join(BASE, name)
    exists = os.path.exists(path)
    git_dir = os.path.join(path, ".git")
    has_git = os.path.exists(git_dir)
    file_count = 0
    total_size = 0
    head_commit = "N/A"
    
    if exists:
        for root, dirs, files in os.walk(path):
            if ".git" in root:
                continue
            file_count += len(files)
            for f in files:
                try:
                    total_size += os.path.getsize(os.path.join(root, f))
                except Exception:
                    pass
                    
        # Git commit check
        try:
            res = subprocess.run(["git", "-C", path, "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
            if res.returncode == 0:
                head_commit = res.stdout.strip()
        except Exception:
            pass
            
    print(f"[{idx:02d}] {name} | Exists: {exists} | Git: {has_git} | Commit: {head_commit} | Files: {file_count} | Size: {total_size/1024:.1f} KB")
