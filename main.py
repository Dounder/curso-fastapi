#  Python
from enum import Enum
from typing import Dict, Optional
# Pydantic
from pydantic import BaseModel, Field, SecretStr
# FastApi
from fastapi import FastAPI, Body, Form, Path, Query, status

#  Instancia de la clase.
app: FastAPI = FastAPI()


class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'


class Location(BaseModel):
    city: str = Field(..., example='Guatemala')
    state: str = Field(..., example='Guatemala')
    country: str = Field(..., example='GT')


class Person(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, example='Alex')
    last_name: str = Field(..., min_length=1, max_length=50, example='Ramirez')
    age: int = Field(..., gt=0, lt=115, example=21)
    hair_color: Optional[HairColor] = Field(default=None, example='black')
    is_married: Optional[bool] = Field(default=None, example=False)
    password: SecretStr = Field(..., min_length=8, example='12345678')


class Login(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: SecretStr = Field(..., min_length=8)
    message: str = Field(
        default='Login successful :3',
        description='User loged in'
    )


@app.get("/", status_code=status.HTTP_200_OK)  # Path Operator Decoration.
def home() -> Dict:  # Path operator function
    return {"Hello": "World"}  # Return JSON.


# Request and Response body
@app.post(
    '/person/new',
    response_model=Person,
    response_model_exclude={'password'},
    status_code=status.HTTP_201_CREATED
)
def create_person(person: Person = Body(...)):
    return person


# Validaciones query parameters
@app.get('/person/detail', status_code=status.HTTP_200_OK)
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title='Person name',
        description='This is the person name. It\'s between 1 and 50 characters',
        example='Juan'
    ),
    age: str = Query(
        ...,
        title='Person age',
        description='This is the person name. It\'s required',
        example=30
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
        description='This is the person id. It\'s required and value is greater than 0',
        example=123
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
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    location: Location = Body(...),
):
    result = person.dict()
    result.update(location.dict())
    return result


@app.post(
    path='/login',
    response_model=Login,
    response_model_exclude={'password'},
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return Login(username=username, password=password)
