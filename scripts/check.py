import os
from pathlib import Path

# Get the absolute path to be 100% sure
base_path = Path(__file__).resolve().parent.parent / "data" / "witcher_3"

def debug_paths():
    print(f"📂 Checking absolute path: {base_path}")
    
    if not base_path.exists():
        print("❌ The witcher_3 directory does not exist at this path.")
        return

    # List the first few items to see the structure
    items = list(base_path.rglob("*"))
    print(f"📊 Total items found in witcher_3: {len(items)}")
    
    # Check for metadata vs parquets
    metadata_count = len([i for i in items if i.name == "metadata.json"])
    parquet_count = len([i for i in items if i.suffix == ".parquet"])
    
    print(f"📝 metadata.json files: {metadata_count}")
    print(f"🗃️ .parquet files: {parquet_count}")

    if parquet_count == 0 and metadata_count > 0:
        print("\n⚠️ ANALYSIS: Metadata was extracted, but Parquets were missed.")
        print("This usually means the Parquet file name inside the .tar.gz")
        print("did not match 'actions_processed.parquet' exactly.")

if __name__ == "__main__":
    debug_paths()