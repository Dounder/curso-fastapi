#  Python
from typing import Dict, Optional
# Pydantic
from pydantic import BaseModel
# FastApi
from fastapi import FastAPI, Body, Query

#  Instancia de la clase.
app: FastAPI = FastAPI()


class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


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
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    age: str = Query(...),
):
    return {name: age}
