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

    class Config:
        orm_mode = True
