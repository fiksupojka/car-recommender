from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine

DATABASE_URL = "postgresql://recommender@0.0.0.0/recommender"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

