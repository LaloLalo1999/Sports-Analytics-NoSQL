from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime, date
from ..database.cassandra import cassandra_db
from ..schemas.game import GameResponse
from ..services.serpapi_service import serpapi_service
import uuid

router = APIRouter()

@router.get("/", response_model=list[GameResponse])
async def get_games(
    date: Optional[date] = Query(None, description="Filter games by date (YYYY-MM-DD)")
):
    """
    Get games for a specific date
    """
    try:
        # First try to fetch from SerpAPI
        games = await serpapi_service.fetch_games(date)
        if games:
            return games

        # If no games from SerpAPI, try to fetch from database
        if date:
            query = "SELECT * FROM gamedetails WHERE date = %s"
            result = cassandra_db.session.execute(query, [date])
        else:
            today = datetime.now().date()
            query = "SELECT * FROM gamedetails WHERE date = %s"
            result = cassandra_db.session.execute(query, [today])

        games = []
        for row in result:
            game = {
                "game_id": str(row.game_id),
                "date": row.date,
                "stage": row.stage,
                "team1_id": str(row.team1_id),
                "team1_name": row.team1_name,
                "team1_score": row.team1_score,
                "team2_id": str(row.team2_id),
                "team2_name": row.team2_name,
                "team2_score": row.team2_score,
                "highlight_video_link": row.highlight_video_link
            }
            games.append(game)
        
        return games
    except Exception as e:
        print(f"Error fetching games: {str(e)}")
        return []

@router.get("/recent")
async def get_recent_games():
    """
    Get recent games
    """
    try:
        # Fetch recent games from SerpAPI
        games = await serpapi_service.fetch_games()
        return games
    except Exception as e:
        print(f"Error fetching recent games: {str(e)}")
        return []

@router.get("/{game_id}/highlights")
async def get_game_highlights(game_id: str):
    """
    Get highlights for a specific game
    """
    try:
        game_uuid = uuid.UUID(game_id)
        query = "SELECT highlight_video_link FROM gamedetails WHERE game_id = %s ALLOW FILTERING"
        result = cassandra_db.session.execute(query, [game_uuid])
        row = result.one()
        if row:
            return {"highlight_video_link": row.highlight_video_link}
        return {"highlight_video_link": None}
    except Exception as e:
        print(f"Error fetching highlights: {str(e)}")
        return {"highlight_video_link": None} 