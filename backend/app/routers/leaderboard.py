from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from .. import models, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/monthly", response_model=list[schemas.LeaderboardEntry])
def monthly_leaderboard(db: Session = Depends(get_db)):
    month_ago = datetime.utcnow() - timedelta(days=30)
    pred = models.Prediction
    match = models.Match
    hist = models.PredictionHistory

    predicted_team_id = case(
        (
            (pred.outcome == "A", match.team_a_id),
            (pred.outcome == "B", match.team_b_id),
        ),
        else_=None,
    )

    win_case = case([(hist.result == "win", 1)], else_=0)

    query = (
        db.query(
            models.Team.name.label("team"),
            func.count(pred.id).label("predictions"),
            func.sum(win_case).label("wins"),
        )
        .join(match, pred.match_id == match.id)
        .join(models.Team, predicted_team_id == models.Team.id)
        .outerjoin(hist, hist.prediction_id == pred.id)
        .filter(pred.created_at >= month_ago)
        .filter(pred.outcome.in_(["A", "B"]))
        .group_by(models.Team.id)
        .order_by(func.sum(win_case).desc())
    )

    return query.all()
