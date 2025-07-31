"""Script simple pour générer des matchs et cotes de démonstration."""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine
from . import models
import random

Base.metadata.create_all(bind=engine)

def create_sample_data(db: Session):
    team_names = ["Equipe A", "Equipe B", "Equipe C", "Equipe D"]
    teams = []
    for name in team_names:
        team = models.Team(name=name)
        db.add(team)
        teams.append(team)
    db.commit()

    tomorrow = datetime.utcnow() + timedelta(days=1)
    for i in range(2):
        match = models.Match(date=tomorrow + timedelta(hours=i), team_a=teams[i], team_b=teams[i+1])
        db.add(match)
        db.commit()
        for outcome in ["A", "B", "draw"]:
            odd = random.uniform(1.5, 3.5)
            db.add(models.BookmakerOdd(match_id=match.id, outcome=outcome, odd=odd))
        db.commit()

def main():
    db = SessionLocal()
    create_sample_data(db)
    db.close()

if __name__ == "__main__":
    main()
