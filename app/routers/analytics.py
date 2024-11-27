from fastapi import APIRouter, HTTPException
from typing import Optional
from ..services.analytics_service import analytics_service

router = APIRouter()

@router.get("/teams/head-to-head/{team1_id}/{team2_id}")
async def get_head_to_head_stats(team1_id: str, team2_id: str):
    """Get head-to-head statistics between two teams"""
    stats = await analytics_service.get_head_to_head_stats(team1_id, team2_id)
    return stats

@router.get("/teams/performance/{team_id}")
async def get_team_performance(team_id: str, last_n_games: Optional[int] = 10):
    """Get team performance trends"""
    trend = await analytics_service.get_team_performance_trend(team_id, last_n_games)
    return trend

@router.get("/players/performance/{player_id}")
async def get_player_performance(player_id: str):
    """Get player performance trends"""
    trend = await analytics_service.get_player_performance_trend(player_id)
    if not trend:
        raise HTTPException(status_code=404, detail="Player not found")
    return trend 