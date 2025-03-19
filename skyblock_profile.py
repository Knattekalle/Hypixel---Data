import csv
import requests
import os
import datetime

# API Keys & URLs
API_KEY = os.getenv("HYPIXEL_API_KEY")
UUID = 29135e50-c229-404b-a0b2-a147abc374fc # UUID = Knattekalle
API_SKYBLOCK_PROFILE = f"https://api.hypixel.net/v2/skyblock/profiles?uuid={UUID}&key={API_KEY}"

# CSV File Names
SKYBLOCK_PROFILE_CSV = "sktblock_profile.csv"
