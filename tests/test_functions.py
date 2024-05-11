import random
from typing import List

from Bot import functions as fe


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
