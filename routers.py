from fastapi import Depends, APIRouter
from sqlmodel import Session, select

from db import get_db
from models import Car
from schemas import CarQuery2

router = APIRouter()

@router.get("/cars/")
def read_cars(db: Session = Depends(get_db)):
    return db.execute(select(Car)).scalars().all()

@router.post("/cars/search/")
def search_cars(car_query: CarQuery2, db: Session = Depends(get_db)):
    query = car_query.create_car_db_query()
    return db.execute(query).scalars().all()
