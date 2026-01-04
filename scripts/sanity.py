import os
import shutil
from pathlib import Path

# Absolute paths to avoid any WSL/Relative path confusion
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
WITCHER_DIR = DATA_DIR / "witcher_3"
TARGET_DIR = DATA_DIR / "labelled_videos" / "witcher_3"

def sanitize_structure():
    # 1. Create the new home for the data
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📂 Target Directory: {TARGET_DIR}")

    # 2. Move the core witcher_3 structure to labelled_videos
    if WITCHER_DIR.exists():
        print("🚚 Moving witcher_3 folder into labelled_videos...")
        for item in WITCHER_DIR.iterdir():
            dest = TARGET_DIR / item.name
            if not dest.exists():
                shutil.move(str(item), str(dest))
        # Remove the now-empty witcher_3 folder
        if not any(WITCHER_DIR.iterdir()):
            WITCHER_DIR.rmdir()

    # 3. Find and move stray parquets
    print("🧹 Searching for stray parquets to align with metadata...")
    # Look for any SHARD folders at the root of data/ that aren't inside labelled_videos
    for shard_folder in DATA_DIR.glob("SHARD_*"):
        if "labelled_videos" in str(shard_folder):
            continue
            
        print(f"📦 Processing stray shard folder: {shard_folder.name}")
        for parquet in shard_folder.rglob("*.parquet"):
            # Calculate the relative path from the SHARD root
            # Example: SHARD_0091/v1924991184/v1924991184_chunk_0180/actions_raw.parquet
            rel_path = parquet.relative_to(DATA_DIR)
            final_dest = DATA_DIR / "labelled_videos" / "witcher_3" / rel_path
            
            # Ensure the destination chunk folder exists
            final_dest.parent.mkdir(parents=True, exist_ok=True)
            
            # Move the file
            shutil.move(str(parquet), str(final_dest))
            print(f"   ✅ Aligned: {parquet.name} -> {rel_path.parent}")

    # 4. Final Cleanup: Remove empty stray SHARD folders
    for shard_folder in DATA_DIR.glob("SHARD_*"):
        if shard_folder.is_dir() and not "labelled_videos" in str(shard_folder):
            shutil.rmtree(shard_folder)

    print("\n✨ DATA SANITIZATION COMPLETE!")
    print(f"Your training data is now at: {TARGET_DIR}")

if __name__ == "__main__":
    sanitize_structure()