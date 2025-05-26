import sqlite3
from datetime import datetime
from helpers import publicaciones_principales, publicaciones_secundarias


def setup_database():
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect("publicaciones.db")
    cursor = conn.cursor()

    # Create authors table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS autores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL
    )
    """
    )

    # Create categories table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL
    )
    """
    )

    # Create publications table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS publicaciones (
        id INTEGER PRIMARY KEY,
        titulo TEXT NOT NULL,
        autor_id INTEGER,
        categoria_id INTEGER,
        fecha_publicacion TEXT,
        descripcion TEXT,
        imagen_url TEXT,
        publicada BOOLEAN,
        FOREIGN KEY (autor_id) REFERENCES autores (id),
        FOREIGN KEY (categoria_id) REFERENCES categorias (id)
    )
    """
    )

    # Create tags table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS etiquetas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL
    )
    """
    )

    # Create publication_tags junction table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS publicacion_etiquetas (
        publicacion_id INTEGER,
        etiqueta_id INTEGER,
        PRIMARY KEY (publicacion_id, etiqueta_id),
        FOREIGN KEY (publicacion_id) REFERENCES publicaciones (id),
        FOREIGN KEY (etiqueta_id) REFERENCES etiquetas (id)
    )
    """
    )

    # Insert authors
    autores = set()
    for pub in publicaciones_principales + publicaciones_secundarias:
        autores.add(pub["autor"])

    for autor in autores:
        cursor.execute("INSERT OR IGNORE INTO autores (nombre) VALUES (?)", (autor,))

    # Insert categories
    categorias = set()
    for pub in publicaciones_principales + publicaciones_secundarias:
        categorias.add(pub["categoria"])

    for categoria in categorias:
        cursor.execute(
            "INSERT OR IGNORE INTO categorias (nombre) VALUES (?)", (categoria,)
        )

    # Insert publications
    for pub in publicaciones_principales + publicaciones_secundarias:
        # Get autor_id
        cursor.execute("SELECT id FROM autores WHERE nombre = ?", (pub["autor"],))
        autor_id = cursor.fetchone()[0]

        # Get categoria_id
        cursor.execute(
            "SELECT id FROM categorias WHERE nombre = ?", (pub["categoria"],)
        )
        categoria_id = cursor.fetchone()[0]

        # Insert publication
        cursor.execute(
            """
        INSERT OR IGNORE INTO publicaciones 
        (id, titulo, autor_id, categoria_id, fecha_publicacion, descripcion, imagen_url, publicada)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                pub["id"],
                pub["titulo"],
                autor_id,
                categoria_id,
                pub["fecha_publicacion"],
                pub["descripcion"],
                pub["imagen_url"],
                pub["publicada"],
            ),
        )

        # Insert tags
        for etiqueta in pub["etiquetas"]:
            cursor.execute(
                "INSERT OR IGNORE INTO etiquetas (nombre) VALUES (?)", (etiqueta,)
            )
            cursor.execute("SELECT id FROM etiquetas WHERE nombre = ?", (etiqueta,))
            etiqueta_id = cursor.fetchone()[0]

            cursor.execute(
                """
            INSERT OR IGNORE INTO publicacion_etiquetas (publicacion_id, etiqueta_id)
            VALUES (?, ?)
            """,
                (pub["id"], etiqueta_id),
            )

    # Commit changes and close connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    setup_database()
