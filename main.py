from abc import ABCMeta
from dataclasses import dataclass
from enum import Enum, IntEnum
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
    
    def __repr__(self):
        return f"{self.name=}, {self.position=}"
    
    def __str__(self):
        return self.__repr__()


class ActorPositionNotOnBoardException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


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
            if any(
                actor.position == f
                   for f in self.forbidden_because_board_is_not_rectangle
            ):
                raise ActorPositionNotOnBoardException(f"{actor=}")
            self.content[*actor.position] = actor.name


class Orientation(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


# Abstract matrix that is used for defining house
# Since house is a block of irregular (but coherent) shape 
# it could be represented by 1's in that TILES matrix
TILES = np.array([
    [0, 0, 0, 0, 0,]
    [0, 0, 0, 0, 0,]
    [0, 0, 0, 0, 0,]
    [0, 0, 0, 0, 0,]
    [0, 0, 0, 0, 0,]
])

MIDDLE_TILE = Point(*(s // 2 for s in TILES.shape))

class House:
    def __init__(self, tiles: List[Point], position_of_center_of_the_tiles_on_board: Point):
        self.tiles = TILES
        for t in tiles:
            self.tiles[t + MIDDLE_TILE] = 1
        self.orientation = Orientation.RIGHT
        self.position_of_center_of_the_tiles_on_board \
            = position_of_center_of_the_tiles_on_board

    @staticmethod
    def _fill_big_abstract_board(house, big_abstract_board):
        abstract_start_point_of_game_board = Point(20, 20)
        position_on_big \
             = abstract_start_point_of_game_board \
                + house.position_of_center_of_the_tiles_on_board
        point_start = position_on_big - MIDDLE_TILE
        point_end = position_on_big + MIDDLE_TILE
        big_abstract_board[
            point_start.x : point_end.x,
            point_start.y : point_end.y,
        ] = house.tiles
        return big_abstract_board

    def __mul__(self, other):
        big_abstract_board_self = np.zeros((100, 100))
        big_abstract_board_self = self._fill_big_abstract_board(self, big_abstract_board_self) 
        
        big_abstract_board_other = np.zeros((100, 100))
        big_abstract_board_other = self._fill_big_abstract_board(other, big_abstract_board_other) 
        
        collision = np.sum(np.dot(big_abstract_board_self, big_abstract_board_other)) > 0
        return collision

    def flip(self):
        new_val = (self.orientation + 1) % len(Orientation)
        self.orientation = Orientation(new_val)


STICK_HOUSE = House([
    Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3),
])
# [
#     1, 1, 1, 1,
#     0, 0, 0, 0,
#     0, 0, 0, 0,
#     0, 0, 0, 0
# ]

GUN_HOUSE = House([
    Point(0, 0), Point(0, 1), Point(0, 2),
    Point(1, 0),
]) 
# [
#     1, 1, 1, 0,
#     1, 0, 0, 0,
#     0, 0, 0, 0,
#     0, 0, 0, 0
# ]

CORNER_HOUSE = House([
    Point(0, 0), Point(0, 1),
    Point(1, 0),
]) 
# [
#     1, 1, 0, 0,
#     1, 0, 0, 0,
#     0, 0, 0, 0,
#     0, 0, 0, 0
# ]


class Pig(Actor):
    def __init__(self, position: Point, house: Optional[House], name: str):
        super().__init__(position, name)
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
        super().__init__(position, "wolf")


def get_config():
    config = {}
    red_pig = Pig(
        Point(0, 1),
        STICK_HOUSE,
        "red_pig"
    )
    blue_pig = Pig(
        Point(1, 2),
        GUN_HOUSE,
        "blue_pig"
    )
    pink_pig = Pig(
        Point(3, 4),
        CORNER_HOUSE,
        "pink_pig"
    )
    config["pigs"] = [
        red_pig,
        blue_pig,
        pink_pig
    ]
    config["wolf"] = Wolf(Point(2, 3))


def run(*kwargs):
    pigs: List[Pig] = kwargs["pigs"]
    wolf: Wolf = kwargs["wolf"]




if __name__ == "__main__":
    config = get_config()
    run(**config)