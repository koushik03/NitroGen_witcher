import tarfile
import json
import io
import os
import shutil
from huggingface_hub import hf_hub_download, HfApi

# Configuration
DATA_DIR = "../data/witcher_3"
GAMES_LIST_FILE = "../data/games.txt"
os.makedirs(DATA_DIR, exist_ok=True)

def get_free_space_gb():
    # Returns free space on the current drive in GB
    total, used, free = shutil.disk_usage("/")
    return free // (2**30)

def collect_data():
    api = HfApi()
    repo_id = "nvidia/NitroGen"
    
    print("Connecting to NitroGen...")
    all_files = api.list_repo_files(repo_id=repo_id, repo_type="dataset")
    shards = sorted([f for f in all_files if f.startswith("actions/SHARD_") and f.endswith(".tar.gz")])
    
    unique_games = set()

    for shard_path in shards:
        # 1. DISK PROTECTION: Check space before downloading
        free_gb = get_free_space_gb()
        if free_gb < 20:
            print(f"🛑 CRITICAL: Only {free_gb}GB left! Stopping to prevent disk crash.")
            break

        print(f"\n📦 Processing: {shard_path} (Free Space: {free_gb}GB)")
        
        try:
            # 2. Download Shard
            local_path = hf_hub_download(repo_id=repo_id, filename=shard_path, repo_type="dataset")
            
            with tarfile.open(local_path, "r:gz") as tar:
                for member in [m for m in tar.getmembers() if "metadata.json" in m.name]:
                    f = tar.extractfile(member)
                    if f:
                        content = json.load(io.TextIOWrapper(f))
                        game_raw = content.get("game", "unknown")
                        unique_games.add(game_raw)
                        
                        # SNAKE_CASE SEARCH
                        if "witcher" in game_raw.lower():
                            print(f"✅ Found Witcher clip in {shard_path}")
                            tar.extract(member, path=DATA_DIR)
                            # Get the matching parquet
                            p_name = member.name.replace("metadata.json", "actions_processed.parquet")
                            try: tar.extract(p_name, path=DATA_DIR)
                            except: pass

            # Update game list
            with open(GAMES_LIST_FILE, "w") as f_list:
                for g in sorted(list(unique_games)): f_list.write(f"{g}\n")

            # 3. FORCE CLEANUP: Delete the shard and the cache folder
            if os.path.exists(local_path):
                os.remove(local_path)
            
            # This clears the "lock" and metadata files HF leaves behind
            cache_dir = os.path.dirname(local_path)
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)

        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    collect_data()