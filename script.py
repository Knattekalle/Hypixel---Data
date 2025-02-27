import requests
import csv
from datetime import datetime

API_KEY = "95632453-ba5f-4c66-aa20-c051e33b830d"
URL = f"https://api.hypixel.net/playerCount?key={API_KEY}"

response = requests.get(URL)
data = response.json()

if data.get("success"):
    total_players = data["playerCount"]  # Total players online
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current time

    print(f"{timestamp} - Total Players Online: {total_players}")

    # Append data to CSV file
    csv_filename = "player_counts.csv"
    with open(csv_filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, total_players])

else:
    print(f"Error: {data.get('cause')}")
