import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from src.config.config import Config

config = Config()

FLASK_ENV = os.getenv("FLASK_ENV", "development")

if FLASK_ENV == "test":
    DATABASE_URL = "sqlite:///:memory:"  # Base de datos en memoria para tests
    engine = create_engine(DATABASE_URL)
else:
    DATABASE_URL = f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

