import requests
import os
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
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
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
        
        for attempt in range(3):
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    print(f"⚠️ Rate limit raggiunto per Sofascore. Attesa 2s... (Tentativo {attempt+1})")
                    import time
                    time.sleep(2)
                else:
                    return None
            except Exception as e:
                print(f"Errore connessione SportAPI: {e}")
                return None
        return None

    def get_match_performance(self, team_home, team_away, league_name):
        standings = self.get_standings(league_name)
        if not standings:
            return "Statistiche classifica non disponibili"
        
        home_stats = "N/D"
        away_stats = "N/D"
        
        try:
            rows = standings.get('standings', [{}])[0].get('rows', [])
            for row in rows:
                team_name_api = row.get('team', {}).get('name', '').lower()
                
                # Cerca un match parziale per essere flessibili sui nomi (es. "Inter" in "Inter Milan")
                if team_home.lower() in team_name_api or team_name_api in team_home.lower():
                    pos = row.get('position', '?')
                    pts = row.get('points', '?')
                    w, d, l = row.get('wins', '?'), row.get('draws', '?'), row.get('losses', '?')
                    home_stats = f"Pos:{pos} Pti:{pts} W{w}-D{d}-L{l}"
                    
                if team_away.lower() in team_name_api or team_name_api in team_away.lower():
                    pos = row.get('position', '?')
                    pts = row.get('points', '?')
                    w, d, l = row.get('wins', '?'), row.get('draws', '?'), row.get('losses', '?')
                    away_stats = f"Pos:{pos} Pti:{pts} W{w}-D{d}-L{l}"
        except Exception as e:
            print(f"Errore parsing classifica: {e}")
            
        return f"{team_home} [{home_stats}] vs {team_away} [{away_stats}]"

if __name__ == "__main__":
    # Test (requires API key)
    api = SportAPI()
    # print(api.get_team_performance("Juventus", "serie-a"))
