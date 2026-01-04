import os
import json
import subprocess
import shutil
from pathlib import Path

# Path to your project data folder (which is the symlink to D:)
BASE_DIR = Path("/home/koushik/projects/NitroGen_witcher/data/labelled_videos/witcher_3")

def check_disk_space():
    # Check space on the D: drive (mounted as /mnt/d)
    total, used, free = shutil.disk_usage("/mnt/d")
    free_gb = free // (2**30)
    print(f"💾 D: Drive Space Remaining: {free_gb} GB")
    if free_gb < 10:
        print("🛑 WARNING: Less than 10GB remaining on D: Drive. Stopping.")
        return False
    return True

def download_chunks():
    if not check_disk_space(): return

    # Find all metadata files
    meta_files = list(BASE_DIR.rglob("metadata.json"))
    total_chunks = len(meta_files)
    print(f"🎬 Found {total_chunks} chunks. Starting download process...")

    for i, meta_path in enumerate(meta_files, 1):
        target_dir = meta_path.parent
        output_file = target_dir / "video.mp4"

        # Skip if already downloaded
        if output_file.exists():
            continue

        # Check space every 50 downloads
        if i % 50 == 0:
            if not check_disk_space(): break

        try:
            with open(meta_path, 'r') as f:
                meta = json.load(f)
            
            vid_info = meta.get('original_video', {})
            url = vid_info.get('url')
            start = vid_info.get('start_time')
            end = vid_info.get('end_time')

            print(f"[{i}/{total_chunks}] 📥 Downloading: {target_dir.name} ({start}s-{end}s)")

            # Precise download using yt-dlp + ffmpeg
            command = [
                "yt-dlp",
                "--download-sections", f"*{start}-{end}",
                "--force-keyframes-at-cuts",
                "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                "--merge-output-format", "mp4",
                "-o", str(output_file),
                url
            ]

            # We use capture_output to keep the terminal from being flooded with yt-dlp logs
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"⚠️ Failed to download {url}. Error: {result.stderr[:100]}")

        except Exception as e:
            print(f"❌ Error processing {meta_path}: {e}")

if __name__ == "__main__":
    download_chunks()