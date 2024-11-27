from pydantic import BaseModel
from typing import List, Optional

class TeamBase(BaseModel):
    team_name: str
    conference: str
    position: int
    wins: int
    losses: int
    games_behind: float
    conf_record: str
    home_record: str
    away_record: str
    last_10: str
    streak: str

class TeamCreate(TeamBase):
    pass

class TeamUpdate(TeamBase):
    team_name: Optional[str] = None
    conference: Optional[str] = None
    position: Optional[int] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    games_behind: Optional[float] = None
    conf_record: Optional[str] = None
    home_record: Optional[str] = None
    away_record: Optional[str] = None
    last_10: Optional[str] = None
    streak: Optional[str] = None

class TeamResponse(TeamBase):
    id: str

    class Config:
        orm_mode = True 