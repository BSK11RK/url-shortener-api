# DB操作
from sqlalchemy.orm import Session
from app import models, auth


def create_user(db: Session, email: str, password: str):
    hashed_password = auth.hash_password(password)
    user = models.User(email=email, password=hashed_password)
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


def get_user_urls(db: Session, user_id: int, limit: int, offset: int):
    return (
        db.query(models.URL)
        .filter(models.URL.user_id == user_id)
        .offset(offset).limit(limit).all()
    )


def delete_url(db: Session, url_id: int, user_id: int):
    url = db.query(models.URL).filter(models.URL.id == url_id).first()
    
    if not url:
        return None
    
    if url.user_id != user_id:
        return None
    
    db.delete(url)
    db.commit()
    return url