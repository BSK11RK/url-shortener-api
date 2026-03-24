# 認証API
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import crud, schemas, auth, models


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user.email, user.password)


@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).first()
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token}