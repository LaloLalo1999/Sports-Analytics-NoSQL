from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime
from ..schemas.team import TeamResponse, TeamCreate, TeamUpdate
from ..database.mongodb import mongodb
from ..database.cassandra import cassandra_db
from bson import ObjectId
from ..services.auth import get_current_user
from ..services.serpapi_service import serpapi_service
import uuid

router = APIRouter()

@router.get("/", response_model=List[TeamResponse])
async def get_teams(
    conference: Optional[str] = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
):
    """
    Get all teams with optional conference filter and pagination.
    First tries to fetch from SerpAPI, then falls back to database.
    """
    try:
        # Normalize conference parameter
        normalized_conference = conference.upper() if conference else None
        
        # First try to fetch from SerpAPI
        teams = await serpapi_service.fetch_teams(normalized_conference)
        if teams:
            # Store teams in MongoDB
            db = await mongodb.get_db()
            for team in teams:
                # Remove id before storing to let MongoDB generate it
                store_team = team.copy()
                if 'id' in store_team:
                    del store_team['id']
                    
                await db.teams.update_one(
                    {"team_name": team["team_name"]},
                    {"$set": store_team},
                    upsert=True
                )
            
            # Apply pagination
            paginated_teams = teams[skip:skip + limit]
            return [TeamResponse(**team) for team in paginated_teams]

    except Exception as e:
        print(f"Error fetching teams from SerpAPI: {str(e)}")

    # Fallback to database
    db = await mongodb.get_db()
    query = {}
    if normalized_conference:
        query["conference"] = normalized_conference
    
    cursor = db.teams.find(query).skip(skip).limit(limit)
    teams = await cursor.to_list(length=limit)
    
    # Debug print
    print(f"Found {len(teams)} teams in database with query: {query}")
    
    return [TeamResponse(**{**team, "id": str(team["_id"])}) for team in teams]

@router.get("/standings", response_model=List[TeamResponse])
async def get_standings(conference: Optional[str] = None):
    """
    Get team standings, optionally filtered by conference.
    First tries to fetch from SerpAPI, then falls back to database.
    """
    try:
        # Normalize conference parameter
        normalized_conference = conference.upper() if conference else None
        
        # First try to fetch from SerpAPI
        teams = await serpapi_service.fetch_teams(normalized_conference)
        if teams:
            print(f"Found {len(teams)} teams from SerpAPI")
            # Store teams in MongoDB
            db = await mongodb.get_db()
            for team in teams:
                # Remove id before storing to let MongoDB generate it
                store_team = team.copy()
                if 'id' in store_team:
                    del store_team['id']
                    
                await db.teams.update_one(
                    {"team_name": team["team_name"]},
                    {"$set": store_team},
                    upsert=True
                )
            return [TeamResponse(**team) for team in teams]

    except Exception as e:
        print(f"Error fetching standings from SerpAPI: {str(e)}")

    # Fallback to database
    db = await mongodb.get_db()
    query = {}
    if normalized_conference:
        query["conference"] = normalized_conference
    
    cursor = db.teams.find(query).sort([
        ("conference", 1),
        ("position", 1)
    ])
    teams = await cursor.to_list(length=100)
    print(f"Found {len(teams)} teams in database with query: {query}")
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
    end_date: Optional[datetime] = None,
    include_live: bool = Query(default=True, description="Include live games from SerpAPI")
):
    """
    Get games for a specific team with optional date range.
    Combines historical data from Cassandra with live data from SerpAPI.
    """
    # Get historical games from Cassandra
    query = "SELECT * FROM teamgames WHERE team_id = ?"
    params = [uuid.UUID(team_id)]
    
    if start_date and end_date:
        query += " AND date >= ? AND date <= ?"
        params.extend([start_date, end_date])
    
    cassandra_games = list(cassandra_db.session.execute(query, params))
    
    # If include_live is True and we're looking for current/future games,
    # fetch additional data from SerpAPI
    games = cassandra_games
    if include_live and (
        not end_date or end_date >= datetime.now().date()
    ):
        # Get team details to match with SerpAPI data
        db = await mongodb.get_db()
        team = await db.teams.find_one({"_id": ObjectId(team_id)})
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
            
        team_name = team.get("team_name")
        
        # Fetch live games from SerpAPI
        live_games = await serpapi_service.fetch_games()
        
        # Filter games for the requested team
        team_live_games = [
            game for game in live_games
            if team_name in [game["team1_name"], game["team2_name"]]
        ]
        
        # Combine the results, avoiding duplicates
        existing_game_ids = {game.game_id for game in cassandra_games}
        for live_game in team_live_games:
            if live_game["game_id"] not in existing_game_ids:
                games.append(live_game)
    
    return games

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