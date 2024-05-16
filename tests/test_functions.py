import random
from typing import List

from Bot import functions as fe
from Bot.functions import Sentence


def generate_dummy_coords(num_coords) -> List[List[int]]:
    dummy_coords = []
    for _ in range(num_coords):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        coord = [x, y]
        dummy_coords.append(coord)
    return dummy_coords


def test_that_get_random_coord_always_return_a_new():
    coords = generate_dummy_coords(10)
    last_coord = None
    for _ in range(1000):
        coord = fe.get_random_coord(coords)
        assert coord != last_coord
        last_coord = coord


def test_get_asteroids():
    sentences = [
        Sentence(
            word="6982 m Asteroid (Veldsp Velc",
            x=1152,
            y=353,
            w=252,
            h=16,
            c_x=1278.0,
            c_y=361.0,
        ),
        Sentence(
            word="7092 m Asteroid (Scordi Sco",
            x=1152,
            y=383,
            w=252,
            h=16,
            c_x=1278.0,
            c_y=391.0,
        ),
        Sentence(
            word="7256 m Asteroid (Scordi Sco",
            x=1152,
            y=413,
            w=252,
            h=16,
            c_x=1278.0,
            c_y=421.0,
        ),
        Sentence(
            word="726m Asteroid (Scordi Sco",
            x=1152,
            y=443,
            w=252,
            h=16,
            c_x=1278.0,
            c_y=451.0,
        ),
        Sentence(
            word="7478 m Asteroid (Conce Con",
            x=1152,
            y=503,
            w=252,
            h=16,
            c_x=1278.0,
            c_y=511.0,
        ),
        Sentence(
            word="77122 m Asteroid (Dense Den",
            x=1152,
            y=533,
            w=252,
            h=16,
            c_x=1278.0,
            c_y=541.0,
        ),
        Sentence(
            word="779% m Asteroid (Sconi sco",
            x=1152,
            y=563,
            w=252,
            h=16,
            c_x=1278.0,
            c_y=571.0,
        ),
        Sentence(
            word="7844 m Asteroid (Dense Den",
            x=1152,
            y=593,
            w=252,
            h=16,
            c_x=1278.0,
            c_y=601.0,
        ),
        Sentence(
            word="8047 m Asteroid (Veldsp Velc",
            x=1152,
            y=653,
            w=252,
            h=16,
            c_x=1278.0,
            c_y=661.0,
        ),
        Sentence(
            word="--® ~~ 8896 m Asteroid (Conde Con",
            x=1044,
            y=684,
            w=360,
            h=19,
            c_x=1224.0,
            c_y=693.5,
        ),
        Sentence(
            word="8271 m Asteroid (Veldsp Velc",
            x=1152,
            y=713,
            w=252,
            h=16,
            c_x=1278.0,
            c_y=721.0,
        ),
    ]

    roids = fe.get_asteroids(sentences)

    assert len(roids) == 11

    assert roids[0].word == "6982 m Asteroid (Veldsp Velc"
    assert roids[1].word == "7092 m Asteroid (Scordi Sco"
