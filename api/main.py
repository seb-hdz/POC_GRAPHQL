from fastapi import FastAPI
import strawberry
from strawberry.asgi import GraphQL
from typing import List, Optional


publicaciones_principales = [
    {
        "id": 1,
        "titulo": "Fundamentos de Estructuras de Datos",
        "autor": "Ana Torres",
        "categoria": "Estructuras de Datos",
        "fecha_publicacion": "2024-05-01",
        "descripcion": "Resumen completo con ejemplos en C++ y Python.",
        "etiquetas": ["listas", "árboles", "pilas", "colas"],
        "imagen_url": "/img/1.jpg",
        "publicada": True
    },
    {
        "id": 2,
        "titulo": "Arquitectura de Computadoras",
        "autor": "Luis Ríos",
        "categoria": "Arquitectura",
        "fecha_publicacion": "2024-05-03",
        "descripcion": "Esquemas de CPU, memoria caché y buses.",
        "etiquetas": ["cpu", "memoria", "mips"],
        "imagen_url": "/img/2.jpg",
        "publicada": True
    },
    {
        "id": 3,
        "titulo": "Redes de Computadoras - Guía práctica",
        "autor": "María Huamán",
        "categoria": "Redes",
        "fecha_publicacion": "2024-04-25",
        "descripcion": "Modelos OSI y TCP/IP con ejemplos de paquetes.",
        "etiquetas": ["tcp", "osi", "protocolos"],
        "imagen_url": "/img/3.jpg",
        "publicada": False
    },
    {
        "id": 4,
        "titulo": "Base de Datos - Apuntes para parciales",
        "autor": "Carlos Vega",
        "categoria": "Base de Datos",
        "fecha_publicacion": "2024-04-28",
        "descripcion": "Modelo relacional, álgebra relacional, SQL.",
        "etiquetas": ["sql", "relacional", "joins"],
        "imagen_url": "/img/4.jpg",
        "publicada": True
    },
    {
        "id": 5,
        "titulo": "Desarrollo Web con Flask",
        "autor": "Luis Ríos",
        "categoria": "Desarrollo Web",
        "fecha_publicacion": "2024-05-04",
        "descripcion": "Tutorial paso a paso para apps con Python.",
        "etiquetas": ["flask", "python", "web"],
        "imagen_url": "/img/5.jpg",
        "publicada": False
    },
    {
        "id": 6,
        "titulo": "Ingeniería de Requisitos - Ejemplos reales",
        "autor": "Ana Torres",
        "categoria": "Ingeniería de Software",
        "fecha_publicacion": "2024-05-10",
        "descripcion": "Casos de uso, historias de usuario, diagramas.",
        "etiquetas": ["requisitos", "uml", "casos_uso"],
        "imagen_url": "/img/6.jpg",
        "publicada": True
    },
    {
        "id": 7,
        "titulo": "Sistemas Operativos - Planificación de CPU",
        "autor": "María Huamán",
        "categoria": "Sistemas Operativos",
        "fecha_publicacion": "2024-05-11",
        "descripcion": "Algoritmos FCFS, SJF, RR explicados.",
        "etiquetas": ["cpu", "procesos", "planificación"],
        "imagen_url": "/img/7.jpg",
        "publicada": True
    }
]
publicaciones_secundarias = [
    {
        "id": 8,
        "titulo": "Resumen de Introducción a la Programación",
        "autor": "Ana Torres",
        "categoria": "Programación",
        "fecha_publicacion": "2024-03-21",
        "descripcion": "Variables, condicionales, bucles en C.",
        "etiquetas": ["c", "programación", "bucles"],
        "imagen_url": "/img/8.jpg",
        "publicada": True
    },
    {
        "id": 9,
        "titulo": "POO en Java - Conceptos Clave",
        "autor": "Luis Ríos",
        "categoria": "Programación",
        "fecha_publicacion": "2024-03-25",
        "descripcion": "Clases, objetos, herencia, interfaces.",
        "etiquetas": ["java", "poo", "herencia"],
        "imagen_url": "/img/9.jpg",
        "publicada": True
    },
    {
        "id": 10,
        "titulo": "Algoritmos de Búsqueda y Ordenamiento",
        "autor": "Carlos Vega",
        "categoria": "Estructuras de Datos",
        "fecha_publicacion": "2024-03-30",
        "descripcion": "Bubble sort, quicksort, búsqueda binaria.",
        "etiquetas": ["ordenamiento", "búsqueda"],
        "imagen_url": "/img/10.jpg",
        "publicada": False
    },
    {
        "id": 11,
        "titulo": "SQL Básico en 2 páginas",
        "autor": "María Huamán",
        "categoria": "Base de Datos",
        "fecha_publicacion": "2024-04-01",
        "descripcion": "Selects, joins, agrupaciones rápidas.",
        "etiquetas": ["sql", "select", "join"],
        "imagen_url": "/img/11.jpg",
        "publicada": True
    },
    {
        "id": 12,
        "titulo": "Apuntes de Modelado UML",
        "autor": "Ana Torres",
        "categoria": "Ingeniería de Software",
        "fecha_publicacion": "2024-04-03",
        "descripcion": "Diagrama de clases, secuencia, actividades.",
        "etiquetas": ["uml", "modelado"],
        "imagen_url": "/img/12.jpg",
        "publicada": True
    },
    {
        "id": 13,
        "titulo": "Concurrencia y Deadlocks",
        "autor": "Carlos Vega",
        "categoria": "Sistemas Operativos",
        "fecha_publicacion": "2024-04-06",
        "descripcion": "Condiciones de Coffman, prevención.",
        "etiquetas": ["deadlock", "concurrencia"],
        "imagen_url": "/img/13.jpg",
        "publicada": True
    },
    {
        "id": 14,
        "titulo": "Notas de Seguridad Informática",
        "autor": "Luis Ríos",
        "categoria": "Seguridad",
        "fecha_publicacion": "2024-04-09",
        "descripcion": "Autenticación, hash, ataques comunes.",
        "etiquetas": ["seguridad", "hash", "csrf"],
        "imagen_url": "/img/14.jpg",
        "publicada": False
    }
]


@strawberry.type
class Publicacion:
    id: int
    titulo: str
    autor: str
    categoria: str
    descripcion: str
    publicada: bool
    etiquetas: List[str]

@strawberry.input
class PublicacionInput:
    autor: Optional[str] = None
    categoria: Optional[str] = None
    publicada: Optional[bool] = None


@strawberry.type
class Movie:
    title: str
    director: str

# This Query class defines the GraphQL API, it is the root of the schema
# Defines what clients can query, defines the API  
@strawberry.type
class Query:
    @strawberry.field
    def movies(self) -> List[Movie]:
        # Fetch movies from a data source (e.g., database, API)
        movies_data = [
            Movie(title="Inception", director="Christopher Nolan"),
            Movie(title="The Matrix", director="Lana Wachowski, Lilly Wachowski"),
            Movie(title="Interstellar", director="Christopher Nolan"),
            Movie(title="The Shawshank Redemption", director="Frank Darabont"),
            Movie(title="The Godfather", director="Francis Ford Coppola"),
        ]
        return movies_data
    
    @strawberry.field
    def publicaciones(self, filtro: Optional[PublicacionInput] = None) -> List[Publicacion]:
        data = publicaciones_principales + publicaciones_secundarias

        if filtro:
            if filtro.autor:
                data = [p for p in data if p["autor"] == filtro.autor]
            if filtro.categoria:
                data = [p for p in data if p["categoria"] == filtro.categoria]
            if filtro.publicada is not None:
                data = [p for p in data if p["publicada"] == filtro.publicada]

        return [map_dict_to_publicacion(p) for p in data]

    
def map_dict_to_publicacion(data: dict) -> Publicacion:
    return Publicacion(
        id=data["id"],
        titulo=data["titulo"],
        autor=data["autor"],
        categoria=data["categoria"],
        descripcion=data["descripcion"],
        publicada=data["publicada"],
        etiquetas=data["etiquetas"]
    )

    if filtro:
        if filtro.autor:
            data = [p for p in data if p["autor"] == filtro.autor]
        if filtro.categoria:
            data = [p for p in data if p["categoria"] == filtro.categoria]
        if filtro.publicada is not None:
            data = [p for p in data if p["publicada"] == filtro.publicada]

    return [map_dict_to_publicacion(p) for p in data]

schema = strawberry.Schema(query=Query)
app = FastAPI()

@app.get("/")
def index():
    return {"message": "Welcome to the Movie API!"}

app.add_route("/graphql", GraphQL(schema, debug=True)) 
