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

        odds = {}
        for outcome in ["A", "B", "draw"]:
            odd_val = random.uniform(1.5, 3.5)
            odds[outcome] = odd_val
            db.add(models.BookmakerOdd(match_id=match.id, outcome=outcome, odd=odd_val))
        db.commit()

        # create a simple prediction and result
        pred_outcome = random.choice(["A", "B"])
        probability = random.uniform(0.4, 0.6)
        pred = models.Prediction(match_id=match.id, outcome=pred_outcome, probability=probability)
        db.add(pred)
        db.commit()

        is_value = 1 if probability * odds[pred_outcome] > 1.1 else 0

        result = random.choice(["win", "loss"])
        db.add(models.PredictionHistory(prediction_id=pred.id, result=result, value_bet=is_value))
        db.commit()

def main():
    db = SessionLocal()
    create_sample_data(db)
    db.close()

if __name__ == "__main__":
    main()
