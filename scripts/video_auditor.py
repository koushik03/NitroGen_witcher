import os
import json
import subprocess
import pandas as pd
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Paths
BASE_DIR = Path("/home/koushik/projects/NitroGen_witcher/data/labelled_videos/witcher_3")
OUTPUT_REPORT = Path("/home/koushik/projects/NitroGen_witcher/scripts/twitch_audit_report.csv")

def verify_video_with_ytdlp(video_info):
    video_id, url = video_info
    # Use -g (get URL) as it forces yt-dlp to actually find a playable stream
    command = ["yt-dlp", "-g", url]
    
    try:
        # We capture stderr because that's where the 'Video does not exist' message lives
        result = subprocess.run(command, capture_output=True, text=True, timeout=20)
        
        # Check if the output contains a valid link OR an error message
        if result.returncode == 0 and result.stdout.strip():
            return {"video_id": video_id, "is_alive": True, "url": url, "error": ""}
        else:
            # Catch specific Twitch error strings
            error_msg = result.stderr.strip()
            return {"video_id": video_id, "is_alive": False, "url": url, "error": error_msg}
            
    except subprocess.TimeoutExpired:
        return {"video_id": video_id, "is_alive": False, "url": url, "error": "Timeout"}
    except Exception as e:
        return {"video_id": video_id, "is_alive": False, "url": url, "error": str(e)}

def run_deep_audit():
    print(f"🕵️ Deep Auditing Twitch links in {BASE_DIR}...")
    
    targets = []
    shard_dirs = [d for d in BASE_DIR.glob("SHARD_*") if d.is_dir()]
    
    for shard in shard_dirs:
        video_dirs = [d for d in shard.iterdir() if d.is_dir() and d.name.startswith('v')]
        for v_dir in video_dirs:
            first_chunk = next(v_dir.glob("v*_chunk_*/metadata.json"), None)
            if first_chunk:
                with open(first_chunk, 'r') as f:
                    meta = json.load(f)
                    url = meta.get('original_video', {}).get('url')
                    if url:
                        targets.append((v_dir.name, url))

    print(f"🌐 Verifying {len(targets)} unique videos. This will take a few minutes...")

    # Using max_workers=3 to avoid Twitch IP bans during the audit
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(verify_video_with_ytdlp, targets))

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_REPORT, index=False)
    
    alive_count = df['is_alive'].sum()
    total = len(df)
    
    print("\n--- 🏁 FINAL AUDIT SUMMARY ---")
    print(f"✅ Videos Alive: {alive_count}")
    print(f"❌ Videos Dead:  {total - alive_count}")
    print(f"📈 Survival Rate: {(alive_count / total) * 100:.2f}%")

if __name__ == "__main__":
    run_deep_audit()