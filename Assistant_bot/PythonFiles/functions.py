import datetime

from PythonFiles.dictionary import set_language
import PythonFiles.variables as var
from PythonFiles import database as db
import calendar
from datetime import date


# function set language of the bot
def set_language_dict(user_id):
    language = db.select_values_from_table('users', 'language', 'digit_id', user_id)[0][0]
    var.dictionary_bot[user_id] = set_language(language)
    var.language_var[user_id] = language


# function to set default values
# default_update update if key in dictionary doesn't exist (bot fell asleep), force_update if forced reset
def set_default_values_entered_mode(user_id, mode):
    if mode == 'forced_update':
        var.current_user_action_step[user_id] = ''
        var.enter_mode[user_id] = False
        var.message_to_edit[user_id] = []
        var.enter_mode_counter_step[user_id] = 0
        var.entered_data[user_id] = []
        var.calendar_current_date[user_id] = {}
        var.show_month_res[user_id] = {}

    elif mode == 'default_update':
        # PRECAUTION: if bot restart
        if user_id not in var.message_to_edit:
            var.message_to_edit[user_id] = []
        if user_id not in var.dictionary_bot:
            set_language_dict(user_id)
        if user_id not in var.current_user_action_step:
            var.current_user_action_step[user_id] = ''
        if user_id not in var.enter_mode:
            var.enter_mode[user_id] = False
        if user_id not in var.enter_mode_counter_step:
            var.enter_mode_counter_step[user_id] = 0
        if user_id not in var.entered_data:
            var.entered_data[user_id] = []
        if user_id not in var.calendar_current_date:
            var.calendar_current_date[user_id] = {}
        if user_id not in var.show_month_res:
            var.show_month_res[user_id] = {}


def print_info(user_id):
    print('''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''')
    print(f"Message_to_edit of user[{user_id}]: {var.message_to_edit[user_id]}")
    print(f"Current_user_step of user[{user_id}]: {var.current_user_action_step[user_id]}")
    print(f"Enter_mode of user[{user_id}]: {var.enter_mode[user_id]}")
    print(f"Enter_mode_counter_step of user[{user_id}]: {var.enter_mode_counter_step[user_id]}")
    print(f"Entered_data of user[{user_id}]: {var.entered_data[user_id]}")
    print(f"Show_month_res: {var.show_month_res[user_id]}")


#  эта фунция работает с библиотекой calendar
'''    August 2022
Mo Tu We Th Fr Sa Su
 1  2  3  4  5  6  7
 8  9 10 11 12 13 14
15 16 17 18 19 20 21
22 23 24 25 26 27 28
29 30 31'''


#  разбивает дефолтный вывод на строки
def get_calendar_rows(year, month):
    kek = calendar.month(year, month, 2, 1)

    new_list = list()
    res_list = list()

    counter = 0
    counter1 = 0

    for i in kek:
        if i == '\n':
            new_list.append(kek[counter1:counter])
            counter1 = counter + 1
        counter += 1

    res_list.append(new_list[0].strip())

    new_list = new_list[1:]

    res_list.append(new_list[0].split(' '))

    for i in new_list[1:]:
        temp = []
        k = i.split(' ')
        for j in k:
            if j.isdigit():
                temp.append(j)
        res_list.append(temp)

    for i in range(7 - len(res_list[2])):
        res_list[2].insert(0, '')

    for i in range(7 - len(res_list[-1])):
        res_list[-1].append('')

    #  print(res_list)
    return res_list


# ф-ция возвращает текущий год и месяц
def get_current_date():
    today = date.today()
    year, month = str(today)[:-3].split('-')
    if month[0] == '0':
        month = month[1]
    return year, month


#  ф-ция возвращает готовый набор кнопок для размещения в виде календаря
def calendar_buttons_creating(user_id, year, month):
    import PythonFiles.variables as variable

    if year is None and month is None:
        year, month = get_current_date()

    k = get_dates_with_event(user_id, year, month)

    res = get_calendar_rows(int(year), int(month))
    new_res = list()

    month_prev_btn = ['<', 'prev_month']
    month_next_btn = ['>', 'next_month']

    variable.calendar_current_date[user_id]['year'] = year
    variable.calendar_current_date[user_id]['month'] = month

    year_month = [f"{var.dictionary_bot[user_id]['month'][int(month)]} {year}", 'year_month']

    first_row = [tuple(year_month)]

    new_res.append(tuple(first_row))

    for i in res[1:]:
        m = []
        if type(i) == list:
            for j in i:
                if k != '':
                    if j.isdigit() and j in map(str, k):
                        m.append(tuple([f"📌{j}", f" {j}"]))
                    else:
                        m.append(tuple([f" {j}", f" {j}"]))
                else:
                    m.append(tuple([f" {j}", f" {j}"]))

        new_res.append(tuple(m))

    last_row = [tuple(month_prev_btn), tuple([' ', ' ']), tuple(month_next_btn)]
    new_res.append(tuple(last_row))
    return new_res


# ф-ция проверки введенной даты или времени
def check_datetime_format(string, format_datetime):
    format_values = 'Y'

    if len(string) == 5 and format_datetime == 'time':
        format_values = "%H:%M"
    elif len(string) == 10 and format_datetime == 'date':
        format_values = '%d.%m.%Y'

    try:
        datetime.datetime.strptime(string, format_values)
        return True
    except ValueError:
        return False


#  ф-ция переключения месяца в инлайн календаре
def switch_month(year, month, act):
    if act == 'prev_month':
        month -= 1
        if month == 0:
            year -= 1
            month = 12
    if act == 'next_month':
        month += 1
        if month == 13:
            year += 1
            month = 1

    return str(year), str(month)


# фунцкия получает данные определенного месяца
def get_select_events_data(user_id, year='', month=''):
    if year == '' and month == '':
        year, month = get_current_date()
    k = db.select_values_from_table(f't{user_id}', '*', 'date_of_the_event', f'{month}.{year}', 'yes',
                                    'yes')
    res = []

    for i in k:
        res.append(i)
    return res


def get_dates_with_event(user_id, year, month):
    res = get_select_events_data(user_id, year, month)
    var.show_month_res[user_id]['res'] = res
    var.show_month_res[user_id]['count'] = len(res)
    var.show_month_res[user_id]['current_counter'] = 0

    k = []
    for i in res:
        k.append(i[2][:2])
    k = list(map(int, k))
    return k


# функция получает количество событий в месяце
def get_select_event_count(user_id):
    year, month = get_current_date()
    k = db.select_values_from_table(f't{user_id}', 'date_of_the_event', 'date_of_the_event', f'{month}.{year}', 'yes',
                                    'yes')

    count_of_events = len(k)  # количество событий в таблице

    return count_of_events
