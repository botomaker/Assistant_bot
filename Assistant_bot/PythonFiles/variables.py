dictionary_bot = dict()  # dictionary for bot's language
language_var = dict()  # language variable, takes the value of the language that is taken from the DataBase table
message_to_edit = dict()  # variable stores message which will be edited
current_user_action_step = dict()  # current user step (which button pressed)
enter_mode = dict()  # variable to turn on/off enter mode
enter_mode_counter_step = dict()  # variable which stores enter step of the user
entered_data = dict()  # whariable stores entered data
calendar_current_date = dict()  # variable stores current month and year to switch month in inline button calendar
show_month_res = dict()  # variable stores days which have an events

# smiles
check_mark_smile = u'\U00002705'
settings_gear_smile = u'\U00002699'
ukraine_flag_smile = '🇺🇦'
english_flag_smile = '🇬🇧'
events_smile = '📅'
about_bot_smile = '🙋‍♂️'
main_menu_smile = '🏠'
show_events_smile = '🔎'
add_event_smile = '📝'
edit_event_smile = '✏️'
del_event_smile = '❌'
back_button_smile = '🔙'
reminder_button_smile = '🔔'
change_lang_smile = '🗣'
mechanic_hand_smile = '🦾'
hello_hand_smile = '✌️'
man_with_laptop_smile = '👨‍💻'
man_hanging_hand_smile = '🙋‍♂️'
facepalm_man_smile = '🤦‍♂️'
blind_smile = '⚡️'
tornado_smile = '🌪'
money_smile = '💸'
notes_smile = '📋'

'''
###################################################################
###################################################################
###################################################################
BUTTONS ###########################################################
###################################################################
###################################################################
###################################################################
'''


# main menu's buttons
def main_menu_buttons(user_id):
    return dictionary_bot[user_id]['events_button'], (dictionary_bot[user_id]['settings_button'],
                                                      dictionary_bot[user_id]['aboutbot_button'])


# setting's buttons
def settings_menu_buttons(user_id):
    return (dictionary_bot[user_id]['notification_button'], dictionary_bot[user_id]['change_language_button']), \
           dictionary_bot[user_id]['back_button']


# event's menu buttons
def events_menu_buttons(user_id):
    return dictionary_bot[user_id]['show_events'], (dictionary_bot[user_id]['add_event'],
                                                    dictionary_bot[user_id]['edit_event'],
                                                    dictionary_bot[user_id]['remove_event']), \
           dictionary_bot[user_id]['main_menu']


# menu buttons
def get_menu_buttons_list(user_id):
    return dictionary_bot[user_id]['aboutbot_button'], dictionary_bot[user_id]['back_button'], \
           dictionary_bot[user_id]['settings_button'], dictionary_bot[user_id]['change_language_button'], \
           dictionary_bot[user_id]['main_menu'], dictionary_bot[user_id]['events_button'], \
           dictionary_bot[user_id]['add_event'], dictionary_bot[user_id]['show_events'], \
           dictionary_bot[user_id]['edit_event'], dictionary_bot[user_id]['remove_event']


# button yes and main menu after entered data
def get_save_final_buttons_list(user_id):
    return [(dictionary_bot[user_id]['yes_btn'], dictionary_bot[user_id]['main_menu'])]


'''
###################################################################
###################################################################
###################################################################
MESSAGE HANDLER####################################################
###################################################################
###################################################################
###################################################################
'''


# enter mode text dictionary
def enter_mode_text(user_id, counter):
    dictionary = {0: "enter_name_of_the_event", 1: "enter_description_of_the_event", 2: "choose_date_of_the_event",
                  3: "set_reminder_text_add", 4: "select_the_frequency_of_the_event", 5: 'set_date_of_the_reminder',
                  6: 'enter_time_of_the_rimender', 7: "save_data_event"}
    return dictionary_bot[user_id][dictionary[counter]]


# save text for added data
def reply_text_save_add_data(user_id, enter_data, all_right):
    dictionary = dictionary_bot[user_id]
    if enter_data[-1] != '0':
        text = f"<i>{dictionary['save_data_name']}</i>{enter_data[0]}\n" \
               f"<i>{dictionary['save_data_des']}</i>{enter_data[1]}\n<i>{dictionary['save_data_date']}</i>" \
               f"{enter_data[2]}\n<i>{dictionary['frequency_is_txt']}</i>{enter_data[3]}\n<i>" \
               f"{dictionary['date_of_remind']}</i>{enter_data[4]}\n<i>{dictionary['time_of_remind']}</i>" \
               f"{enter_data[5]}"
    else:
        text = f"<i>{dictionary['save_data_name']}</i>{enter_data[0]}\n" \
               f"<i>{dictionary['save_data_des']}</i>{enter_data[1]}\n<i>{dictionary['save_data_date']}</i>" \
               f"{enter_data[2]}"
        if all_right != 'yes_allright':
            text += f"\n{dictionary['reminder_not_insert']}"

    if all_right == 'yes_allright':
        text = f"<b>{dictionary['save_data_event']}</b>\n{text}"
        text += f"\n\n{dictionary['all_right?']}"

    return text


# get reminder callback buttons list
def reminder_button_list(user_id):
    return dictionary_bot[user_id]['set_reminder_inline_btn'], dictionary_bot[user_id]['later_reminder_inline_btn']


# get frequency callback button list
def frequency_buttons_list(user_id):
    return dictionary_bot[user_id]['yearly_event'], dictionary_bot[user_id]['monthly_event'], \
           dictionary_bot[user_id]['weekly_event'], dictionary_bot[user_id]['daily_event'], \
           dictionary_bot[user_id]['one_time_event']


# get frequency callback button list
def frequency_buttons_dict(user_id, frequency):
    dictionary = {dictionary_bot[user_id]['yearly_event']: 'yearly_event', dictionary_bot[user_id]['monthly_event']:
                  'monthly_event', dictionary_bot[user_id]['weekly_event']: 'weekly_event',
                  dictionary_bot[user_id]['daily_event']: 'daily_event',
                  dictionary_bot[user_id]['one_time_event']: 'one_time_event'}
    return dictionary[frequency]


'''
###################################################################
###################################################################
###################################################################
CALLBACK HANDLER###################################################
###################################################################
###################################################################
###################################################################
'''


# get callback answer of language buttons list
def get_language_callback_button_list():
    return ['UA', 'EN']


# get callback answer of calendar buttons list
def get_calendar_callback_button_list():
    callback_button = ['year_month', 'prev_month', 'next_month']
    callback_button += [f" {str(x)}" for x in range(1, 32)]
    return callback_button


def reminder_callback_button_list():
    return ['set_reminder_inline_btn', 'later_reminder_inline_btn']


def frequency_callback_buttons_list():
    return ['yearly_event', 'monthly_event', 'weekly_event', 'daily_event', 'one_time_event']


# Список кнопок в меню просмотра событий
def show_event_inline_button_list():
    return ['calendar_btn', 'search_btn']


def get_buttons_check_events_list():
    return ['prev_event', 'next_event', 'back_show_event']


# get language buttons tuples
def languages_callback_button_tuples(user_id, language):
    if language == 'UA':
        return ((f'Українська {check_mark_smile}', 'UA'), ('English', 'EN')), [dictionary_bot[user_id]['main_menu'],
                                                                               'main_menu']
    elif language == 'EN':
        return (('Українська', 'UA'), (f'English {check_mark_smile}', 'EN')), [dictionary_bot[user_id]['main_menu'],
                                                                               'main_menu']

    # return (('Українська', 'UA'), ('English', 'EN')), ['sa', 's'] works with single button
    # return [((f'Українська {smile}', 'UA'), ('English', 'EN'))]  # works only with tuple


# reminder callback buttons tuples
def reminder_callback_button(user_id):
    dict_bot = dictionary_bot[user_id]
    return [((dict_bot['set_reminder_inline_btn'], 'set_reminder_inline_btn'), (dict_bot['later_reminder_inline_btn'],
                                                                                'later_reminder_inline_btn'))]


# callback buttons of frequency tuples
def get_frequency_buttons(dict_bot):
    return [((dict_bot['yearly_event'], 'yearly_event'), (dict_bot['monthly_event'], 'monthly_event'),
             (dict_bot['weekly_event'], 'weekly_event'), (dict_bot['daily_event'], 'daily_event'),
             (dict_bot['one_time_event'], 'one_time_event'))]


# кнопки для переключения просмотра событий
def buttons_check_events(user_id, number, count):
    return [(('<', 'prev_event'), (f"{number}/{count}", ' '), ('>', 'next_event')),
            [dictionary_bot[user_id]['back_button'], 'back_show_event']]


def buttons_check_events_remove(user_id, number, count):
    return [(('<', 'prev_event'), (f"{number}/{count}", ' '), ('>', 'next_event')),
            ((dictionary_bot[user_id]['back_button'], 'back_show_event'), (dictionary_bot[user_id]['remove_event_short'],
             'remove_event_short'))]


def buttons_check_events_edit(user_id, number, count):
    return [(('<', 'prev_event'), (f"{number}/{count}", ' '), ('>', 'next_event')),
            ((dictionary_bot[user_id]['back_button'], 'back_show_event'), (dictionary_bot[user_id]['edit_event_short'],
             'edit_event_short'))]


def get_show_events_inline_buttons(user_id):
    return [((dictionary_bot[user_id]['calendar_btn'], 'calendar_btn'), (dictionary_bot[user_id]['search_btn'],
                                                                         'search_btn'))]


'''
###################################################################
###################################################################
###################################################################
DICTIONARY ########################################################
###################################################################
###################################################################
###################################################################
'''

'''
    #########           #########     
    ###     ###         ###     ###
    ###      ###        ###      ###
    ###      ###        ###      ###
    ###      ###        ###    ###
    ###      ###        ###     ###
    ###     ###         ###      ###
    #########           ###########
'''


def get_users_table_create_columns():
    return '''
        digit_id INTEGER NOT NULL,
        telegram_id VARCHAR(255) NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        language VARCHAR(255) NOT NULL
    '''


def get_user_personal_create_table_columns():
    return '''
        event VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        date_of_the_event VARCHAR(255) NOT NULL,
        frequency VARCHAR(255) NOT NULL,
        date_of_the_remind VARCHAR(255) NOT NULL,
        time_of_the_remind VARCHAR(255) NOT NULL
    '''


def get_user_table_columns():
    return 'digit_id, telegram_id, first_name, surname, language'


def get_user_personal_table_columns():
    return 'event, description, date_of_the_event, frequency, date_of_the_remind, time_of_the_remind'
