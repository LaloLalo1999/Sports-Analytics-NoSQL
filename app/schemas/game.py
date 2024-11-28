from pydantic import BaseModel
from typing import Optional
from datetime import date
from uuid import UUID

class GameBase(BaseModel):
    date: date
    stage: str
    team1_id: UUID
    team1_name: str
    team1_score: int
    team2_id: UUID
    team2_name: str
    team2_score: int
    highlight_video_link: Optional[str] = None

class GameCreate(GameBase):
    pass

class GameUpdate(GameBase):
    date: Optional[date] = None
    stage: Optional[str] = None
    team1_score: Optional[int] = None
    team2_score: Optional[int] = None
    highlight_video_link: Optional[str] = None

class GameResponse(GameBase):
    game_id: UUID

    class Config:
        orm_mode = True 