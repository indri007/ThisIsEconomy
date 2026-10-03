#!/usr/bin/env python3
import os
import subprocess
import sys

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

TARGET_DIR = "/Users/jevin/Documents/tesis_mbg/cloned_repos"

def main():
    os.makedirs(TARGET_DIR, exist_ok=True)
    print(f"Target directory: {TARGET_DIR}")
    print("=" * 60)
    
    results = []
    for idx, (name, url) in enumerate(REPOS, 1):
        dest = os.path.join(TARGET_DIR, name)
        print(f"[{idx}/{len(REPOS)}] Cloning {name}...")
        if os.path.exists(dest):
            print(f"    -> Destination '{dest}' already exists. Skipping.")
            results.append((name, "SKIPPED (Already exists)"))
            continue
        
        cmd = ["git", "clone", "--depth", "1", url, dest]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"    -> Successfully cloned {name}.")
            results.append((name, "SUCCESS"))
        except subprocess.CalledProcessError as e:
            print(f"    -> ERROR cloning {name}: {e.stderr.strip()}")
            results.append((name, f"FAILED: {e.stderr.strip()[:100]}"))
    
    print("=" * 60)
    print("Summary:")
    for name, status in results:
        print(f" - {name:<40}: {status}")

if __name__ == "__main__":
    main()
