from Keyboard import keyboard
from PythonFiles.functions import set_language_dict, switch_month, calendar_buttons_creating, get_select_events_data
import PythonFiles.database as db
import PythonFiles.variables as var


########################################################################################################################
#  Language settings ###################################################################################################
#  The language is setting in the bot using inline buttons #############################################################
########################################################################################################################
def language_callback_buttons_processing(answer_data, user_id):
    send_message_type_list = []
    # there is checking user current step, if not "change_language_button" send message "something happen"
    if var.current_user_action_step[user_id] == 'change_language_button':
        db.update_table_values('users', 'language', str(answer_data), 'digit_id', f"{user_id}")
        set_language_dict(user_id)
        text = var.dictionary_bot[user_id]['current_language_message']
        markup = keyboard.inline_keyboard(var.languages_callback_button_tuples(user_id, var.language_var[user_id]),
                                          None, 3)
        temp_list = [text, markup, 'edit_message']
        send_message_type_list.append(temp_list)
    else:
        text = var.dictionary_bot[user_id]['something_happened']
        temp_list = [text, '', 'edit_message']
        send_message_type_list.append(temp_list)

    return send_message_type_list


########################################################################################################################
#  main menu inline keyboard ###########################################################################################
########################################################################################################################
def main_menu_callback_button_processing(user_id):
    send_message_type_list = []

    if var.current_user_action_step[user_id] == 'change_language_button':
        text = var.dictionary_bot[user_id]['current_language_message']
        temp_list = [text, '', 'edit_message']
        send_message_type_list.append(temp_list)

        text = var.dictionary_bot[user_id]['main_menu']
        markup = keyboard.reply_keyboard(var.main_menu_buttons(user_id), 2, True, False)
        temp_list = [text, markup, 'simple_message']
        send_message_type_list.append(temp_list)
    else:
        text = var.dictionary_bot[user_id]['something_happened']
        temp_list = [text, '', 'edit_message']
        send_message_type_list.append(temp_list)

    return send_message_type_list


########################################################################################################################
#  Calendar buttons processing in enter mode ###########################################################################
########################################################################################################################
def add_mode_calendar_buttons_processing(answer_data, user_id):
    send_message_type_list = []
    # if bot off если переменная enter_mode_counter = 0, то это значит, что бот приостановился или тп,
    # происходит обработка с reply_message
    if var.enter_mode_counter_step[user_id] == 0:
        text = var.dictionary_bot[user_id]['something_happened']
        markup = ''
        temp_list = [text, markup, 'edit_message']
        send_message_type_list.append(temp_list)

    # switch months переключение месяцев, получаются текущие установленные год и месяц в боте (из ф-ции
    # создания кнопок календаря) и в ф-ции switch_month происходит увеличение/уменьшение месяца
    elif answer_data == 'prev_month' or answer_data == 'next_month':
        year, month = int(var.calendar_current_date[user_id]['year']), \
                      int(var.calendar_current_date[user_id]['month'])

        year, month = switch_month(year, month, str(answer_data))

        text = var.dictionary_bot[user_id]['choose_date_of_the_event']
        markup = keyboard.inline_keyboard(calendar_buttons_creating(user_id, year, month), None, 7)
        temp_list = [text, markup, 'edit_message']
        send_message_type_list.append(temp_list)

    elif answer_data == 'year_month':
        pass

    # Обработка кнопок календаря (числа)
    else:
        #  идет обрезка кнопки так как она создается с пробелом в начале ' 9' и проверка, является ли цифрой
        if str(answer_data)[1:].isdigit():
            year = var.calendar_current_date[user_id]['year']
            month = var.calendar_current_date[user_id]['month']

            # добавляется нолик к месяцу
            if len(str(month)) == 1:
                month = f"0{month}"
            answer_data = answer_data[1:]

            # добавляется нолик к дню
            if len(str(answer_data)) == 1:
                answer_data = f"0{str(answer_data)}"
            date_res = f"{answer_data}.{month}.{year}"

            # добавляется дата в массив со всеми введенными данными
            var.entered_data[user_id].append(date_res)

            if var.enter_mode_counter_step[user_id] == 3:
                text = var.dictionary_bot[user_id]['selected_date_txt'] + str(var.entered_data[user_id][2])
                send_message_type_list.append([text, '', 'edit_message'])
                # создается текст и кнопки для выбора устанавливать напоминание или нет
                text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id])
                markup = keyboard.inline_keyboard(var.reminder_callback_button(user_id), None, 2)
                temp_list = [text, markup, 'message_with_text']
                send_message_type_list.append(temp_list)

                var.enter_mode_counter_step[user_id] = 4

            elif var.enter_mode_counter_step[user_id] == 6:
                text = var.dictionary_bot[user_id]['selected_date_txt'] + str(var.entered_data[user_id][4])
                send_message_type_list.append([text, '', 'edit_message'])

                text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id])
                temp_list = [text, '', 'message_with_text']
                send_message_type_list.append(temp_list)
                var.enter_mode_counter_step[user_id] = 7

    return send_message_type_list


########################################################################################################################
# Reminder set buttons processing ######################################################################################
########################################################################################################################
def reminder_set_callback_processing(answer_data, user_id):
    send_message_type_list = []

    if var.enter_mode_counter_step[user_id] == 0:
        text = var.dictionary_bot[user_id]['something_happened']
        markup = ''
        temp_list = [text, markup, 'edit_message']
        send_message_type_list.append(temp_list)

    else:
        if answer_data == var.reminder_callback_button_list()[0]:
            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

            var.enter_mode_counter_step[user_id] = 5
            text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id])
            markup = keyboard.inline_keyboard(var.get_frequency_buttons(var.dictionary_bot[user_id]), None, 2)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

        elif answer_data == var.reminder_callback_button_list()[1]:
            text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id] - 1)
            temp_list = [text, '', 'edit_message', user_id, var.message_to_edit[user_id][-1]]
            send_message_type_list.append(temp_list)
            var.entered_data[user_id] += ['0', '0', '0']
            text = var.reply_text_save_add_data(user_id, var.entered_data[user_id], 'yes_allright')
            markup = keyboard.reply_keyboard(var.get_save_final_buttons_list(user_id), 2, True, False)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

            var.enter_mode_counter_step[user_id] = 8

    return send_message_type_list


########################################################################################################################
# Frequency buttons processing #########################################################################################
########################################################################################################################
def frequency_callback_processing(answer_data, user_id):
    send_message_type_list = []

    if var.enter_mode_counter_step[user_id] == 0:
        text = var.dictionary_bot[user_id]['something_happened']
        markup = ''
        temp_list = [text, markup, 'edit_message']
        send_message_type_list.append(temp_list)

    else:
        var.entered_data[user_id].append(var.dictionary_bot[user_id][answer_data])
        text = var.dictionary_bot[user_id]['frequency_is_txt'] + str(var.entered_data[user_id][3])
        markup = ''
        temp_list = [text, markup, 'edit_message']
        send_message_type_list.append(temp_list)
        var.enter_mode_counter_step[user_id] = 6

        text = var.dictionary_bot[user_id]['set_date_of_the_reminder']
        markup = keyboard.inline_keyboard(calendar_buttons_creating(user_id, None, None), None, 7)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

    return send_message_type_list


########################################################################################################################
# Show events buttons processing #######################################################################################
########################################################################################################################
def show_events_callback_processing(answer_data, user_id):
    send_message_type_list = []

    if var.current_user_action_step[user_id] == 'show_events' or var.current_user_action_step[user_id] == 'remove_event'\
            or var.current_user_action_step[user_id] == 'edit_event':

        if answer_data == var.show_event_inline_button_list()[0]:
            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

            text = var.dictionary_bot[user_id]['choose_date_of_the_event_short']
            markup = keyboard.inline_keyboard(calendar_buttons_creating(user_id, None, None), None, 7)

            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

        elif answer_data == var.show_event_inline_button_list()[1]:
            print('kek')
            if var.current_user_action_step[user_id] != 'remove_event' and var.current_user_action_step[user_id] != 'edit_event':
                var.current_user_action_step[user_id] = 'show_event_enter_mode'
            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

            text = var.dictionary_bot[user_id]['enter_date_name_show_events']
            temp_list = [text, '', 'message_with_text']
            send_message_type_list.append(temp_list)

    else:
        text = var.dictionary_bot[user_id]['something_happened']
        markup = ''
        temp_list = [text, markup, 'edit_message']
        send_message_type_list.append(temp_list)

    return send_message_type_list


########################################################################################################################
#  Calendar buttons processing in show event mode ######################################################################
########################################################################################################################
def show_event_mode_calendar_buttons_processing(answer_data, user_id):
    send_message_type_list = []

    # switch months переключение месяцев, получаются текущие установленные год и месяц в боте (из ф-ции
    # создания кнопок календаря) и в ф-ции switch_month происходит увеличение/уменьшение месяца
    if answer_data == 'prev_month' or answer_data == 'next_month':
        year, month = int(var.calendar_current_date[user_id]['year']), \
                      int(var.calendar_current_date[user_id]['month'])

        year, month = switch_month(year, month, str(answer_data))

        text = var.dictionary_bot[user_id]['choose_date_of_the_event_short']
        markup = keyboard.inline_keyboard(calendar_buttons_creating(user_id, year, month), None, 7)
        temp_list = [text, markup, 'edit_message']
        send_message_type_list.append(temp_list)

    elif answer_data == 'year_month':
        year, month = int(var.calendar_current_date[user_id]['year']), \
                      int(var.calendar_current_date[user_id]['month'])
        text = f"{var.dictionary_bot[user_id]['events_for_month']}{var.dictionary_bot[user_id]['month'][int(month)]} " \
               f"{year}"
        markup = ''
        temp_list = [text, markup, 'edit_message']
        send_message_type_list.append(temp_list)

        res = get_select_events_data(user_id, var.calendar_current_date[user_id]['year'],
                                     var.calendar_current_date[user_id]['month'])

        send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

        var.show_month_res[user_id]['res'] = res
        var.show_month_res[user_id]['count'] = len(res)
        var.show_month_res[user_id]['current_counter'] = 0

        text = var.reply_text_save_add_data(user_id, res[0], 'no_allright')
        markup = keyboard.inline_keyboard(var.buttons_check_events(user_id,
                                                                   var.show_month_res[user_id]['current_counter'] + 1,
                                                                   var.show_month_res[user_id]['count']), None, 3)

        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

    # Обработка кнопок календаря (числа)
    else:
        #  идет обрезка кнопки так как она создается с пробелом в начале ' 9' и проверка, является ли цифрой
        if str(answer_data)[1:].isdigit():
            month = var.calendar_current_date[user_id]['month']

            # добавляется нолик к месяцу
            if len(str(month)) == 1:
                month = f"0{month}"
            answer_data = answer_data[1:]

            # добавляется нолик к дню
            if len(str(answer_data)) == 1:
                answer_data = f"0{str(answer_data)}"

            year, month = int(var.calendar_current_date[user_id]['year']), \
                          int(var.calendar_current_date[user_id]['month'])

            res = get_select_events_data(user_id, year, month)
            kek = []
            for i in res:
                if answer_data == i[2][:2]:
                    kek.append(i)
            if kek:
                send_message_type_list.append(['', '', 'delete_message'])
                var.show_month_res[user_id]['res'] = kek
                var.show_month_res[user_id]['count'] = len(kek)
                var.show_month_res[user_id]['current_counter'] = 0

                text = var.reply_text_save_add_data(user_id, kek[0], 'no_allright')
                if var.current_user_action_step[user_id] == 'remove_event':
                    markup = keyboard.inline_keyboard(
                        var.buttons_check_events_remove(user_id, var.show_month_res[user_id]['current_counter'] + 1,
                                                        var.show_month_res[user_id]['count']), None, 3)
                elif var.current_user_action_step[user_id] == 'edit_event':
                    markup = keyboard.inline_keyboard(
                        var.buttons_check_events_edit(user_id, var.show_month_res[user_id]['current_counter'] + 1,
                                                        var.show_month_res[user_id]['count']), None, 3)
                else:
                    markup = keyboard.inline_keyboard(
                        var.buttons_check_events(user_id, var.show_month_res[user_id]['current_counter'] + 1,
                                                 var.show_month_res[user_id]['count']), None, 3)

                temp_list = [text, markup, 'message_with_text']
                send_message_type_list.append(temp_list)

    return send_message_type_list


########################################################################################################################
#  Switch event buttons processing #####################################################################################
########################################################################################################################
def switch_event_button_processing(answer_data, user_id):
    send_message_type_list = []
    print(var.current_user_action_step[user_id])
    if var.current_user_action_step[user_id] != 'show_events' and \
            var.current_user_action_step[user_id] != 'show_event_enter_mode' \
            and var.current_user_action_step[user_id] != 'edit_event' and\
            var.current_user_action_step[user_id] != 'remove_event':
        text = var.dictionary_bot[user_id]['something_happened']
        markup = ''
        temp_list = [text, markup, 'edit_message']
        send_message_type_list.append(temp_list)

    else:
        if answer_data == 'prev_event':

            if var.show_month_res[user_id]['current_counter'] != 0:
                var.show_month_res[user_id]['current_counter'] -= 1
                text = var.reply_text_save_add_data(user_id, var.show_month_res[user_id]['res']
                [var.show_month_res[user_id]['current_counter']], 'no_allright')
                if var.current_user_action_step[user_id] == 'remove_event':
                    markup = keyboard.inline_keyboard(
                        var.buttons_check_events_remove(user_id, var.show_month_res[user_id]['current_counter'] + 1,
                                                        var.show_month_res[user_id]['count']), None, 3)
                elif var.current_user_action_step[user_id] == 'edit_event':
                    markup = keyboard.inline_keyboard(
                        var.buttons_check_events_edit(user_id, var.show_month_res[user_id]['current_counter'] + 1,
                                                        var.show_month_res[user_id]['count']), None, 3)
                else:
                    markup = keyboard.inline_keyboard(
                        var.buttons_check_events(user_id, var.show_month_res[user_id]['current_counter'] + 1,
                                                 var.show_month_res[user_id]['count']), None, 3)

                temp_list = [text, markup, 'edit_message']
                send_message_type_list.append(temp_list)
            else:
                return ''

        elif answer_data == 'next_event':
            if var.show_month_res[user_id]['current_counter'] != var.show_month_res[user_id]['count'] - 1:
                var.show_month_res[user_id]['current_counter'] += 1
                text = var.reply_text_save_add_data(user_id, var.show_month_res[user_id]['res']
                [var.show_month_res[user_id]['current_counter']], 'no_allright')

                if var.current_user_action_step[user_id] == 'remove_event':
                    markup = keyboard.inline_keyboard(
                        var.buttons_check_events_remove(user_id, var.show_month_res[user_id]['current_counter'] + 1,
                                                        var.show_month_res[user_id]['count']), None, 3)
                elif var.current_user_action_step[user_id] == 'edit_event':
                    markup = keyboard.inline_keyboard(
                        var.buttons_check_events_edit(user_id, var.show_month_res[user_id]['current_counter'] + 1,
                                                      var.show_month_res[user_id]['count']), None, 3)
                else:
                    markup = keyboard.inline_keyboard(
                        var.buttons_check_events(user_id, var.show_month_res[user_id]['current_counter'] + 1,
                                                 var.show_month_res[user_id]['count']), None, 3)

                temp_list = [text, markup, 'edit_message']
                send_message_type_list.append(temp_list)
            else:
                return ''

        elif answer_data == 'back_show_event':
            if var.current_user_action_step[user_id] == 'edit_event' or \
                    var.current_user_action_step[user_id] == 'remove_event':
                pass
            else:
                var.current_user_action_step[user_id] = 'show_events'
            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

            text = var.dictionary_bot[user_id]['show_month_events_txt2']
            markup = keyboard.inline_keyboard(var.get_show_events_inline_buttons(user_id), None, 2)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

    return send_message_type_list


def remove_callback_button_processing(user_id):
    send_message_type_list = []

    if var.current_user_action_step[user_id] != 'remove_event':
        text = var.dictionary_bot[user_id]['something_happened']
        markup = ''
        temp_list = [text, markup, 'edit_message']
        send_message_type_list.append(temp_list)

    else:
        text1 = var.show_month_res[user_id]['res'][var.show_month_res[user_id]['current_counter']]
        text = var.reply_text_save_add_data(user_id, text1, 'no_allright')
        text += '\n\n' + var.dictionary_bot[user_id]['remove_event_txt']
        markup = keyboard.inline_keyboard([((var.dictionary_bot[user_id]['yes_btn'], 'yes_btn'), (var.dictionary_bot[user_id]['no_btn'], 'no_btn'))], None, 3)

        temp_list = [text, markup, 'edit_message']
        send_message_type_list.append(temp_list)

    return send_message_type_list


def yes_no_buttons_processing(answer_data, user_id):
    send_message_type_list = []

    if var.current_user_action_step[user_id] != 'remove_event':
        text = var.dictionary_bot[user_id]['something_happened']
        markup = ''
        temp_list = [text, markup, 'edit_message']
        send_message_type_list.append(temp_list)

    elif answer_data == 'yes_btn':
        event_name = var.show_month_res[user_id]['res'][var.show_month_res[user_id]['current_counter']][0]
        date_event = var.show_month_res[user_id]['res'][var.show_month_res[user_id]['current_counter']][2]
        db.delete_values_from_table(f't{user_id}', 'event', event_name, 'date_of_the_event', date_event)

        text = var.dictionary_bot[user_id]['event_deleted_success']
        temp_list = [text, '', 'edit_message']
        send_message_type_list.append(temp_list)

        text = var.dictionary_bot[user_id]['show_month_events_txt2']
        markup = keyboard.inline_keyboard(var.get_show_events_inline_buttons(user_id), None, 2)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

    else:
        text = var.dictionary_bot[user_id]['show_month_events_txt2']
        markup = keyboard.inline_keyboard(var.get_show_events_inline_buttons(user_id), None, 2)
        temp_list = [text, markup, 'edit_message']
        send_message_type_list.append(temp_list)

    return send_message_type_list


def edit_event_callback_button_processing(user_id):
    send_message_type_list = []
    if var.current_user_action_step[user_id] != 'edit_event':
        text = var.dictionary_bot[user_id]['something_happened']
        markup = ''
        temp_list = [text, markup, 'edit_message']
        send_message_type_list.append(temp_list)

    else:
        var.current_user_action_step[user_id] = 'add_edit_event'
        # get enter mode step text by the get_enter_mode function
        text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id])

        markup = keyboard.reply_keyboard([var.dictionary_bot[user_id]['save_current_val'],
                                          var.dictionary_bot[user_id]['main_menu']], 1, True, False)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)
        var.enter_mode[user_id] = True
        var.enter_mode_counter_step[user_id] = 1

    return send_message_type_list
