#Python
from typing import Optional
#Pydantic
from pydantic import BaseModel
#FASTAPI
from fastapi import FastAPI, Query, Body
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
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    age: str = Query(...,)

):
    return {name:age}
@app.get("/saludar")
async def saludar(
    name: str = Query(...,min_length=2,max_length=50),
    edad: Optional[int] = Query(20,le=100, gt=1)
):
    return {"saludo":f"Hola {name}, tines {edad}"}