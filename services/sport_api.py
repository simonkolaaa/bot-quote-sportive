import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

class SportAPI:
    def __init__(self):
        self.api_key = os.getenv("X_RAPIDAPI_KEY")
        self.api_host = os.getenv("X_RAPIDAPI_HOST", "sportapi7.p.rapidapi.com")
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }
        self.base_url = f"https://{self.api_host}/api/v1"
        
        # Tournament IDs for Sofascore
        self.tournaments = {
            "serie-a": 31,
            "premier-league": 17,
            "la-liga": 8
        }

    def get_standings(self, league_name):
        tournament_id = self.tournaments.get(league_name)
        if not tournament_id:
            return None
        
        # Need to find the current season ID first (or just use the tournament ID if the API supports it)
        # For simplicity, we'll try to get the latest season/standings
        # Endpoints vary, but usually it's /tournament/{id}/season/{season_id}/standings/total
        # Let's assume we can get it via /tournament/{id}/standings/total (some APIs support this)
        
        url = f"{self.base_url}/unique-tournament/{tournament_id}/standings/total"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        return None

    def get_team_performance(self, team_name, league_name):
        # This is a bit complex as we need to match team names
        # For now, let's return a summary of standings for that team
        standings = self.get_standings(league_name)
        if not standings:
            return "Statistiche non disponibili"
        
        # Parse standings rows
        try:
            rows = standings.get('standings', [{}])[0].get('rows', [])
            for row in rows:
                if team_name.lower() in row.get('team', {}).get('name', '').lower():
                    pos = row.get('position')
                    pts = row.get('points')
                    matches = row.get('matches')
                    wins = row.get('wins')
                    draws = row.get('draws')
                    losses = row.get('losses')
                    return f"Pos: {pos}, Punti: {pts}, W/D/L: {wins}/{draws}/{losses} su {matches} gare"
        except:
            pass
            
        return "Team non trovato in classifica"

if __name__ == "__main__":
    # Test (requires API key)
    api = SportAPI()
    # print(api.get_team_performance("Juventus", "serie-a"))
