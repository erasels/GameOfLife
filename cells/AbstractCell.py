from abc import ABC, abstractmethod

from numpy.typing import NDArray
from pygame import Color

class AbstractCell(ABC):
    _dead: bool
    _position: tuple
    _color: Color

    def isDead(self) -> bool:
        return self._dead

    def setLivingState(self, state: bool) -> None:
        self._dead = state

    def die(self):
        self.setLivingState(False)

    @property
    def position(self) -> tuple:
        return self._position

    @position.setter
    def position(self, position: tuple):
        self._position = position

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color: Color):
        self._color = color

    @abstractmethod
    def update(self, grid: NDArray, activeCells: list):
        pass

    # Method to effectively remove the cell from game
    def erase(self, grid: NDArray, activeCells: list):
        activeCells.remove(self)

    def __init__(self, position: tuple = (0, 0)):
        self._dead = False
        self._position = position
