import os
from serpapi import GoogleSearch
from datetime import datetime, date
from ..database.cassandra import cassandra_db
import uuid
from bson import ObjectId

class SerpAPIService:
    def __init__(self):
        self.api_key = os.getenv('SERPAPI_API_KEY')

    async def fetch_games(self, date_param=None, store_in_db=True):
        """
        Fetch games from SerpAPI
        Args:
            date_param: Optional date to fetch games for
            store_in_db: Whether to store results in Cassandra (default: True)
        """
        params = {
            "engine": "google",
            "q": "NBA games today",
            "api_key": self.api_key,
            "sports_results_tab": "matches"
        }

        if date_param:
            params["q"] = f"NBA games on {date_param}"

        search = GoogleSearch(params)
        results = search.get_dict()

        if "sports_results" not in results:
            return []

        games = []
        for game in results.get("sports_results", {}).get("games", []):
            # Convert string date to date object if provided, otherwise use today
            game_date = (
                date_param if isinstance(date_param, date)
                else datetime.strptime(date_param, '%Y-%m-%d').date() if date_param
                else datetime.now().date()
            )

            game_data = {
                "game_id": uuid.uuid4(),
                "date": game_date,
                "stage": game.get("stage", "SCHEDULED"),
                "team1_id": uuid.uuid4(),
                "team1_name": game["teams"][0]["name"],
                "team1_score": int(game["teams"][0].get("score", 0)),
                "team2_id": uuid.uuid4(),
                "team2_name": game["teams"][1]["name"],
                "team2_score": int(game["teams"][1].get("score", 0)),
                "highlight_video_link": game.get("video_highlights", {}).get("link") or ""
            }
            games.append(game_data)
            
            if store_in_db:
                try:
                    self.store_game(game_data)
                except Exception as e:
                    print(f"Warning: Failed to store game in Cassandra: {str(e)}")
                    print(f"Game data: {game_data}")

        return games

    def store_game(self, game_data):
        """Store game data in Cassandra database"""
        if not hasattr(cassandra_db, 'session') or not cassandra_db.session:
            raise RuntimeError("Cassandra session not initialized")

        # Prepare statements for better performance and safety
        gamedetails_stmt = cassandra_db.session.prepare("""
            INSERT INTO gamedetails (
                date, game_id, stage, team1_id, team1_name, team1_score,
                team2_id, team2_name, team2_score, highlight_video_link
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """)
        
        teamgames_stmt = cassandra_db.session.prepare("""
            INSERT INTO teamgames (
                team_id, date, game_id, opponent_team_id, opponent_team_name,
                team_score, opponent_score, highlight_video_link
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """)

        try:
            # Execute gamedetails insert
            cassandra_db.session.execute(gamedetails_stmt, [
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

            # Execute teamgames insert for team1
            cassandra_db.session.execute(teamgames_stmt, [
                game_data["team1_id"],
                game_data["date"],
                game_data["game_id"],
                game_data["team2_id"],
                game_data["team2_name"],
                game_data["team1_score"],
                game_data["team2_score"],
                game_data["highlight_video_link"]
            ])

            # Execute teamgames insert for team2
            cassandra_db.session.execute(teamgames_stmt, [
                game_data["team2_id"],
                game_data["date"],
                game_data["game_id"],
                game_data["team1_id"],
                game_data["team1_name"],
                game_data["team2_score"],
                game_data["team1_score"],
                game_data["highlight_video_link"]
            ])
            
        except Exception as e:
            print(f"Error details for game {game_data['game_id']}: {str(e)}")
            raise

    async def fetch_teams(self, conference=None):
        """
        Fetch NBA teams from SerpAPI
        Args:
            conference: Optional conference filter ('eastern' or 'western')
        """
        params = {
            "engine": "google",
            "q": "NBA standings",
            "api_key": self.api_key,
            "sports_results_tab": "standings",  # Specifically request standings
            "hl": "en",
            "gl": "us",
            "google_domain": "google.com"
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            print("Debugging sports_results:", results.get("sports_results", {}))
            
            if "sports_results" not in results:
                print("No sports results found in SerpAPI response")
                return []

            # Get the standings data directly from sports_results
            standings = results.get("sports_results", {}).get("standings", [])
            if not standings:
                print("No standings data found")
                return []

            teams = []
            conference_map = {
                "eastern": "EASTERN",
                "western": "WESTERN",
                "east": "EASTERN",
                "west": "WESTERN"
            }

            for conf_standings in standings:
                # Get conference name from the standings section title
                conf_title = conf_standings.get("name", "").lower()
                conf_name = next((k for k in conference_map.keys() 
                                if k in conf_title), None)
                
                if not conf_name:
                    print(f"Unknown conference name in title: {conf_title}")
                    continue

                normalized_conf = conference_map[conf_name]
                if conference and normalized_conf.lower() != conference.lower():
                    continue

                # Process teams in this conference
                for team in conf_standings.get("teams", []):
                    try:
                        team_data = {
                            "team_name": team.get("name", ""),
                            "conference": normalized_conf,
                            "position": int(team.get("position", 0)),
                            "wins": int(team.get("wins", 0)),
                            "losses": int(team.get("losses", 0)),
                            "games_behind": float(team.get("games_behind", "0").replace("-", "0")),
                            "conf_record": team.get("conference_record", "0-0"),
                            "home_record": team.get("home_record", "0-0"),
                            "away_record": team.get("away_record", "0-0"),
                            "last_10": team.get("last_10", "0-0"),
                            "streak": team.get("streak", "")
                        }
                        teams.append(team_data)
                        print(f"Processed team: {team_data['team_name']} ({team_data['conference']})")
                    except (KeyError, ValueError) as e:
                        print(f"Error processing team data: {e}")
                        print(f"Raw team data: {team}")
                        continue

            print(f"Found {len(teams)} teams from SerpAPI")
            return teams

        except Exception as e:
            print(f"Error in fetch_teams: {str(e)}")
            print(f"Full error: {str(e.__class__.__name__)}: {str(e)}")
            return []

serpapi_service = SerpAPIService() 