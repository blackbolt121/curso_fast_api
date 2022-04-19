#Python
from typing import Optional
#Pydantic
from pydantic import BaseModel
#FASTAPI
from fastapi import FastAPI, Query, Body, Path
#Contiene toda la aplicación
app = FastAPI()

#Creamos un modelo
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_single: Optional[bool] = None

@app.get("/")
async def home2():
    return {"Hello":"World"}

@app.get("/hello/{user}")
async def home(user):
    return {"response":f"hello {user}"}
#Los tres puntos significa que el parametro es obligatorio
@app.post("/person/new")
async def create_person(person: Person = Body(...)):
    return person
#Validaciones: Query Parameters
@app.get("/person/detail")
async def show_person(
    name: Optional[str] = Query
    (None,
     min_length=1,
     max_length=50,
     title="Person Name",
     description="This is the person name. It's between 1 and 50 characters"),
    age: str = Query(
        ...,
        title="Person age",
        description="This is the person age. It's required"
        )
):
    return {name:age}
@app.get("/saludar")
async def saludar(
    name: str = Query(
        ...,
        min_length=2,
        max_length=50,
        title="This is the name of the preson",
        description="it's name length must be between 2 and 50 characters"
        ),
    edad: Optional[int] = Query(
        20,
        le=100,
        gt=1,
        title="Age parameter",
        description="Here you put the age of the person, it must be between 1 and 100"
        )
):
    return {"saludo":f"Hola {name}, tines {edad}"}
@app.get("(person/detail/{person_id}")
async def show_person_by_id(
    person_id: int = Path(...,ge=1)
    ):
    return {person_id: "exists"}