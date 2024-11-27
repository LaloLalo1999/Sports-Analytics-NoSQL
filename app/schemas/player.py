from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class PlayerBase(BaseModel):
    player_id: str
    name: str
    position: str
    season_stats: str

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(PlayerBase):
    name: Optional[str] = None
    position: Optional[str] = None
    season_stats: Optional[str] = None

class PlayerTeam(BaseModel):
    team_id: str
    team_name: str

class PlayerGame(BaseModel):
    game_id: UUID
    date: datetime
    team_id: str
    opponent_team_id: str
    stage: str

class PlayerResponse(PlayerBase):
    current_team: Optional[PlayerTeam] = None
    games_played: List[PlayerGame] = []

    class Config:
        orm_mode = True 