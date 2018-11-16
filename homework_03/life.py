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

        self.clist = game.cell_list()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_grid()
            self.draw_cell_list(self.clist)
            self.clist = self.update_cell_list(self.clist)

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True) ->list:
        """ Создание списка клеток.
        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        self.clist = []
        small_list = []
        if randomize is True:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    small_list.append(random.randint(0, 1))
                self.clist.append(small_list)
                small_list = []
        else:
            self.clist = [[0] * self.cell_width for _ in range(self.cell_height)]
        return self.clist

    def draw_cell_list(self, clist: list):
        """ Отображение списка клеток
        :param clist: Список клеток для отрисовки, представленный в виде матрицы
        """

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

    def get_neighbours(self, cell: tuple) -> list:
        """ Вернуть список соседей для указанной ячейки
        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        row, col = cell
        a = self.cell_height - 1
        b = self.cell_width - 1
        neighbours = [self.clist[i][j] for i in range(row - 1, row + 2) for j in range(col - 1, col + 2)
                      if (0 <= i <= a) and (0 <= j <= b) and (i != row or j != col)]
        return neighbours

    def update_cell_list(self, cell_list: list) -> list:
        """ Выполнить один шаг игры.
        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.
        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        deepcopy = copy.deepcopy(self.clist)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                neighbours = sum(self.get_neighbours((i, j)))
                if cell_list[i][j]:
                    if not 1 < neighbours < 4:
                        deepcopy[i][j] = 0
                else:
                    if neighbours == 3:
                        deepcopy[i][j] = 1
        self.clist = deepcopy
        return self.clist


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
