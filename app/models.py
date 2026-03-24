# テーブル定義
from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    
    
class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True)
    original_url = Column(String)
    short_code = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    click_count = Column(Integer, default=0)