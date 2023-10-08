import pygame
import numpy as np
from numpy.typing import NDArray

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

# Initialize the grid randomly
grid: NDArray[int] = np.random.choice([0, 1], size=(ROWS, COLS), p=[0.9, 0.1])


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
