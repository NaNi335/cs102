import requests
import config
import telebot
import logging
from bs4 import BeautifulSoup
from datetime import *

# just a check point
logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(config.access_token)


def save_cache_page(group, page, week=''):
    file = "{0}{1}.txt".format(week, group)
    f = open(file, "w")
    f.write(page)
    f.close()


def get_page(group, week=''):
    file = "{0}{1}.txt".format(week, group)
    try:
        f = open(file, 'r')
        web_page_content = f.read()
        logging.info('we did it with opening the cashed file')
    except FileNotFoundError:
        if week:
            week = str(week) + '/'
        url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
            domain=config.domain,
            week=week,
            group=group)
        response = requests.get(url)
        web_page_content = response.text
        print(web_page_content)
        week = week[:-1]
        save_cache_page(group, web_page_content, week)
        logging.info('we created a new file')
    return web_page_content


def parse_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")

    days = {"monday": "1day",
            "tuesday": "2day",
            "wednesday": "3day",
            "thursday": "4day",
            "friday": "5day",
            "saturday": "6day"}

    daycode = days[day]

    schedule_table = soup.find("table", attrs={"id": daycode})
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text + ', ' + room.dd.text for room in locations_list]

    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['start', 'help'])
def answer_help(message):
    resp = """<b>Комманды бота:</b>
    1) <b>Вывод расписания в указанный день:</b> \n /(День недели) (Неделя)* (Номер группы) 
    <i>* необязательный параметр, "1" - четная неделя, "2" - нечетная неделя</i>
    2) <b>Вывод ближайшего расписания:</b> \n /near (Номер группы)
    3) <b>Вывод расписания на завтра:</b> \n /tomorrow (Номер группы)
    4) <b>Вывод всего расписания:</b> \n /all (Неделя) (Номер группы)
    
    <i>Для вызова списка функций используйте /help</i>"""
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    # just a check point
    logging.info('получаем команду с опред. днем')
    try:
        day, group = message.text.split()
        print(day, group)
        day = day[1:]  # тк day будет у нас с лишним символом "/"
        web_page = get_page(group)
    except:
        day, week, group = message.text.split()
        print(day, week, group)
        day = day[1:]
        web_page = get_page(group, week)
    times_lst, locations_lst, lessons_lst = parse_schedule(web_page, day)
    resp = ''
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        # функция zip объединяет в кортежи элементы из последовательностей переданных в качестве аргументов
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    logging.info('считаем nearest')
    _, group = message.text.split
    # time.strftime("%s") -- current timestamp in sec



    #day = time.strftime('%Y %m %d')
    #listdate = day.split



@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    what_day_is_it_today = datetime.today().weekday()
    print(what_day_is_it_today)
    what_day_is_it_today = str(what_day_is_it_today)
    print(what_day_is_it_today)
    days = {"6": "monday",
            "0": "tuesday",
            "1": "wednesday",
            "2": "thursday",
            "3": "friday",
            "4": "saturday",
            "5": "monday"}

    today = datetime.today()
    week_is = today.strftime("%U")
    if int(week_is) % 2 == 0:
        week = "1"
    else:
        week = "2"

    _, group = message.text.split()
    web_page = get_page(group, week)
    day = days[what_day_is_it_today]
    print("target day we need is", day)
    times_lst, locations_lst, lessons_lst = parse_schedule(web_page, day)
    resp = ''
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    resp = ''
    _, group, week = message.text.split()
    alldays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    for day in alldays:
        if week:
            web_page = get_page(group, week)
        else:
            web_page = get_page(group)
        times_lst, locations_lst, lessons_lst = parse_schedule(web_page, day)
        schedule = ''
        for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
            schedule += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
        resp += '<b>{0}</b>'.format(day) + "\n" + schedule
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
