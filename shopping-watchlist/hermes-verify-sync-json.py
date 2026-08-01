import json
import os

input_file = "/opt/data/projects/shopping-watchlist/sync_input.json"
try:
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    if "items" not in data:
        print("Verification Failed: Missing 'items' key")
        exit(1)
    
    item_count = len(data["items"])
    print(f"Verification Success: {input_file} is valid JSON with {item_count} items.")
except Exception as e:
    print(f"Verification Failed: {str(e)}")
    exit(1)
