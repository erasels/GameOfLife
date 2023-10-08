from numpy.typing import NDArray

from cells.AbstractCell import AbstractCell


class Space(AbstractCell):
    _blocker: bool

    @property
    def blocker(self) -> bool:
        return self._blocker

    @blocker.setter
    def blocker(self, state: bool):
        self._blocker = state

    def update(self, grid: NDArray):
        pass

    def __init__(self, position: tuple = (0, 0)):
        super().__init__(position)
        self._blocker = False
