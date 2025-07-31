from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class Team(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Match(BaseModel):
    id: int
    date: datetime
    team_a: Team
    team_b: Team

    class Config:
        orm_mode = True

class BookmakerOdd(BaseModel):
    id: int
    outcome: str
    odd: float

    class Config:
        orm_mode = True

class Prediction(BaseModel):
    id: int
    outcome: str
    probability: float
    created_at: datetime

    class Config:
        orm_mode = True

class PredictionWithValue(Prediction):
    is_value_bet: bool

class PredictionHistory(BaseModel):
    id: int
    prediction_id: int
    result: str
    value_bet: int
    evaluated_at: datetime

    class Config:
        orm_mode = True

class LeaderboardEntry(BaseModel):
    team: str
    predictions: int
    wins: int

class FavoriteMatch(BaseModel):
    id: int
    match: Match

    class Config:
        orm_mode = True

class FavoritePrediction(BaseModel):
    id: int
    prediction: Prediction

    class Config:
        orm_mode = True
