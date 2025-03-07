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


# Process player counts
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

# Process player counts in the different minigames
if data_playercount_minigames.get("success"):
    minigames_playercount = data_playercount_minigames["games"]

    # CSV file path
    csv_file = "game_mode_player_counts.csv"

    # Delete the file if it already exists to ensure we write a new header
    if os.path.exists(csv_file):
        os.remove(csv_file)

    # Write the new CSV with the updated header
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write the header
        header = ["timestamp"]
        for game, details in minigames_playercount.items():
            if "modes" in details:  # This means it has subcategories (modes)
                header.append(game)  # Add the main game name
                for mode in details["modes"]:
                    header.append(f"{game}_{mode}")  # Add each mode as a subcategory
            else:
                header.append(game)  # Add the main game name
        writer.writerow(header)

        # Write the data row
        row = [timestamp]
        for game, details in minigames_playercount.items():
            if "modes" in details:
                row.append(details["players"])  # Add the total player count for the game
                for mode in details["modes"]:
                    row.append(details["modes"][mode])  # Add player count for each mode
            else:
                row.append(details["players"])  # Add the total player count for the game
        writer.writerow(row)

    print(f"Game Mode Data saved: {timestamp}")
else:
    print(f"Error fetching game mode stats: {data_playercount_minigames.get('cause')}")


