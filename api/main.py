from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import strawberry
from strawberry.asgi import GraphQL
from typing import List, Optional
import sqlite3

from entities import Publicacion
from utilities import map_dict_to_publicacion


def get_db_connection():
    conn = sqlite3.connect("publicaciones.db")
    conn.row_factory = sqlite3.Row
    return conn


@strawberry.input
class PublicacionInput:
    titulo: Optional[str] = None
    autor: Optional[str] = None
    categoria: Optional[str] = None
    publicada: Optional[bool] = None
    imagen_url: Optional[str] = None


@strawberry.type
class Query:
    @strawberry.field
    def publicaciones(
        self, filtro: Optional[PublicacionInput] = None
    ) -> List[Publicacion]:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Base query to get all publications with author and category names
        query = """
            SELECT 
                p.id,
                p.titulo,
                a.nombre as autor,
                c.nombre as categoria,
                p.fecha_publicacion,
                p.descripcion,
                p.imagen_url,
                p.publicada,
                GROUP_CONCAT(e.nombre) as etiquetas
            FROM publicaciones p
            JOIN autores a ON p.autor_id = a.id
            JOIN categorias c ON p.categoria_id = c.id
            LEFT JOIN publicacion_etiquetas pe ON p.id = pe.publicacion_id
            LEFT JOIN etiquetas e ON pe.etiqueta_id = e.id
        """

        params = []
        where_clauses = []

        if filtro:
            if filtro.titulo:
                where_clauses.append("p.titulo LIKE ?")
                params.append(f"%{filtro.titulo}%")
            if filtro.autor:
                where_clauses.append("a.nombre LIKE ?")
                params.append(f"%{filtro.autor}%")
            if filtro.categoria:
                where_clauses.append("c.nombre LIKE ?")
                params.append(f"%{filtro.categoria}%")
            if filtro.publicada is not None:
                where_clauses.append("p.publicada = ?")
                params.append(filtro.publicada)
            if filtro.imagen_url:
                where_clauses.append("p.imagen_url LIKE ?")
                params.append(f"%{filtro.imagen_url}%")

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        query += " GROUP BY p.id ORDER BY p.id"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        # Convert rows to dictionaries and split etiquetas string into list
        publicaciones = []
        for row in rows:
            pub_dict = dict(row)
            pub_dict["etiquetas"] = (
                pub_dict["etiquetas"].split(",") if pub_dict["etiquetas"] else []
            )
            publicaciones.append(pub_dict)

        return [map_dict_to_publicacion(p) for p in publicaciones]

    @strawberry.field
    def autores(self) -> List[str]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM autores ORDER BY nombre")
        autores = [row["nombre"] for row in cursor.fetchall()]
        conn.close()
        return autores

    @strawberry.field
    def categorias(self) -> List[str]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM categorias ORDER BY nombre")
        categorias = [row["nombre"] for row in cursor.fetchall()]
        conn.close()
        return categorias


schema = strawberry.Schema(query=Query)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"message": "GraphQL PoC"}


app.add_route("/graphql", GraphQL(schema, debug=True))
