from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


class TransmissionType(str, Enum):
    manual = "Manual"
    automatic = "Automatic"

class FuelType(str, Enum):
    lpg = "LPG"
    diesel = "Diesel"
    petrol = "Petrol"
    electric = "Electric"
    cng = "CNG"

class OwnerType(str, Enum):
    first_owner = "First Owner"
    second_owner = "Second Owner"
    third_owner = "Third Owner"
    fourth_and_above_owner = "Fourth & Above Owner"
    test_drive_car = "Test Drive Car"

class SellerType(str, Enum):
    trustmark_dealer = "Trustmark Dealer"
    individual = "Individual"
    dealer = "Dealer"

class Car(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # would be nice to have name as enum to avoid useless queries
    # must be generated from the first string in name maybe?
    name: str = Field(index=True)
    year: int = Field(index=True)
    selling_price: int = Field(index=True)
    km_driven: int = Field(index=True)
    fuel: FuelType = Field(index=True)
    seller_type: SellerType = Field(index=True)
    transmission: TransmissionType = Field(index=True)
    owner: OwnerType = Field(index=True)
