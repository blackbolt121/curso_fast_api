#GUIA DE FASTAPI
##¿Como iniciar una API desde un archivo py?
Para correr el programa es necesario hacer uso del comando

>**uvicorn main:app --reload**

El parametro --reload sirve para recargar el sitio en caso de que se haga un cambio en el archivo se recarge la ejecución de la API

##¿Como visualizar la documentación de la API?
Con la ruta http://{url}/docs
ejemplo
http://localhost:8000/docs
Muestra la documentancion de la API 
Se puede hacer lo mismo con redoc
http://{url}/redoc

##La clase optional
La clase optional es importante para determinar el tipo del modelo es opcional.
Se importa desde la libreria typing
<pre>
<code>
    from typing import Optional
</code>
</pre>
**En caso de necesitar colocarlo en el modelo se coloca como
<pre>
<code>
    Optional[type]
</code>
</pre>
##Consulta más documentación aquí
>1.https://www.markdownguide.org/basic-syntax/
>2.https://hackmd.io/@duvanbotello/rk8vjxCrt

##Validaciones con Query
Con Query podemos agregar parametros en la URL de nuestra API
Para las validaciones al menos hay para string e integers, además podemos definir si son obligatorios o no pasando dentro del constructor los ... (obligatorio),
o None o valor predeterminado (No obligatorio)

>#Ejemplo
>`
>   @app.get("/saludar")
>   def saludar(
>    nombre: string=Query(...),
>    edad: Optional[int] = Query(20)
>    )
>   
>`
Adicionalmente dentro de los Query podemos agregar parametros para filtrar, entre esos parametros son
###Cadenas
-max_length: Defines el tamaño maximo
-min_length: ..... mínimo
-regex: Defines el tipo de cadena por una expresion regular
###Numerico
-ge: Condición para que el numero no sea mayor o igual
-le: Condición para que el numero no sea menor o igual
-gt: Condición para que el numero no sea extrictamente mayor
-lt: Condicion para que el numero no sea extrictamente menor
