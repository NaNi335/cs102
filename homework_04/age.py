import datetime
from datetime import datetime
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    friends_info = get_friends(user_id, 'bdate')
    age_in_days = []  # возраст всех пользователей В ДНЯХ
    full_years = []  # возраст всех пользователей В ПОЛНЫХ ГОДАХ
    friends_ages = []
    for friend in friends_info:
        full_years.append(User(**friend))  # User - пользователь с необязательным полем даты рождения
    for friend in full_years:
        if friend.bdate is not None:
            birthday_as_list = friend.bdate.split('.')  # [12, 03, 2000]
            if len(birthday_as_list) == 3:
                now_as_string = str(datetime.now()).split(' ')[0]  # выведет 2018-11-30
                now = now_as_string.split('-')  # [2018, 11, 30]
                years = int(now[0]) - int(birthday_as_list[2])
                months = int(now[1]) - int(birthday_as_list[1])
                days = int(now[2]) - int(birthday_as_list[0])
                total_days = days + months * 30.4 + years * 365.25
                age_in_days.append(total_days)
                friends_ages.append(years)
    if age_in_days:
        return median(friends_ages)
    else:
        return None


