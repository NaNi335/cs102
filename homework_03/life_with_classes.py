import pygame
from pygame.locals import *
import random
import copy


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
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


class Cell:

    def __init__(self, row, col, state=False):
        self.state = state
        self.row = row
        self.col = col

    def is_alive(self):
        return self.state


class CellList:

    def __init__(self, nrows, ncols, randomize=False):
        self.nrows = nrows
        self.ncols = ncols

        """
        if randomize:
            self.grid = [[Cell(i, j, random.randint(0, 1)) for j in range(ncols)] for i in range(nrows)]
        else:
            self.grid = [[Cell(i, j, 0) for j in range(ncols)] for i in range(nrows)]
        """

        self.grid = []
        small_list = []
        if randomize is True:
            for i in range(self.nrows):
                for j in range(self.ncols):
                    small_list.append(random.randint(0, 1))
                self.grid.append(small_list)
                small_list = []
        else:
            self.grid = [[0] * self.nrows for _ in range(self.ncols)]

    def get_neighbours(self, cell):
        row, col = cell
        a = self.nrows - 1
        b = self.ncols - 1
        neighbours = [self.grid[i][j] for i in range(row - 1, row + 2) for j in range(col - 1, col + 2)
                      if (0 <= i <= a) and (0 <= j <= b) and (i != row or j != col)]
        return neighbours

    def update(self):
        deepcopy = copy.deepcopy(self.grid)
        for cell in self:
            spisok = self.get_neighbours(cell)
            neighbours = sum(unit.is_alive() for unit in spisok)
            if cell.is_alive():
                if not 1 < neighbours < 4:
                    deepcopy[cell.row][cell.col].state = 0
            else:
                if neighbours == 3:
                    deepcopy[cell.row][cell.col].state = 1
        self.grid = deepcopy
        return self

    @classmethod
    def from_file(cls, filename):
        grid = []
        with open (filename) as file:
            for i, x in enumerate(file):
                grid.append([Cell(i, j, int(z)) for j, z in enumerate(x) if z in '01'])
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
        self.j +=1
        if self.j == self.ncols:
            self.i += 1
            self.j = 0
        return cell

    def __str__(self):
        str = ''
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.grid.alive:
                    str += '1'
                else:
                    str += '0'
            str += '\n'
        return str
