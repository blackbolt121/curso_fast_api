#Python
from typing import Optional
#Pydantic
from pydantic import BaseModel
#FASTAPI
from fastapi import FastAPI
from fastapi import Body
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

@app.get("/{user}")
async def home(user):
    return {"response":f"hello {user}"}

#Los tres puntos significa que el parametro es obligatorio
@app.post("/person/new")
async def create_person(person: Person = Body(...)):
    return person