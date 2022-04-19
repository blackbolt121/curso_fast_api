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
"""