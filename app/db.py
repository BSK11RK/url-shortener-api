# DB接続
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


# dataフォルダ作成
os.makedirs("data", exist_ok=True)

DATABASE_URL = "sqlite:///./data/app.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()