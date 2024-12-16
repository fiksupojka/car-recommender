from enum import Enum
from typing import List, Optional, get_type_hints

from pydantic import BaseModel, create_model
from sqlalchemy import or_
from sqlmodel import select, SQLModel
from models import Car

def generate_query_model(model: SQLModel) -> BaseModel:
    """Generates pydantic model used for request.data validation from SQL model.

    This is pretty important part of the code. This is the logic.

    If SQL model attribute is str, generates a list of strings.
    If SQL model attribute is str, generates a list of these enums.
    If SQL model attribute is number, generates two number attributes with
    "_min" and "_max" suffixes.

    In a better world, the ifs in the for cycle could be done in much more
    elegant way with creating a new class CarRecommenderField(sql_model.Field)"""

    fields = {}
    # get_type_hints returns attributes with their respective types
    type_hints = get_type_hints(model)

    for field_name, field_type in type_hints.items():
        # we add to query only attributes used for values storing
        # we do not search with respect to id
        if field_name == 'id':
            continue
        # we do not use type float, but its use would be the same as int -
        # we expect a lower and upper bound for the value
        elif field_type in [int, float]:
            fields[f"{field_name}_min"] = (Optional[field_type], None)
            fields[f"{field_name}_max"] = (Optional[field_type], None)
        # for a string we expect a list of strings
        elif field_type == str:
            fields[field_name] = (Optional[List[field_type]], None)
        # for an enum we expect a list of enum values
        elif isinstance(field_type, type) and issubclass(field_type, Enum):
            fields[field_name] = (Optional[List[field_type]], None)

    # creates a model with respective attributes and types for Pydantic
    return create_model('CarQuery', **fields)

def create_car_db_query(self):
    """Generates SQL Alchemy search query from data got in a body of the request.

    The logic of the creation is pretty similar to the generate_query_model function,
    because both of them depend on Car model, which is the bearer of the truth."""
    type_hints = get_type_hints(Car)
    query = select(Car)
    for field_name, field_type in type_hints.items():
        # we do not search with respect to id
        if field_name == 'id':
            continue
        # we do not use type float, but its use would be the same as int -
        # we expect a lower and upper bound for the value
        elif field_type in [int, float]:
            if (min_value := getattr(self, field_name + '_min')) is not None:
                query = query.where(getattr(Car, field_name) >= min_value)
            if (max_value := getattr(self, field_name + '_max')) is not None:
                query = query.where(getattr(Car, field_name) <= max_value)
        # for a string we expect a list of strings
        elif field_type == str:
            if (value := getattr(self, field_name)):
                like_conditions = [getattr(Car, field_name).like(f'%{name}%') for name in value]
                query = query.where(or_(*like_conditions))
        # for an enum we expect a list of enum values
        elif isinstance(field_type, type) and issubclass(field_type, Enum):
            if (value := getattr(self, field_name)):
                query = query.where(getattr(Car, field_name).in_(value))
    return query

# This is such an ugly code with respect to the beauty of the first idea
CarQuery = generate_query_model(Car)
CarQuery.create_car_db_query = create_car_db_query
