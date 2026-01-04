import os
import json
import pandas as pd
from pathlib import Path

# Paths - Using absolute paths to avoid errors
BASE_DIR = Path("/home/koushik/projects/NitroGen_witcher/data/labelled_videos/witcher_3")
OUTPUT_FILE = Path("/home/koushik/projects/NitroGen_witcher/scripts/witcher_3_analysis.csv")

def run_analysis():
    data_rows = []
    print(f"🔍 Analyzing dataset at: {BASE_DIR}")

    # Use rglob to find all metadata files regardless of depth
    metadata_files = list(BASE_DIR.rglob("metadata.json"))
    
    if not metadata_files:
        print("❌ No metadata.json files found. Check your directory structure!")
        return

    for meta_path in metadata_files:
        chunk_dir = meta_path.parent
        parquet_path = chunk_dir / "actions_raw.parquet"
        
        info = {
            "video_id": "Unknown",
            "chunk_id": "Unknown",
            "source": "Unknown",
            "resolution": "Unknown",
            "duration": 0,
            "action_rows": 0,
            "has_parquet": False
        }

        # 1. Parse nested JSON based on your reference
        try:
            with open(meta_path, 'r') as f:
                meta = json.load(f)
                info["chunk_id"] = meta.get("chunk_id", "Unknown")
                
                vid_data = meta.get("original_video", {})
                info["video_id"] = vid_data.get("video_id", "Unknown")
                info["source"] = vid_data.get("source", "Unknown")
                info["duration"] = vid_data.get("duration", 0)
                
                res = vid_data.get("resolution", [0, 0])
                # Format as Height x Width (1080x1920)
                info["resolution"] = f"{res[0]}x{res[1]}"
        except Exception as e:
            print(f"⚠️ Error reading JSON {meta_path}: {e}")

        # 2. Check Parquet
        if parquet_path.exists():
            try:
                df = pd.read_parquet(parquet_path)
                info["action_rows"] = len(df)
                info["has_parquet"] = True
            except Exception:
                pass

        data_rows.append(info)

    # Generate Report
    df_final = pd.DataFrame(data_rows)
    os.makedirs(OUTPUT_FILE.parent, exist_ok=True)
    df_final.to_csv(OUTPUT_FILE, index=False)
    
    # --- ANALYSIS SUMMARY ---
    total_hours = df_final["duration"].sum() / 3600
    
    print("\n--- ⚔️ WITCHER 3 DATA PROPERTIES ---")
    print(f"📊 Total Video Duration: {total_hours:.2f} Hours")
    print(f"📂 Total Chunks Found: {len(df_final)}")
    print(f"✅ Chunks with Action Labels: {df_final['has_parquet'].sum()}")
    
    print("\n📍 SOURCES:")
    print(df_final['source'].value_counts())
    
    print("\n🖥️ RESOLUTIONS:")
    print(df_final['resolution'].value_counts())
    
    print("\n🔗 SOURCE to RESOLUTION MAPPING:")
    print(df_final.groupby(['source', 'resolution']).size())
    
    print(f"\n✅ Full CSV analysis saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_analysis()