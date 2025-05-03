import csv
import requests
import os
import datetime

# API Keys & URLs
API_KEY = os.getenv("SUBMITTED_HYPIXEL_API_KEY")
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



