import strawberry
from typing import List, Optional


@strawberry.type
class Publicacion:
    id: int
    titulo: str
    autor: str
    categoria: str
    descripcion: str
    publicada: bool
    etiquetas: List[str]
    imagen_url: Optional[str] = None
