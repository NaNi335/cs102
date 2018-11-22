import pygame
from pygame.locals import *
import random
import copy


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10) -> None:
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

    def draw_grid(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_cell_list(self, cell_list: "CellList") -> None:
        x = 0
        y = 0
        for cell in cell_list:
            if cell.is_alive():
                pygame.draw.rect(self.screen, pygame.Color('green'),
                                 [x + 1, y + 1, self.cell_size - 1, self.cell_size - 1])
            else:
                pygame.draw.rect(self.screen, pygame.Color('white'),
                                 [x + 1, y + 1, self.cell_size - 1, self.cell_size - 1])
            x += self.cell_size
            if x >= self.width:
                y += self.cell_size
                x = 0

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        cell_list = CellList(self.cell_height, self.cell_width, randomize=True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(cell_list)
            cell_list.update()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


class Cell:

    def __init__(self, row: int, col: int, state=False) -> None:
        self.state = state
        self.row = row
        self.col = col

    def is_alive(self) -> bool:
        return self.state


class CellList:

    def __init__(self, nrows: int, ncols: int, randomize=False) -> None:
        self.nrows = nrows
        self.ncols = ncols
        self.grid = []
        for element in range(nrows):
            line = []
            for col_number in range(ncols):
                if randomize:
                    line.append(Cell(element, col_number, random.randint(0, 1)))
                else:
                    line.append(Cell(element, col_number, False))
            self.grid.append(line)

    def get_neighbours(self, cell: Cell) -> list:
        neighbours = []
        col, row = cell.col, cell.row
        for element in range(row - 1, row + 2):
            for col_number in range(col - 1, col + 2):
                if element in range(0, self.nrows) and col_number in range(0, self.ncols) \
                        and (col_number != col or element != row):
                    neighbours.append(self.grid[element][col_number])
        return neighbours

    def update(self):
        new_clist = copy.deepcopy(self.grid)
        for cell in self:
            summa = sum(i.is_alive() for i in self.get_neighbours(cell))
            if summa != 2 and summa != 3:
                new_clist[cell.row][cell.col].state = False
            elif summa == 3:
                new_clist[cell.row][cell.col].state = True
        self.grid = new_clist
        return self

    def __iter__(self):
        self.element, self.col_number = 0, 0
        return self

    def __next__(self) -> Cell:
        if self.element < self.nrows:
            cell = self.grid[self.element][self.col_number]
            self.col_number += 1
            if self.col_number == self.ncols:
                self.element += 1
                self.col_number = 0
            return cell
        else:
            raise StopIteration

    def __str__(self) -> str:
        string = ''
        for element in range(0, self.nrows):
            for col_number in range(0, self.ncols):
                if self.grid[element][col_number].state:
                    string += '1 '
                else:
                    string += '0 '
            string += "\n"
        return string

    @classmethod
    def from_file(cls, filename: str) -> "CellList":
        with open(filename, 'r') as f:
            grid = []
            row = 0
            col = 0
            ncol = 0
            for lenght in f:
                line = []
                for element in lenght:
                    if element == '0':
                        line.append(Cell(row, col, False))
                    if element == '1':
                        line.append(Cell(row, col, True))
                    col += 1
                ncol = col
                col = 0
                grid.append(line)
            for line in grid:
                for cell in line:
                    cell.row = row
                row += 1

            cell_list = CellList(row, ncol, False)
            cell_list.grid = grid
            return cell_list


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
