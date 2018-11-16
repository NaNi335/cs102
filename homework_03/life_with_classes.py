import pygame
from pygame.locals import *
import copy
import random


class Cell:

    def __init__(self, row, col, state=0):
        self.state = state
        self.row = row
        self.col = col

    def is_alive(self):
        return self.state

    def __int__(self):
        return self.is_alive()


class CellList:

    def __init__(self, nrows, ncols, randomize=False):
        self.clist = []
        self.nrows = nrows
        self.ncols = ncols

        row = []
        if randomize is True:
            for i in range(self.nrows):
                for j in range(self.ncols):
                    row.append(random.randint(0, 1))
                self.clist.append(row)
                row = []
        else:
            self.clist = [[0] * self.ncols for _ in range(self.nrows)]

    def update(self):
        deepcopy = copy.deepcopy(self.clist)
        for i in range(self.nrows):
            for j in range(self.ncols):
                number_of_neighbours = sum(self.get_neighbours((i, j)))
                if self.clist[i][j]:
                    if not 1 < number_of_neighbours < 4:
                        deepcopy[i][j] = 0
                else:
                    if number_of_neighbours == 3:
                        deepcopy[i][j] = 1
        self.clist = deepcopy
        return self.clist

    def get_neighbours(self, cell):
        row, col = cell
        a = self.nrows - 1
        b = self.ncols - 1
        neighbours = []
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i <= a and (0 <= j <= b) and (i != row or j != col):
                    neighbours.append(self.clist[i][j])
        return neighbours

    @classmethod
    def from_file(cls, filename):
        def from_file(cls, filename: str) -> "CellList":
            grid = []
            with open(filename) as file:
                for i, line in enumerate(file):
                    grid.append([Cell(i, j, int(c))
                                 for j, c in enumerate(line) if c in "01"])
            clist = cls(len(grid), len(grid[0]), False)
            clist.grid = grid
            return clist

    def __iter__(self):
        self.i, self.j = 0, 0
        return self

    def __next__(self):
        if self.i == self.nrows:
            raise StopIteration

        cell = self.grid[self.i][self.j]
        self.j += 1
        if self.j == self.ncols:
            self.i += 1
            self.j = 0
        return cell

    def __str__(self):
        str = ''
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.grid[i][j].state:
                    str += '1 '
                else:
                    str += '0 '
            str += '\n'
        return str


class GameOfLife:
    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        # http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        cell_list = CellList(self.height, self.width, randomize=True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(cell_list.clist)
            cell_list.clist = cell_list.update()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_cell_list(self, clist):
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                x = j * self.cell_size + 1  # отрисовка черной линии по бокам
                y = i * self.cell_size + 1
                a = self.cell_size - 1
                b = self.cell_size - 1
                if clist[i][j]:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x, y, a, b))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, a, b))


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
