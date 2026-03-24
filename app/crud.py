# DB操作
from sqlalchemy.orm import Session
from app import models


def create_user(db: Session, email: str, password: str):
    user = models.User(email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_url(db: Session, original_url: str, short_code: str, user_id: int):
    url = models.URL(
        original_url=original_url,
        short_code=short_code,
        user_id=user_id
    )
    db.add(url)
    db.commit()
    db.refresh(url)
    return url