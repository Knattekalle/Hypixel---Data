import requests
import csv
from datetime import datetime

API_KEY = "5fb91a80-ab5c-4943-aa32-bbdfdaa38738"

# URLs for the APIs
url_playercount = f"https://api.hypixel.net/playerCount?key={API_KEY}"
url_punishments = f"https://api.hypixel.net/v2/punishmentstats?key={API_KEY}"

# Fetching player count data
response = requests.get(url_playercount)
data = response.json()

if data_playercount.get("success"):
    total_players = data_playercount["playerCount"]  # Total players online
else:
    total_players = None  # In case of an error, set it to None

# Fetching punishment stats data
response_punishments = requests.get(url_punishments)
data_punishments = response_punishments.json()

if data_punishments.get("success"):
    watchdog_lastMinute = data_punishments["watchdog_lastMinute"]
    staff_rollingDaily = data_punishments["staff_rollingDaily"]
    watchdog_total = data_punishments["watchdog_total"]
    watchdog_rollingDaily = data_punishments["watchdog_rollingDaily"]
    staff_total = data_punishments["staff_total"]
else:
    # In case of an error, set punishment stats to None
    watchdog_lastMinute = None
    staff_rollingDaily = None
    watchdog_total = None
    watchdog_rollingDaily = None
    staff_total = None


# Timestamp for when the data is fetched
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Save player count data to the CSV file
with open("player_counts.csv", mode="a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([timestamp, total_players])

print(f"Player Count Data saved: {timestamp}, Players: {total_players}")

# Save punishment stats data to the CSV file
with open("punishment_stats.csv", mode="a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        timestamp, 
        watchdog_lastMinute, 
        staff_rollingDaily, 
        watchdog_total, 
        watchdog_rollingDaily, 
        staff_total
    ])

print(f"Punishment Stats Data saved: {timestamp}, Watchdog Last Minute: {watchdog_lastMinute}, Staff Daily: {staff_rollingDaily}")
