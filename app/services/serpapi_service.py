import os
from serpapi import GoogleSearch
from datetime import datetime
from ..database.cassandra import cassandra_db
import uuid

class SerpAPIService:
    def __init__(self):
        self.api_key = os.getenv('SERPAPI_API_KEY')

    async def fetch_games(self, date=None):
        params = {
            "engine": "google",
            "q": "NBA games today",  # We can modify this query as needed
            "api_key": self.api_key,
            "sports_results_tab": "matches"
        }

        if date:
            params["q"] = f"NBA games on {date}"

        search = GoogleSearch(params)
        results = search.get_dict()

        if "sports_results" not in results:
            return []

        games = []
        for game in results.get("sports_results", {}).get("games", []):
            game_data = {
                "game_id": uuid.uuid4(),
                "date": datetime.strptime(date or datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d').date(),
                "stage": game.get("stage", "SCHEDULED"),
                "team1_id": uuid.uuid4(),  # You might want to map this to your actual team IDs
                "team1_name": game["teams"][0]["name"],
                "team1_score": int(game["teams"][0].get("score", 0)),
                "team2_id": uuid.uuid4(),  # You might want to map this to your actual team IDs
                "team2_name": game["teams"][1]["name"],
                "team2_score": int(game["teams"][1].get("score", 0)),
                "highlight_video_link": game.get("video_highlights", {}).get("link", "")
            }
            games.append(game_data)
            
            # Store in Cassandra
            self.store_game(game_data)

        return games

    def store_game(self, game_data):
        # Store in gamedetails table
        query = """
            INSERT INTO gamedetails (
                date, game_id, stage, team1_id, team1_name, team1_score,
                team2_id, team2_name, team2_score, highlight_video_link
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cassandra_db.session.execute(query, [
            game_data["date"],
            game_data["game_id"],
            game_data["stage"],
            game_data["team1_id"],
            game_data["team1_name"],
            game_data["team1_score"],
            game_data["team2_id"],
            game_data["team2_name"],
            game_data["team2_score"],
            game_data["highlight_video_link"]
        ])

        # Store in teamgames table for both teams
        team_query = """
            INSERT INTO teamgames (
                team_id, date, game_id, opponent_team_id, opponent_team_name,
                team_score, opponent_score, highlight_video_link
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # For team1
        cassandra_db.session.execute(team_query, [
            game_data["team1_id"],
            game_data["date"],
            game_data["game_id"],
            game_data["team2_id"],
            game_data["team2_name"],
            game_data["team1_score"],
            game_data["team2_score"],
            game_data["highlight_video_link"]
        ])

        # For team2
        cassandra_db.session.execute(team_query, [
            game_data["team2_id"],
            game_data["date"],
            game_data["game_id"],
            game_data["team1_id"],
            game_data["team1_name"],
            game_data["team2_score"],
            game_data["team1_score"],
            game_data["highlight_video_link"]
        ])

serpapi_service = SerpAPIService() 