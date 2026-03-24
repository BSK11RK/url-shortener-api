# メイン
from fastapi import FastAPI
from app.routers import auth, url
from app.db import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(url.router)