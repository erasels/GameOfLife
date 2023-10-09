import random

import pygame
import numpy as np
from numpy.typing import NDArray

from cells.AbstractCell import AbstractCell
from cells.Space import Space

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
CELL_SIZE = 5
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")


def fill_grid(rows, cols, active_cells: list) -> NDArray[object]:
    new_grid = NDArray((rows, cols), dtype=object)
    for x in range(new_grid.shape[0]):
        for y in range(new_grid.shape[1]):
            new_cell = Space((x, y)) if random.randint(0, 1) == 0 else Space((x, y))
            new_grid[x, y] = new_cell
            if not isinstance(new_cell, Space):
                active_cells.append(new_cell)

    return new_grid


def draw_grid() -> None:
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            if grid[y // CELL_SIZE][x // CELL_SIZE] == 1:
                pygame.draw.rect(screen, WHITE, rect)
            else:
                pygame.draw.rect(screen, BLACK, rect)
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
            pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))


def update_life() -> None:
    global grid
    new_grid: NDArray[int] = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            # Count live neighbors
            total: int = (grid[i, (j - 1) % COLS] + grid[i, (j + 1) % COLS] +
                          grid[(i - 1) % ROWS, j] + grid[(i + 1) % ROWS, j] +
                          grid[(i - 1) % ROWS, (j - 1) % COLS] + grid[(i - 1) % ROWS, (j + 1) % COLS] +
                          grid[(i + 1) % ROWS, (j - 1) % COLS] + grid[(i + 1) % ROWS, (j + 1) % COLS])
            # Apply Conway's rules
            if grid[i, j] == 1 and (total < 2 or total > 3):
                new_grid[i, j] = 0
            elif grid[i, j] == 0 and total == 3:
                new_grid[i, j] = 1
    grid = new_grid


activeCells: list = []
grid: NDArray[object] = fill_grid(ROWS, COLS, activeCells)
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    draw_grid()
    update_life()

    pygame.display.flip()

pygame.quit()
