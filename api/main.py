from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import strawberry
from strawberry.asgi import GraphQL
from typing import List, Optional

from helpers import publicaciones_principales, publicaciones_secundarias
from entities import Publicacion
from utilities import map_dict_to_publicacion


@strawberry.input
class PublicacionInput:
    titulo: Optional[str] = None
    autor: Optional[str] = None
    categoria: Optional[str] = None
    publicada: Optional[bool] = None
    imagen_url: Optional[str] = None


# This Query class defines the GraphQL API, it is the root of the schema
# Defines what clients can query, defines the API
@strawberry.type
class Query:
    @strawberry.field
    def publicaciones(
        self, filtro: Optional[PublicacionInput] = None
    ) -> List[Publicacion]:
        data = publicaciones_principales + publicaciones_secundarias

        if filtro:
            for key, value in vars(filtro).items():
                if value is not None and value != "":
                    data = [
                        p
                        for p in data
                        if (
                            p[key] == value
                            or (
                                isinstance(p[key], str)
                                and value.lower() in p[key].lower()
                            )
                        )
                    ]

        return [map_dict_to_publicacion(p) for p in data]

    @strawberry.field
    def autores(self) -> List[str]:
        return list(
            set(
                [
                    p["autor"]
                    for p in publicaciones_principales + publicaciones_secundarias
                ]
            )
        )

    @strawberry.field
    def categorias(self) -> List[str]:
        return list(
            set(
                [
                    p["categoria"]
                    for p in publicaciones_principales + publicaciones_secundarias
                ]
            )
        )


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
