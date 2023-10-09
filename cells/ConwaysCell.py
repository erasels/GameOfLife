from numpy.typing import NDArray
from pygame import Color

from cells.AbstractCell import AbstractCell
from cells.Space import Space


class ConwaysCell(AbstractCell):

    def setLivingState(self, state: bool) -> None:
        super().setLivingState(state)
        if not state:
            self.color = Color("red")
        else:
            self.color = Color("green")

    def getNeighbors(self, grid: NDArray) -> list:
        ret = []
        row, col = self.position
        for i in range(row - 1, row + 2):
            if i < 0 or i >= grid.shape[0]:
                continue
            for j in range(col - 1, col + 2):
                if j < 0 or j >= grid.shape[1]:
                    continue
                if (i, j) == self.position:
                    continue

                if not isinstance(grid[i, j], Space):
                    ret.append(grid[i, j])

        return ret

    def update(self, grid: NDArray, activeCells: list):
        neighbors = self.getNeighbors(grid)
        livingNeighbors = sum(1 for neighbor in neighbors if not neighbor.isDead())
        if self.isDead():
            if livingNeighbors == 3:
                self.setLivingState(True)
                self.color = Color("blue")
        else:
            if livingNeighbors < 2 or livingNeighbors > 3:
                self.die()

    def __init__(self, position: tuple = (0, 0), livingState: bool = True):
        super().__init__(position)
        self.setLivingState(livingState)
