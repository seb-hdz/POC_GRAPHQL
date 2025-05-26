from entities import Publicacion


def map_dict_to_publicacion(data: dict) -> Publicacion:
    return Publicacion(
        id=data["id"],
        titulo=data["titulo"],
        autor=data["autor"],
        categoria=data["categoria"],
        descripcion=data["descripcion"],
        publicada=data["publicada"],
        etiquetas=data["etiquetas"],
        imagen_url=data["imagen_url"],
    )
