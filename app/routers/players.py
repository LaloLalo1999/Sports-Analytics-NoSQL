from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from ..schemas.player import PlayerResponse, PlayerCreate, PlayerUpdate
from ..services.dgraph_service import dgraph_service
from ..services.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[PlayerResponse])
async def get_players(
    team_id: Optional[str] = None,
    position: Optional[str] = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
):
    """
    Get players with optional filters
    """
    query = """
    query players($position: string, $team_id: string, $offset: int, $limit: int) {
        players(func: type(Player)) @filter(%s) {
            uid
            player_id
            name
            position
            season_stats
            plays_for @facets(since) {
                uid
                team_id
                name
            }
        }
    } offset: $offset, first: $limit
    """
    
    filters = []
    if position:
        filters.append(f"eq(position, $position)")
    if team_id:
        filters.append(f"has(plays_for) AND uid_in(plays_for, $team_id)")
    
    filter_str = " AND ".join(filters) if filters else "has(player_id)"
    query = query % filter_str
    
    variables = {
        "$position": position,
        "$team_id": team_id,
        "$offset": skip,
        "$limit": limit
    }
    
    result = await dgraph_service.execute_query(query, variables)
    return [PlayerResponse(**player) for player in result["players"]]

@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player(player_id: str):
    """
    Get a specific player by ID
    """
    player = await dgraph_service.get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return PlayerResponse(**player)

@router.get("/{player_id}/games")
async def get_player_games(
    player_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Get games for a specific player with optional date range
    """
    query = """
    query player_games($player_id: string, $start_date: datetime, $end_date: datetime) {
        player(func: eq(player_id, $player_id)) {
            participated_in @facets(stats) @filter(%s) {
                uid
                game_id
                date
                stage
                team1 { uid team_id name }
                team2 { uid team_id name }
            }
        }
    }
    """
    
    date_filter = []
    if start_date:
        date_filter.append(f"ge(date, $start_date)")
    if end_date:
        date_filter.append(f"le(date, $end_date)")
    
    filter_str = " AND ".join(date_filter) if date_filter else "has(game_id)"
    query = query % filter_str
    
    variables = {
        "$player_id": player_id,
        "$start_date": start_date.isoformat() if start_date else None,
        "$end_date": end_date.isoformat() if end_date else None
    }
    
    result = await dgraph_service.execute_query(query, variables)
    return result["player"][0]["participated_in"] if result["player"] else []

@router.get("/search/{player_name}")
async def search_players(player_name: str):
    """
    Search players by name
    """
    query = """
    query search_players($name: string) {
        players(func: type(Player)) @filter(regexp(name, $name, "i")) {
            uid
            player_id
            name
            position
            season_stats
            plays_for @facets(since) {
                uid
                team_id
                name
            }
        }
    }
    """
    
    variables = {"$name": player_name}
    result = await dgraph_service.execute_query(query, variables)
    return result["players"] 