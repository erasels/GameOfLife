from __future__ import annotations

from numpy.typing import NDArray
from pygame import Color

from cells.AbstractCell import AbstractCell
from cells.Space import Space


class ConwaysCell(AbstractCell):
    toUpdate: list[ConwaysCell] = []

    @staticmethod
    def conwayUpdate(grid, activeCells):
        for col in range(grid.shape[0]):
            for row in range(grid.shape[1]):
                grid[col, row].update(grid, activeCells)
        ConwaysCell.processCalculatedUpdates()

    @staticmethod
    def processCalculatedUpdates():
        for cell in ConwaysCell.toUpdate:
            cell.takeNextState()
        ConwaysCell.toUpdate.clear()

    def setLivingState(self, state: bool) -> None:
        super().setLivingState(state)
        if not state:  # Is alive
            self.color = Color("green")
        else:
            self.color = Color("red")

    def setNextState(self, state: bool):
        if state != self.isDead():
            ConwaysCell.toUpdate.append(self)
        super().setNextState(state)

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

    def onClick(self, grid):
        neighbors = self.getNeighbors(grid)
        print(f"Neighbors of cell at ({self.position[0]}, {self.position[1]}, Dead:{self.isDead()}):")
        for neighbor in neighbors:
            print(f"{neighbor.position} Dead:{grid[neighbor.position].isDead()}")
            if neighbor.isDead():
                neighbor.color = Color("yellow")

    def update(self, grid: NDArray, activeCells: list):
        neighbors = self.getNeighbors(grid)
        livingNeighbors = sum(1 for neighbor in neighbors if not neighbor.isDead())
        if self.isDead():
            if livingNeighbors == 3:
                self.setNextState(False)
        else:
            if livingNeighbors < 2 or livingNeighbors > 3:
                self.setNextState(True)

    def __init__(self, position: tuple = (0, 0), livingState: bool = True):
        super().__init__(position)
        self.setLivingState(livingState)
