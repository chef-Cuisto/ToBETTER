from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/favorites", tags=["favorites"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/matches/{match_id}", response_model=schemas.FavoriteMatch)
def add_favorite_match(match_id: int, user_id: int, db: Session = Depends(get_db)):
    fav = models.FavoriteMatch(user_id=user_id, match_id=match_id)
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return fav


@router.get("/matches", response_model=list[schemas.FavoriteMatch])
def list_favorite_matches(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.FavoriteMatch).filter(models.FavoriteMatch.user_id == user_id).all()


@router.post("/predictions/{prediction_id}", response_model=schemas.FavoritePrediction)
def add_favorite_prediction(prediction_id: int, user_id: int, db: Session = Depends(get_db)):
    fav = models.FavoritePrediction(user_id=user_id, prediction_id=prediction_id)
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return fav


@router.get("/predictions", response_model=list[schemas.FavoritePrediction])
def list_favorite_predictions(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.FavoritePrediction).filter(models.FavoritePrediction.user_id == user_id).all()
