import os
from collections import defaultdict
from operator import itemgetter
from itertools import groupby

# pip install tabulate
from tabulate import tabulate


class DataFrame:

    def __init__(self, headers, rows):
        self._headers = headers
        self._rows = rows

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, new_headers):
        assert len(self._headers) == len(new_headers)
        pass

    @property
    def rows(self):
        return self._rows

    def group_by(self, by):
        pass

    def merge(self, df, by):
        pass

    def __getitem__(self, name):
        pass

    def __setitem__(self, name):
        pass

    def __str__(self):
        return tabulate(self.rows, headers=self.headers)

    @staticmethod
    def from_file(path):
        pass

    def to_csv(path):
        pass


class GrouppedDataFrame:

    def __init__(self, by, headers, groups):
        self._by = by
        self._headers = headers
        self._groups = groups

    def sum_by(self, by):
        pass


# BASE_PATH =  # ...
PATH = os.path.join(BASE_PATH, 'spb_cameras.csv')
POPULATION_PATH = os.path.join(BASE_PATH, 'spb_population_per_district.csv')
CAMERAS_PATH = os.path.join(BASE_PATH, 'cameras_per_district.csv')

# ===================================================
df = DataFrame.from_file(PATH)
amount_df = df.group_by('district').sum_by('amount')
amount_df.headers = ['Район', 'Число Камер']
amount_df.to_csv('cameras_per_district.csv')
print(amount_df)
# Район                Число Камер
# -----------------  -------------
# Адмиралтейский               396
# Василеостровский             588
# Выборгский                  3299
# Калининский                 3369
# Кировский                    732
# ...


# ===================================================
amount_df = DataFrame.from_file(CAMERAS_PATH)
pop_df = DataFrame.from_file(POPULATION_PATH)
full_df = amount_df.merge(pop_df, by='Район')
print(full_df)
# Район                Число Камер    Население    Площадь
# -----------------  -------------  -----------  ---------
# Калининский                 3369       538258      40.18
# Выборгский                  3299       509592     115.52
# Фрунзенский                 2787       401410      37.52
# Красногвардейский           2379       357906      56.35
# ...

# full_df['Плотность'] =  # ...
full_df.to_csv('exam_done.csv')
print(full_df)
# Район                Число Камер    Население    Площадь    Плотность
# -----------------  -------------  -----------  ---------  -----------
# Калининский                 3369       538258      40.18      13396.2
# Выборгский                  3299       509592     115.52      4411.29
# ...