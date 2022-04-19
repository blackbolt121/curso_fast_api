from fastapi import FastAPI
#Contiene toda la aplicación
app = FastAPI()

@app.get("/")
async def home2():
    return {"Hello":"World"}

@app.get("/{user}")
async def home(user):
    return {"response":f"hello {user}"}
"""
 Para correr el programa es necesario hacer uso del comando
 uvicorn main:app --reload 
 El parametro --reload sirve para recargar el sitio en caso de
 que se haga un cambio en el archivo se recarge la ejecución de la
 API
"""
"""
Con la ruta http://{url}/docs
ejemplo
http://localhost:8000/docs
Muestra la documentancion de la API
Lo mismo se puede hacer con redoc
"""