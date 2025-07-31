from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from .database import Base

class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    team_a_id = Column(Integer, ForeignKey('teams.id'))
    team_b_id = Column(Integer, ForeignKey('teams.id'))
    team_a = relationship('Team', foreign_keys=[team_a_id])
    team_b = relationship('Team', foreign_keys=[team_b_id])

class BookmakerOdd(Base):
    __tablename__ = 'bookmaker_odds'
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey('matches.id'))
    outcome = Column(String)  # e.g., 'A', 'B', 'draw'
    odd = Column(Float)
    match = relationship('Match', back_populates='odds')

Match.odds = relationship('BookmakerOdd', back_populates='match')

class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey('matches.id'))
    outcome = Column(String)
    probability = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    match = relationship('Match')

class PredictionHistory(Base):
    __tablename__ = 'prediction_history'
    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey('predictions.id'))
    result = Column(String)  # 'win' or 'loss'
    value_bet = Column(Integer)  # 1 if value bet, 0 otherwise
    evaluated_at = Column(DateTime, default=datetime.utcnow)
    prediction = relationship('Prediction')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class FavoriteMatch(Base):
    __tablename__ = 'favorite_matches'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    match_id = Column(Integer, ForeignKey('matches.id'))
    user = relationship('User')
    match = relationship('Match')

class FavoritePrediction(Base):
    __tablename__ = 'favorite_predictions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    prediction_id = Column(Integer, ForeignKey('predictions.id'))
    user = relationship('User')
    prediction = relationship('Prediction')
