from typing import List, Dict, Optional
from datetime import datetime, timedelta
from ..database.mongodb import mongodb
from ..database.cassandra import cassandra_db
from ..database.dgraph import dgraph_db

class AnalyticsService:
    @staticmethod
    async def get_head_to_head_stats(team1_id: str, team2_id: str) -> Dict:
        """Get head-to-head statistics between two teams"""
        query = """
        SELECT * FROM teamgames 
        WHERE team_id = ? AND opponent_team_id = ?
        """
        games = cassandra_db.session.execute(query, [team1_id, team2_id])
        
        stats = {
            "total_games": 0,
            "team1_wins": 0,
            "team2_wins": 0,
            "avg_score_team1": 0,
            "avg_score_team2": 0,
            "last_games": []
        }
        
        total_score_team1 = 0
        total_score_team2 = 0
        
        for game in games:
            stats["total_games"] += 1
            if game.team_score > game.opponent_score:
                stats["team1_wins"] += 1
            else:
                stats["team2_wins"] += 1
            total_score_team1 += game.team_score
            total_score_team2 += game.opponent_score
            
            if len(stats["last_games"]) < 5:
                stats["last_games"].append(game)
        
        if stats["total_games"] > 0:
            stats["avg_score_team1"] = total_score_team1 / stats["total_games"]
            stats["avg_score_team2"] = total_score_team2 / stats["total_games"]
        
        return stats

    @staticmethod
    async def get_team_performance_trend(team_id: str, last_n_games: int = 10) -> List:
        """Get team performance trends over the last N games"""
        query = """
        SELECT * FROM teamgames 
        WHERE team_id = ? 
        ORDER BY date DESC 
        LIMIT ?
        """
        games = cassandra_db.session.execute(query, [team_id, last_n_games])
        return list(games)

    @staticmethod
    async def get_player_performance_trend(player_id: str) -> Dict:
        """Get player's performance trends over the season"""
        query = """
        query player_trend($player_id: string) {
            player(func: eq(player_id, $player_id)) {
                participated_in (orderdesc: date) @facets(stats) {
                    date
                    stats
                }
            }
        }
        """
        variables = {"$player_id": player_id}
        result = await dgraph_service.execute_query(query, variables)
        return result["player"][0] if result["player"] else None

analytics_service = AnalyticsService() 