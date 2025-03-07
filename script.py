import requests
import csv
import os
from datetime import datetime

API_KEY = os.getenv("HYPIXEL_API_KEY")

# API URLs
url_playercount = f"https://api.hypixel.net/playerCount?key={API_KEY}"
url_punishments = f"https://api.hypixel.net/v2/punishmentstats?key={API_KEY}"
url_playercount_minigames = f"https://api.hypixel.net/v2/counts?key={API_KEY}"

# Fetch player count data
response_playercount = requests.get(url_playercount)
data_playercount = response_playercount.json()

# Fetch punishment stats data
response_punishments = requests.get(url_punishments)
data_punishments = response_punishments.json()

# Fetch counts data
response_playercount_minigames = requests.get(url_playercount_minigames)
data_playercount_minigames = response_playercount_minigames.json()

# Time
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Process player count
if data_playercount.get("success"):
    total_players = data_playercount["playerCount"]  

    with open("player_counts.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, total_players])

    print(f"Player Count Data saved: {timestamp}, Players: {total_players}")
else:
    print(f"Error fetching player count: {data_playercount.get('cause')}")


# Process punishment stats
if data_punishments.get("success"):
    watchdog_last_minute = data_punishments["watchdog_lastMinute"]
    staff_rolling_daily = data_punishments["staff_rollingDaily"]
    watchdog_total = data_punishments["watchdog_total"]
    watchdog_rolling_daily = data_punishments["watchdog_rollingDaily"]
    staff_total = data_punishments["staff_total"]

    with open("punishment_stats.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, watchdog_last_minute, staff_rolling_daily, watchdog_total, watchdog_rolling_daily, staff_total])

    print(f"Punishment Data saved: {timestamp}, Watchdog Last Minute: {watchdog_last_minute}, Staff Rolling Daily: {staff_rolling_daily}")
else:
    print(f"Error fetching punishment stats: {data_punishments.get('cause')}")


# Process playercounts in the different minigames
if data_playercount_minigames.get("success"):
    minigames_playercount = data_playercount_minigames["games"]

    # CSV header
    csv_file = "game_mode_player_counts.csv"
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write header only if file is new
        if not file_exists:
            header = ["timestamp"] + list(minigames_playercount.keys())
            writer.writerow(header)

        # Extract player counts per game
        row = [timestamp] + [minigames_playercount[game]["players"] for game in minigames_playercount]
        writer.writerow(row)

    print(f"Game Mode Data saved: {timestamp}")
else:
    print(f"Error fetching game mode stats: {data_playercount_minigames.get('cause')}")

