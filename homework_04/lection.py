"""

min(['ab', 'z', 'abc'], key=lambda x: len(x#)

states = [-1, 0, 1]
values = [rnd() for _ in range]
min(states, key=lambda state: abs(value - state)) for value in values]

"""

# Api Vk
"""
comfig.py

не надо её коммитить -> .gitignore

VK_CONFIG = {
    'access_token':'',
    'domain':'https//...',
    'version': '5.87'
}

PLOTLY_CONFIG = {
'api_key' = '...'
''
пакет апи от плотпай

прогнозирование возраста через друзейЖ

vk_api.py

get_friends
.... (репозиторий)

version = confog.get('version')
access_token = config.get('access)
domain = config.get(...)

query_params = Формирование параметров запроса
response = Запрос к Api c указанными прааметрами
Проверить что ответ не содержит ошибок
вернуть список друзей

срок действия токена истек или в нем ошибкаб он не поддерживает запрос или...


Библиотека requests

возвращает ответ в формате json

Если ошибка, когда делается запрос
необходима функция, которая оборачивает функцию запроса

можно проверить запросы на httpbin
500 ошибка - систеная ошибка сервера

------
ответ сервера (json)

валлидируем соответствие нашему формату:

pip install pydantic

from pydantic import BaseModel
from python import Optional

class BaseUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    online: int
    deactivated: Optional[str]
    
class User(BaseUser):
    bdate: Optional[str]
    
    #валлидатор который парсит ответ автоматически
    см фотка №4 
    ***
    @validator('bdate')
    def bdate_validate(cls, v):
    # return date()
    #return None
    ***
см фотка №3
***
user.bdate # => None
***


class Message(BaseModel):
pass

def age_predict(user_id):
    #дальше пишем функцию
    
    
days = 13245363
years = days / 365.25


максимальное количество сообщений = 200
но тк мы можем делать сколько угодно запросов
должен будет происходить сдвиг на 200 и повторный запрос

после трех запросов вк отрубает
=> надо будет вчислить время на три запроса? подождать столько же и только тогда делать запрос


считаем количество сообщений по дням/часам/годам

Рисование графика через Plot.ly  => api_key

___________________________

ГРАФ ДРУЗЕЙ
get_network
делаем список id
pip install python-igraph
(рисует графы  + алгоритмы над графами)
как люди связаны друг  с другом = community

get_network грубо говоря формирует данные которые нам потом надо будет правильно подставить!



import time
delay = ... (формула с habr)
time.sleep(delay)

"""
