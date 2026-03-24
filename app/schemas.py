# クリエイト/レスポンス
from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    
    
class URLCreate(BaseModel):
    original_url: str
    
    
class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    click_count: int
    
    class Config:
        from_attributes = True