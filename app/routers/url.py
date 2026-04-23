# メイン機能
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import random, string

from app.db import SessionLocal
from app.auth import get_current_user
from app import crud, models, schemas, auth


router = APIRouter(tags=["urls"])


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
@router.get("/urls", response_model=list[schemas.URLResponse])
def get_urls(
    limit: int = Query(10, le=100),
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    return crud.get_user_urls(db, current_user.id, limit, offset)
    
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


@router.delete("/urls/{url_id}")
def delete_url(
    url_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    deleted = crud.delete_url(db, url_id, current_user.id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="URLが見つかりません")
    return {"message": "削除しました"}