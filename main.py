from abc import ABCMeta
from dataclasses import dataclass
from typing import List, Optional

import numpy as np


@dataclass
class Point:
    x: int
    y: int


class Actor(ABCMeta):
    def __init__(self, position: Point, name: str):
        self.position = position
        self.name = name
    
    def __mul__(self, other):
        collision = self.position == other.position
        return collision
    

class Board:
    def __init__(self):
        self.content = self._zero_board()
        self.forbidden_because_board_is_not_rectangle = [
            (0, 0), (0, 3), (0, 4),
            # this row is full 
            # this row is full
            # this row is full
            (4, 20)
        ]
    
    def _zero_board(self):
        self.content = np.array([
            [0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0,],
            [0, 0, 0, 0, 0,]
        ])

    def update(self, actors: List[Actor]):
        self.content = self._zero_board()
        for actor in actors:
            self.content[*actor.position] = actor.name


# Abstract matrix that is used for defining house
# Since house is a block of irregular (but coherent) shape 
# it could be represented by 1's in that TILES matrix
TILES = np.array([
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0
])

SAMPLE_TILES_STICK = [
    1, 1, 1, 1,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0
]  # tiles = 0, 1, 2, 3

SAMPLE_TILES_GUN = [
    1, 1, 1, 0,
    1, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0
]  # tiles = 0, 1, 2, 4

SAMPLE_TILES_CORNER = [
    1, 1, 0, 0,
    1, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0
]  # tiles = 0, 1, 4 


class House:
    def __init__(self, tiles: List[int]):
        self.tiles = TILES
        self.tiles[tiles] = 1

    def __mul__(self, other):
        collision = np.sum(np.dot(self, other)) > 0
        return collision


class Pig(Actor):
    def __init__(self, position: Point, house: Optional[House]):
        super().__init__(position)
        self.house = house

    def __mul__(self, other):
        collision = super().__mul__(other)
        if not collision:
            assert (self.house is None and other.house is None) \
                or (self.house is not None and other.house is not None)
            if self.house is not None and other.house is not None:
                return self.house * other.house
            else:
                return False
        else:
            return True
        


class Wolf(Actor):
    def __init__(self, position):
        super().__init__(position)


def get_config():
    config = {}
    config["pigs"] = [
        Pig(
            Point(0, 1)
        )
    ]


def run(*kwargs):
    pigs: List[Pig] = kwargs["pigs"]
    wolf = kwargs["wolf"]



if __name__ == "__main__":
    config = get_config()
    run(**config)