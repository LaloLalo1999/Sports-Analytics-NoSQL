from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime
from ..schemas.team import TeamResponse, TeamCreate, TeamUpdate
from ..database.mongodb import mongodb
from ..database.cassandra import cassandra_db
from bson import ObjectId
from ..services.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TeamResponse])
async def get_teams(
    conference: Optional[str] = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
):
    """
    Get all teams with optional conference filter and pagination
    """
    db = await mongodb.get_db()
    query = {}
    if conference:
        query["conference"] = conference.upper()
    
    cursor = db.teams.find(query).skip(skip).limit(limit)
    teams = await cursor.to_list(length=limit)
    return [TeamResponse(**{**team, "id": str(team["_id"])}) for team in teams]

@router.get("/standings", response_model=List[TeamResponse])
async def get_standings(conference: Optional[str] = None):
    """
    Get team standings, optionally filtered by conference
    """
    db = await mongodb.get_db()
    query = {}
    if conference:
        query["conference"] = conference.upper()
    
    cursor = db.teams.find(query).sort([
        ("conference", 1),
        ("position", 1)
    ])
    teams = await cursor.to_list(length=100)
    return [TeamResponse(**{**team, "id": str(team["_id"])}) for team in teams]

@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(team_id: str):
    """
    Get a specific team by ID
    """
    db = await mongodb.get_db()
    team = await db.teams.find_one({"_id": ObjectId(team_id)})
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return TeamResponse(**{**team, "id": str(team["_id"])})

@router.get("/{team_id}/games")
async def get_team_games(
    team_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Get games for a specific team with optional date range
    """
    # Query Cassandra for team games
    query = f"""
        SELECT * FROM teamgames 
        WHERE team_id = {team_id}
    """
    if start_date and end_date:
        query += f" AND date >= '{start_date}' AND date <= '{end_date}'"
    
    result = cassandra_db.session.execute(query)
    return list(result)

@router.get("/search/{team_name}")
async def search_teams(team_name: str):
    """
    Search teams by name
    """
    db = await mongodb.get_db()
    regex_query = {"team_name": {"$regex": team_name, "$options": "i"}}
    cursor = db.teams.find(regex_query)
    teams = await cursor.to_list(length=10)
    return [TeamResponse(**{**team, "id": str(team["_id"])}) for team in teams] 