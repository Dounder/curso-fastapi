#  Python
from enum import Enum
from typing import Dict, Optional
# Pydantic
from pydantic import BaseModel, Field
# FastApi
from fastapi import FastAPI, Body, Path, Query

#  Instancia de la clase.
app: FastAPI = FastAPI()


class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        lt=115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)


class Location(BaseModel):
    city: str
    state: str
    country: str


@app.get("/")  # Path Operator Decoration.
def home() -> Dict:  # Path operator function
    return {"Hello": "World"}  # Return JSON.


# Request and Response body
@app.post('/person/new')
def create_person(person: Person = Body(...)):
    return person


# Validaciones query parameters
@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title='Person name',
        description='This is the person name. It\'s between 1 and 50 characters'
    ),
    age: str = Query(
        ...,
        title='Person age',
        description='This is the person name. It\'s required'
    ),
):
    return {name: age}


# Validaciones: path parameters
@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title='Person id',
        description='This is the person id. It\'s required and value is greater than 0'
    )
):
    return {person_id: 'it exists'}


# Validaciones: Request body
@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        title='Person Id',
        description='This is the person id',
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...),
):
    result = person.dict()
    result.update(location.dict())
    return result
