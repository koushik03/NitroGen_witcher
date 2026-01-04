import tarfile
import os
import shutil
from pathlib import Path
from huggingface_hub import hf_hub_download

# Configuration - Absolute paths are safer
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "witcher_3"
REPO_ID = "nvidia/NitroGen"

def recover_parquets():
    if not DATA_DIR.exists():
        print(f"❌ DATA_DIR not found at: {DATA_DIR}")
        return

    # Look for SHARD folders directly in witcher_3
    shard_dirs = [d for d in os.listdir(DATA_DIR) if d.startswith("SHARD_")]
    
    print(f"🔍 Found {len(shard_dirs)} shards to revisit.")

    for shard_id in shard_dirs:
        # NitroGen stores shards in an 'actions/' prefix in the repo
        shard_repo_path = f"actions/{shard_id}.tar.gz"
        print(f"\n🔄 Opening {shard_repo_path}...")
        
        try:
            local_path = hf_hub_download(repo_id=REPO_ID, filename=shard_repo_path, repo_type="dataset")
            
            with tarfile.open(local_path, "r:gz") as tar:
                all_members = tar.getmembers()
                
                # Get the video IDs we already have folders for
                video_ids = [d for d in os.listdir(DATA_DIR / shard_id) if d.startswith('v')]
                
                for vid in video_ids:
                    # Find ANY parquet related to this video (raw or processed)
                    matches = [m for m in all_members if vid in m.name and m.name.endswith(".parquet")]
                    
                    for m in matches:
                        print(f"   📥 Extracting: {m.name}")
                        # Extract directly to the data folder
                        tar.extract(m, path=DATA_DIR.parent) 

            # Cleanup shard to save C: drive space
            if os.path.exists(local_path):
                os.remove(local_path)
            shutil.rmtree(Path(local_path).parent, ignore_errors=True)

        except Exception as e:
            print(f"❌ Error on {shard_id}: {e}")

if __name__ == "__main__":
    recover_parquets()