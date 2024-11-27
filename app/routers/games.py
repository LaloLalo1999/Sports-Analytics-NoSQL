from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime, timedelta
from ..schemas.game import GameResponse, GameCreate, GameUpdate
from ..database.cassandra import cassandra_db
from uuid import UUID

router = APIRouter()

@router.get("/", response_model=List[GameResponse])
async def get_games(
    date: Optional[datetime] = None,
    days: Optional[int] = Query(default=1, ge=1, le=30)
):
    """
    Get games for a specific date or date range
    """
    if not date:
        date = datetime.utcnow()
    
    end_date = date + timedelta(days=days)
    
    query = f"""
        SELECT * FROM gamedetails 
        WHERE date >= '{date.date()}' AND date < '{end_date.date()}'
    """
    
    result = cassandra_db.session.execute(query)
    return list(result)

@router.get("/{game_id}", response_model=GameResponse)
async def get_game(game_id: UUID):
    """
    Get details for a specific game
    """
    query = f"""
        SELECT * FROM gamedetails 
        WHERE game_id = {game_id}
        LIMIT 1
    """
    
    result = cassandra_db.session.execute(query)
    game = result.one()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.get("/{game_id}/highlights")
async def get_game_highlights(game_id: UUID):
    """
    Get highlight video link for a specific game
    """
    query = f"""
        SELECT highlight_video_link FROM gamedetails 
        WHERE game_id = {game_id}
        LIMIT 1
    """
    
    result = cassandra_db.session.execute(query)
    game = result.one()
    if not game or not game.highlight_video_link:
        raise HTTPException(status_code=404, detail="Highlights not found")
    return {"highlight_video_link": game.highlight_video_link}

@router.get("/search")
async def search_games(
    team_name: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    stage: Optional[str] = None
):
    """
    Search games with various filters
    """
    conditions = []
    if start_date and end_date:
        conditions.append(f"date >= '{start_date.date()}' AND date <= '{end_date.date()}'")
    if team_name:
        conditions.append(f"(team1_name = '{team_name}' OR team2_name = '{team_name}')")
    if stage:
        conditions.append(f"stage = '{stage}'")
    
    query = "SELECT * FROM gamedetails"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    result = cassandra_db.session.execute(query)
    return list(result) 