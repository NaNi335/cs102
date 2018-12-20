import requests
import config
import telebot
import logging
from bs4 import BeautifulSoup
import os
import sqlite3
import hashlib

db_filename = 'bot.db'
db_is_new = not os.path.exists(db_filename)
conn = sqlite3.connect(db_filename)


logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(config.access_token)


def save_cache_page(group, page):
    file = "{0}.txt".format(group)
    f = open(file, "w")
    f.write(str(page.encode('utf8')))
    f.close()


def open_file(group):
    file = "{0}.txt".format(group)
    try:
        f = open(file, "r")
        res = f.read()
    except:
        res = 'NOTHING'

    return res

def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page_content = response.text
    cached_page = open_file(group)
    h1 = hashlib.md5()
    h1.update(web_page_content.encode('utf8'))
    h2 = hashlib.md5()
    h2.update(cached_page.encode('utf8'))

    logging.info('old md5 is {0} and new md5 is {1}'.format(h2.hexdigest(), h1.hexdigest()))

    if h1.hexdigest() == h2.hexdigest():
        web_page_content = cached_page
        logging.info('return cached')
    else:
        save_cache_page(group, web_page_content)
        logging.info('return new')

    return web_page_content




def parse_schedule_for_a_monday(web_page):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": "1day"})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text + ', ' + room.dd.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list

def parse_schedule_for_a_everyday(web_page, day, type=oneday):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием
    days = {"monday" : "1day",
            "tuesday": "2day",
            "wednesday": "3day",
            "thursday": "4day",
            "friday": "5day",
            "saturday": "6day"}

    daycode = days[day]

    schedule_table = soup.find("table", attrs={"id": daycode})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text + ', ' + room.dd.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


# @bot.message_handler(commands=['monday'])
# def get_monday(message):
#     """ Получить расписание на понедельник """
#     _, group = message.text.split()
#     web_page = get_page(group)
#     times_lst, locations_lst, lessons_lst = \
#         parse_schedule_for_a_monday(web_page)
#     resp = ''
#     for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
#         # функция zip объединяет в кортежи элементы из последовательностей переданных в качестве аргументов
#         resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
#     bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    # PUT YOUR CODE HERE
    logging.info('ловим команду с опред. днем')
    """ Получить расписание на понедельник """
    day, group = message.text.split()
    day = day[1:]
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_everyday(web_page, day)
    resp = ''
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        # функция zip объединяет в кортежи элементы из последовательностей переданных в качестве аргументов
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')
    pass


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """Получить расписание на следующий день"""
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    # PUT YOUR CODE HERE
    pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
