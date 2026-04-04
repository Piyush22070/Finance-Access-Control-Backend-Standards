import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from fastapi import HTTPException

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis Client connection
try:
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
except redis.RedisError as e:
    redis_client = None
    raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

