from fastapi import FastAPI,Body
from fastapi.responses import HTMLResponse
#Basemodel no ayuda a modelar los schemas 
from pydantic import BaseModel
#para poner campos opcionales
from typing import Optional


app = FastAPI()
app.title = "Mi apliacion con FastApi"
app.version="0.0.1"

class Movie(BaseModel):
    id: Optional[int] = None
    title: str
    overview:str
    year:int
    rating:float
    category:str

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Acción'    
    } ,
    {
        'id': 2,
        'title': 'fast and furius',
        'overview': "carrrrrrrros...",
        'year': 2009,
        'rating': 1.0,
        'category': 'Acción'    
    } 
]

@app.get("/" ,tags =["Home"])
def message():
    return HTMLResponse( "<h1>Hola Santiago<h1>")


@app.get('/movies', tags=['movies'])
def get_movies():
    return movies


# @app.get("/movies/{id},tags=['movies']")
# def get_movie(id:int):
#     for i in movies:
#         if i['id'] ==id:
#             return i
#     return id

# con lambda function ------->
# La comprensión de lista es la siguiente:


# [movie for movie in movies if movie['id'] == movie_id][0]
# Donde:

# movie: es el valor que se agregará a la nueva lista, en este caso, cada elemento de movies que cumpla con la condición.
# movie for movie in movies: es la variable que se utiliza para iterar sobre la lista original.
# movies: es la lista original de películas.
# if movie['id'] == movie_id: es la condición que se utiliza para filtrar la lista original. Solo se agregarán a la nueva lista aquellos elementos cuyo ID (id) coincida con el ID de la película proporcionado (movie_id).
# [0]: después de la comprensión de lista, se agrega [0] para devolver el primer elemento de la lista (si existe).
# En resumen, esta comprensión de lista se utiliza para buscar una película específica en una lista de películas y devolver su información. Si la película correspondiente se encuentra, se devuelve como resultado de la función read_movie(). Si la lista de películas está vacía o no se puede encontrar una película con el ID proporcionado, se genera una excepción IndexError.


@app.get(
    "/movies/{movie_id}",
    tags=["Movies"])
def read_movie(movie_id: int):
    try:
        return [ movie for movie in movies if movie['id'] == movie_id][0]
    except IndexError:
        return {"error": "Movie not found"}
    
@app.get('/movies/' ,tags=['movies'])
def get_movies_by_category(category:str):
    return list(filter(lambda i :i['category']==category, movies )) 

@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie.dict())
    return movies

@app.delete('/movies/{movie_id}',tags=["movies"])
def delete_movie(movie_id:int):
     for i in movies:
         if i["id"] == movie_id:
             movies.remove(i)
             return movies
         
@app.put('/movies/{movie_id}',tags=["movies"])
def update_movie(id: int ,movie:Movie):
    for i in movies:
        if i['id'] == id:
            i['title'] = movie.title
            i['overview'] = movie.overview
            i['year'] = movie.year
            i['rating'] = movie.rating
            i['category'] = movie.category
            return movies
        

