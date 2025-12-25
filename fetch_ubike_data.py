import requests
import json
import os
from datetime import datetime
import time

# Constants
API_URL = "https://data.ntpc.gov.tw/api/datasets/010e5b15-3823-4b20-b401-b1cf000550c5/json"
DATA_FILE = "ubike_data.json"
MAX_HISTORY_POINTS = 340 # Approx 7 days (48 * 7) + buffer

def fetch_data():
    try:
        response = requests.get(API_URL, params={"page": 0, "size": 1000}, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def filter_stations(data):
    target_stations = []
    # Filter keywords: You can adjust these to find specific stations
    keywords = ["板橋車站", "捷運板橋站", "板橋福德公園", "新府區運路口"]
    
    for station in data:
        name = station.get("sna", "")
        if any(k in name for k in keywords):
            # Extract relevant fields
            # sbi: available bikes
            # bemp: empty spaces
            # act: 1 = active
            if station.get("act") == "1":
                target_stations.append({
                    "station": name,
                    "available": int(station.get("sbi", 0)),
                    "total": int(station.get("tot", 0))
                })
    
    return target_stations

def update_json(new_data):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Load existing data
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []
    else:
        history = []
    
    # Create new entry
    entry = {
        "time": current_time,
        "stations": new_data
    }
    
    history.append(entry)
    
    # Prune old data if needed
    if len(history) > MAX_HISTORY_POINTS:
        history = history[-MAX_HISTORY_POINTS:]
        
    # Save back
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    print(f"Updated {DATA_FILE} at {current_time} with {len(new_data)} stations.")

def main():
    print("Fetching YouBike data...")
    raw_data = fetch_data()
    if not raw_data:
        print("No data received.")
        return

    filtered_data = filter_stations(raw_data)
    if not filtered_data:
        print("No matching stations found in the current batch. Ensure pagination handles all stations if list is long.")
        # Note: The API defaults to size=100. If New Taipei has many stations, we might need to loop pages.
        # But for now let's see if 1000 covers it (passed in fetch_data).
        
    print(f"Found {len(filtered_data)} stations.")
    update_json(filtered_data)

if __name__ == "__main__":
    main()
