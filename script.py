'''
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

'''

import csv
import requests
import os
import datetime

# API Keys & URLs
API_KEY = os.getenv("HYPIXEL_API_KEY")
API_PLAYERCOUNT = f"https://api.hypixel.net/playerCount?key={API_KEY}"
API_PUNISHMENTS = f"https://api.hypixel.net/v2/punishmentstats?key={API_KEY}"
API_GAMECOUNTS = f"https://api.hypixel.net/v2/counts?key={API_KEY}"

# CSV File Names
PLAYER_COUNT_CSV = "player_counts.csv"
PUNISHMENTS_CSV = "punishment_stats.csv"
MAIN_GAMES_CSV = "main_games.csv"
SUB_GAMES_CSV = "sub_games.csv"

def fetch_data(url):
    """Fetch data from the given API URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from {url}: {response.status_code}")
        return None

def write_to_csv(file_name, data, header):
    """Append data to a CSV file, creating it if it doesn't exist."""
    file_exists = os.path.exists(file_name)
    
    with open(file_name, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)  # Write header if file is new
        writer.writerows(data)

def process_player_count(data):
    """Process player count data."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if data.get("success"):
        total_players = data["playerCount"]
        return [[timestamp, total_players]]
    return []

def process_punishment_stats(data):
    """Process punishment stats data."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if data.get("success"):
        return [[
            timestamp, 
            data["watchdog_lastMinute"], 
            data["staff_rollingDaily"], 
            data["watchdog_total"], 
            data["watchdog_rollingDaily"], 
            data["staff_total"]
        ]]
    return []

def process_game_modes(data):
    """Process game mode player counts, separating main games & sub-games."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    main_games = []
    sub_games = []
    
    if data.get("success"):
        for game, details in data["games"].items():
            total_players = details.get("players", 0)
            main_games.append([timestamp, game, total_players, 1])  # Category 1 for main games
            
            if "modes" in details:  # Sub-games exist
                for mode, mode_players in details["modes"].items():
                    sub_games.append([timestamp, f"{game}_{mode}", mode_players, 2, game])  # Category 2 for sub-games
    
    return main_games, sub_games

def main():
    """Main function to fetch and store all data."""
    # Fetch data from APIs
    player_data = fetch_data(API_PLAYERCOUNT)
    punishment_data = fetch_data(API_PUNISHMENTS)
    game_mode_data = fetch_data(API_GAMECOUNTS)

    # Process & Write Player Count Data
    player_count_rows = process_player_count(player_data)
    write_to_csv(PLAYER_COUNT_CSV, player_count_rows, ["timestamp", "total_players"])

    # Process & Write Punishment Stats
    punishment_rows = process_punishment_stats(punishment_data)
    write_to_csv(PUNISHMENTS_CSV, punishment_rows, ["timestamp", "watchdog_last_minute", "staff_rolling_daily", "watchdog_total", "watchdog_rolling_daily", "staff_total"])

    # Process & Write Game Mode Data
    main_games, sub_games = process_game_modes(game_mode_data)
    write_to_csv(MAIN_GAMES_CSV, main_games, ["timestamp", "game", "players", "category"])
    write_to_csv(SUB_GAMES_CSV, sub_games, ["timestamp", "game", "players", "category", "parent_game"])

    print("✅ Data successfully updated!")

if __name__ == "__main__":
    main()



