# Python
from os import stat
from typing import Optional
from enum import Enum
from hashlib import md5
from unicodedata import category
# Pydantic
from pydantic import BaseModel, ValidationError, EmailStr
# Esta clase nos sirve para agregar validaciones a un cuerpo
from pydantic import Field
# FASTAPI
from fastapi import Cookie, FastAPI, File, Header, Query, Body, Path, UploadFile, status, Form, HTTPException
# Contiene toda la aplicación
app = FastAPI()

# Enums
# Definimos un enum para limitar el tipo de string que puede recibir nuestra clase


class HairColor(Enum):
    white = "white"
    red = "red"
    brown = "brown"
    blonde = "blonde"
    black = "black"

# Creamos un modelo


class Person(BaseModel):
    first_name: str = Field(...,
                            min_length=1,
                            max_length=50)
    last_name: str = Field(...,
                           min_length=1,
                           max_length=50)
    age: int = Field(
        ...,
        gt=0,
        lt=100
    )
    hair_color: Optional[HairColor] = Field(
        default=None
    )
    is_single: Optional[bool] = Field(
        default=True
    )
    email: Optional[EmailStr] = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Rodrigo",
                "last_name": "Lopez",
                "age": 21,
                "hair_color": "black",
                "is_single": True
            }
        }


"""
Con este modelo creamos un objeto de respuesta
"""


class PersonOut(BaseModel):
    person_id: int = Field(..., gt=1)
    first_name: str = Field(...,
                            min_length=1,
                            max_length=50)
    last_name: str = Field(...,
                           min_length=1,
                           max_length=50)
    age: int = Field(
        ...,
        gt=0,
        lt=100
    )
    city: str
    state: str
    country: str


class Location(BaseModel):
    city: str
    state: str
    country: str

    class config:
        schema_extra = {
            "example": {
                "city": "Corregidora",
                "state": "Queretaro",
                "country": "Mexico"
            }
        }


class User(BaseModel):
    email: EmailStr = Field(..., example="rgo1999@hotmail.com")
    password: str = Field(..., min_length=1)

    class config:
        schema_extra = {
            "example": {
                "email": "email@example.com",
                "password": "super_pa$$word"
            }
        }


"""
Con el framework FASTAPI, disponemos del objeto status
En el podemos indicarle el codigo de estatus de la petición desde nuestro
path function decorator de manera personalizada. Por defecto dependiendo del
VERBO HTTP, coloca el codigo adecuado, sin embargo con esto podemos personalizarlo
"""


@app.get(
    path="/",
    status_code=status.HTTP_200_OK
)
async def home2():
    return {"Hello": "World"}
"""
Tanto para path y query existe la opción de agregar ejemplos, y en la misma
documentación de la api (docs), aparecera el valor puesto de ejemplo
"""


@app.get("/hello_world/{user}")
async def home(user: str = Path(..., min_length=1, example="World")):
    return {"hello": f"{user}"}
# Los tres puntos significa que el parametro es obligatorio


@app.post("/person/new")
async def create_person(person: Person = Body(...)):
    return person
# Validaciones: Query Parameters


@app.get("/person/detail")
async def show_person(
    name: Optional[str] = Query
    (None,
     min_length=1,
     max_length=50,
     title="Person Name",
     description="This is the person name. It's between 1 and 50 characters",
     example="Jose"),
    age: str = Query(
        ...,
        title="Person age",
        description="This is the person age. It's required",
        example=14
    )
):
    return {name: age}


@app.get("/saludar")
async def saludar(
    name: str = Query(
        ...,
        min_length=2,
        max_length=50,
        title="This is the name of the preson",
        description="it's name length must be between 2 and 50 characters",
        example="Javier"
    ),
    edad: Optional[int] = Query(
        20,
        le=100,
        gt=1,
        title="Age parameter",
        description="Here you put the age of the person, it must be between 1 and 100",
        example=10
    )
):
    return {"saludo": f"Hola {name}, tines {edad}"}


@app.get("(person/detail/{person_id}")
async def show_person_by_id(
    person_id: int = Path(..., ge=1)
):
    return {person_id: "exists"}


@app.put("/person/{person_id}", response_model=PersonOut)
async def update_person(
    person_id: int = Path
    (..., gt=0, title="Here you put the id of the person", description="The id of the person must be greater than 0", example=777),
    person: Person = Body(...),
        location: Location = Body(...)):
    data = {**dict(person), **dict(location)}
    data["person_id"] = person_id
    data["adicional"] = "jajajas"
    return data


@app.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=User,
    response_model_exclude=("password",)
)
def login(
    _email: EmailStr = Form(...,
                            example="hello@world.com"
                            ),
    _password: str = Form(...,
                          min_length=8,
                          example="supa_p4$$w0rd"
                          )
):
    log = User(email=_email, password=_password)
    print(_password)
    return log


@app.post(
    path="/contact",
    status_code=status.HTTP_202_ACCEPTED
)
def contact(
    nombre: str = Form(
        ...,
        min_length=1,
        max_length=20,
        title="First Name",
        description="Here you put your name",
        example="Gabriela"
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
        title="Last Name",
        description="You have to especify your last name",
        example="Santana",
    ),
    email: EmailStr = Form(...,
                           description="Put your email here",
                           example="email@example.com"),
    message: str = Form(
        ...,
        min_length=20,
        max_length=200,
        description="Please, enter a message",
        example="You can put any message here"),
    user_agent: Optional[str] = Header(default=None),
    content_type: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return {0:[user_agent,content_type, ads]}
@app.post(
    path="/post-image",
    description="Sube imagenes desde esta URL"
)
def postImage(image : UploadFile = File(...)):
    
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": image.file.read().__len__()
    }
@app.post(
    "/exist/{user}",
    name="Agrega usuario", #Podemos agregarle un nombre a la ruta de la API en la documentación
    tags=["User"]#, #Podemos añadir etiquetas a nuestra API para hacer que en la documentación este categorizada
    #description="Valida la existencia de un usuario con esta ruta" #Podemos añadir descripciones a las rutas de nuestra API
    )
def userExists(user: int = Path(
    ...,
    gt=0,
    description="Aquí va el id de usuario",
    example=5
    )
):
    """
    # Un titulo impresionante #
    
    >Hola, con **FastAPI** podemos agregar documentación con MarkDown simplemente utilizando
    un comentario de lineas multiples con _triple_ _\"_ 
    """
    available_users = [1,2,3,4,5]
    if(user in available_users):
        return {int(user) :"User found"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found") #Es importante definir excepciones en caso de que un parametro sea invalida y sale de las validaciones