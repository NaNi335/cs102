from collections import Counter
import datetime
from datetime import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from typing import List, Tuple

from api import messages_get_history
from api_models import Message
import config


Dates = List[datetime.date]
Frequencies = List[int]


plotly.tools.set_credentials_file(
    username=config.PLOTLY_CONFIG['nani335'],
    api_key=config.PLOTLY_CONFIG['6ieeb82yGQkavDiWUbXT']
)


def fromtimestamp(ts: int) -> datetime.date:
    return datetime.datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> Tuple[Dates, Frequencies]:
    """ Получить список дат и их частот
    :param messages: список сообщений
    """
    dates = [datetime.fromtimestamp(messages[i]['date'].strftime("%Y-%m-%d")) for i in range(len(messages))]
    dates_quantity = Counter(dates)
    date = [time for time in dates_quantity]
    quantity = [dates_quantity[time] for time in dates_quantity]
    return date, quantity


def plotly_messages_freq(dates: Dates, freq: Frequencies) -> None:
    """ Построение графика с помощью Plot.ly
    :param date: список дат
    :param freq: число сообщений в соответствующую дату
    """
    # PUT YOUR CODE HERE