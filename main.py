import random

import pygame
import numpy as np
from numpy.typing import NDArray
from pygame import Color

from cells.ConwaysCell import ConwaysCell
from cells.Space import Space

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
CELL_SIZE = 8
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")


def fill_grid(rows, cols, active_cells: list) -> NDArray[object]:
    new_grid = NDArray((rows, cols), dtype=object)
    for x in range(new_grid.shape[0]):
        for y in range(new_grid.shape[1]):
            new_cell = ConwaysCell((x, y)) if random.randint(0, 3) == 0 else Space((x, y))
            new_grid[x, y] = new_cell
            if not isinstance(new_cell, Space):
                active_cells.append(new_cell)

    return new_grid


def draw_grid() -> None:
    global grid
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, grid[row, col].color, rect)

    # If you want grid lines, you can draw them separately outside the above loops:
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))


def update_life() -> None:
    global grid, activeCells
    for cell in activeCells:
        cell.update(grid, activeCells)


activeCells: list = []
grid: NDArray[object] = fill_grid(ROWS, COLS, activeCells)
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(Color("black"))

    draw_grid()
    update_life()

    pygame.display.flip()

pygame.quit()
