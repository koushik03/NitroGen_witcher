import pandas as pd
from datasets import load_dataset
import os

def get_unique_game_titles():
    print("Starting stream to collect all game titles. This might take a few minutes for the full dataset metadata.")
    
    # Load the dataset using the 'default' configuration name, as 'actions_processed' was invalid.
    dataset_stream = load_dataset("nvidia/NitroGen", "default", split="train", streaming=True)
    
    unique_games = set()
    count = 0
    
    try:
        for example in dataset_stream:
            count += 1
            meta = example.get('metadata', {})
            game_name = meta.get('game', None)
            
            if game_name:
                unique_games.add(game_name)
            
            if count % 10000 == 0:
                print(f"Processed {count} metadata entries. Found {len(unique_games)} unique games so far.")

    except StopIteration:
        print("Reached end of dataset stream.")
    except Exception as e:
        print(f"An error occurred: {e}")

    print(f"\nTotal metadata entries processed: {count}")
    print(f"Total unique games found: {len(unique_games)}")
    
    sorted_games = sorted(list(unique_games))
    
    output_path = "../available_games_list.txt"
    with open(output_path, 'w') as f:
        for game in sorted_games:
            f.write(f"{game}\n")
            
    print(f"List of all games saved to {os.path.abspath(output_path)}")
    
    return sorted_games

if __name__ == "__main__":
    get_unique_game_titles()
