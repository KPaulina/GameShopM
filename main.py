from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
import os

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)
redis = get_redis_connection(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True,
)


class Games (HashModel):
    name: str
    price: float
    genre: str

    class Meta:
        datebase = redis


@app.get('/games')
def all():
    return [format(pk) for pk in Games.all_pks()]


def format(pk: str):
    game = Games.get(pk)
    return {
        'id': game.pk,
        'name': game.name,
        'price': game.price,
        'genre': game.genre
    }


@app.post('/games')
def create(game: Games):
    return game.save()


@app.get('games/{pk}')
def get(pk: str):
    return Games.get(pk)