# メイン機能
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import crud
import random, string


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def create_short_code():
    return ''.join(random.choices(string.ascii_letters, k=6))


@router.post("/urls")
def create_short_url(original_url: str, db: Session = Depends(get_db)):
    code = create_short_code()
    return crud.create_url(db, original_url, code, user_id=1)