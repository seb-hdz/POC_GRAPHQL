from fastapi import FastAPI
import strawberry
from strawberry.asgi import GraphQL
from typing import List


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
    
schema = strawberry.Schema(query=Query)
app = FastAPI()

@app.get("/")
def index():
    return {"message": "Welcome to the Movie API!"}

app.add_route("/graphql", GraphQL(schema, debug=True)) 
