# Rule of Game of Life
# Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by overpopulation.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

import pygame
import time
import numpy as np


color_gb =(10,10,10)
color_grid = (40,40,40)
color_die_next = (170,170,170)
color_alive_next = (255,255,255)

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))
    #examine each dim in grid
    for i, j in np.ndindex(cells.shape):
        #computing "alive sorce" of each dim: sum of 3x3 matrix from (i,j) less (i,j) itself
        alive = np.sum(cells[i-1:i+2, j-1:j+2]) - cells[i, j]
        color = color_gb if cells[i,j] == 0 else color_alive_next

        if cells[i,j] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = color_die_next
            elif 2 <= alive <=3:
                updated_cells[i,j] = 1
                if with_progress:
                    color = color_alive_next
        else:
            if alive == 3:
                updated_cells[i,j] = 1
                if with_progress:
                    color = color_alive_next

        pygame.draw.rect(screen, color, (j * size, i*size, size - 1, size -1))
        
    return updated_cells #an updated matrix


def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))

    cells = np.zeros((60,80))
    screen.fill(color_grid)
    
    print(update(screen, cells, 10))

    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        #game screen control
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(color_grid)

        if running:
            cells = update(screen, cells, 10, True)
            pygame.display.update()

        time.sleep(0.01)



if __name__ == '__main__':
    main()
    