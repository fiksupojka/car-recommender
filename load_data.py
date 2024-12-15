"""Script for reading the data from the .csv file."""

import pandas as pd
from sqlmodel import Session

from db import engine
from models import Car


if __name__ == "__main__":
    df = pd.read_csv('cars.csv')
    with Session(engine) as session:
        for _, row in df.iterrows():
            car = Car(
                name=row['name'], year=row['year'], selling_price=row['selling_price'],
                km_driven=row['km_driven'], fuel=row['fuel'], seller_type=row['seller_type'],
                transmission=row['transmission'], owner=row['owner']
            )
            session.add(car)
        session.commit()