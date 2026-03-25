# メイン機能
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import random, string

from app.db import SessionLocal
from app.auth import get_current_user
from app import crud, models


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def create_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


# URL作成
@router.post("/urls")
def create_short_url(
    original_url: str, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    code = create_short_code()
    return crud.create_url(
        db, 
        original_url=original_url, 
        short_code=code, 
        user_id=current_user.id
    )
    
    
# 自分のURL一覧
@router.get("/urls")
def get_urls(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(crud.models.URL).filter(
        crud.models.URL.user_id == current_user.id
    ).all()
    
    
@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    url = db.query(models.URL).filter(
        models.URL.short_code == short_code
    ).first()
    
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # クリック数増加
    url.click_count += 1
    db.commit()
    return RedirectResponse(url.original_url)