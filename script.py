import requests
import csv
from datetime import datetime

API_KEY = "9e7d7a66-cf45-45f3-bb0f-062ddf0661de"
url_2 = f"https://api.hypixel.net/playerCount?key={API_KEY}"

response = requests.get(url_2)
data = response.json()

if data.get("success"):
    total_players = data["playerCount"]  # Total players online
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append to CSV file
    with open("player_counts.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, total_players])

    print(f"Data saved: {timestamp}, {total_players}")
else:
    print(f"Error: {data.get('cause')}")
