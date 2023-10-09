from __future__ import annotations

import random

import pygame
from numpy.typing import NDArray
from pygame import Color

from cells.AbstractCell import AbstractCell
from cells.ConwaysCell import ConwaysCell

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
CELL_SIZE = 4
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")


def fill_grid(rows, cols, active_cells: list) -> NDArray[AbstractCell]:
    new_grid = NDArray((rows, cols), dtype=AbstractCell)
    for x in range(new_grid.shape[0]):
        for y in range(new_grid.shape[1]):
            new_cell = ConwaysCell((x, y), livingState=random.randint(0, 1) == 0)
            new_grid[x, y] = new_cell

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
    ConwaysCell.conwayUpdate(grid, activeCells)


activeCells: list = []
grid: NDArray[AbstractCell] = fill_grid(ROWS, COLS, activeCells)
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detect left mouse button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Calculate the clicked cell's coordinates
            x, y = event.pos
            row = y // CELL_SIZE
            col = x // CELL_SIZE

            # Ensure the coordinates are within bounds
            if 0 <= row < ROWS and 0 <= col < COLS:
                clicked_cell = grid[row, col]
                clicked_cell.onClick(grid)

    screen.fill(Color("black"))

    draw_grid()
    update_life()

    pygame.display.flip()

pygame.quit()
