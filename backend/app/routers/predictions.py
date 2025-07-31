from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/predictions", tags=["predictions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Prediction])
def list_predictions(db: Session = Depends(get_db)):
    return db.query(models.Prediction).all()

def _is_value_bet(pred: models.Prediction, db: Session) -> bool:
    odd = (
        db.query(models.BookmakerOdd)
        .filter(
            models.BookmakerOdd.match_id == pred.match_id,
            models.BookmakerOdd.outcome == pred.outcome,
        )
        .first()
    )
    if not odd:
        return False
    return pred.probability * odd.odd > 1.1

@router.get("/valuebets", response_model=list[schemas.PredictionWithValue])
def list_value_bets(db: Session = Depends(get_db)):
    preds = db.query(models.Prediction).all()
    result = []
    for p in preds:
        result.append(
            schemas.PredictionWithValue(
                id=p.id,
                outcome=p.outcome,
                probability=p.probability,
                created_at=p.created_at,
                is_value_bet=_is_value_bet(p, db),
            )
        )
    return result
