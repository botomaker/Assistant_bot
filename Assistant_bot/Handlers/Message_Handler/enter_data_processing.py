import PythonFiles.variables as var
from Keyboard import keyboard
from PythonFiles.functions import calendar_buttons_creating, check_datetime_format, set_default_values_entered_mode
import PythonFiles.database as db


def enter_mode_processing(user_id, entered_text):
    send_message_type_list = []
    ######################################################################################################
    ######################################################################################################
    # STEP 1 - Enter short description
    ######################################################################################################
    ######################################################################################################
    if var.enter_mode_counter_step[user_id] == 1:  # STEP 1
        text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id])
        if var.current_user_action_step[user_id] == 'add_edit_event':
            markup = keyboard.reply_keyboard([var.dictionary_bot[user_id]['save_current_val'],
                                              var.dictionary_bot[user_id]['main_menu']], 1, True, False)
        else:
            markup = ''
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

        var.enter_mode_counter_step[user_id] = 2
        if entered_text == var.dictionary_bot[user_id]['save_current_val']:
            event_name = var.show_month_res[user_id]['res'][var.show_month_res[user_id]['current_counter']][0]
            entered_text = event_name
        var.entered_data[user_id].append(entered_text)

    ######################################################################################################
    ######################################################################################################
    # STEP 2 - Set date of the event
    ######################################################################################################
    ######################################################################################################
    elif var.enter_mode_counter_step[user_id] == 2:  # STEP 2
        text = '----'
        if entered_text == var.dictionary_bot[user_id]['save_current_val']:
            event_des = var.show_month_res[user_id]['res'][var.show_month_res[user_id]['current_counter']][1]
            entered_text = event_des
        if var.current_user_action_step[user_id] == 'add_edit_event':
            markup = keyboard.reply_keyboard([var.show_month_res[user_id]['res'][var.show_month_res[user_id]['current_counter']][2],
                                          var.dictionary_bot[user_id]['main_menu']], 1, True, False)
        else:
            markup = ''

        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

        text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id])
        # markup делается inline клавиатурой в виде календаря
        markup = keyboard.inline_keyboard(calendar_buttons_creating(user_id, None, None), None, 7)
        temp_list = [text, markup, 'message_with_text']

        send_message_type_list.append(temp_list)

        var.enter_mode_counter_step[user_id] = 3

        var.entered_data[user_id].append(entered_text)

    ################################################################################################################
    ################################################################################################################
    # STEP 3 - Проверяется введенная дата и в случае успеха изменяется сообщение с календарем(удаляется клавиатура и
    # новая надпись вписывается) и присылается следующее сообщение "выбрать периодичность события"
    ################################################################################################################
    ################################################################################################################
    elif var.enter_mode_counter_step[user_id] == 3:  # STEP 3
        # check data input format
        if check_datetime_format(entered_text, 'date'):

            text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id])
            markup = keyboard.inline_keyboard(var.reminder_callback_button(user_id), None, 2)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

            var.entered_data[user_id].append(entered_text)

            text = var.dictionary_bot[user_id]['selected_date_txt'] + str(var.entered_data[user_id][2])

            temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
            send_message_type_list.append(temp_list)
            var.enter_mode_counter_step[user_id] = 4

        #  if data input is incorrect
        else:
            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

            var.enter_mode_counter_step[user_id] = 3
            text = var.dictionary_bot[user_id]['incorrect_data_format']
            markup = ''
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

            text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id] - 1)
            markup = keyboard.inline_keyboard(calendar_buttons_creating(user_id, None, None), None, 7)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

    ######################################################################################################
    ######################################################################################################
    # STEP 4
    ######################################################################################################
    ######################################################################################################
    elif var.enter_mode_counter_step[user_id] == 4:  # STEP 4

        if str(entered_text).title() in var.reminder_button_list(user_id):
            # if entered text is "set reminder"
            if entered_text.title() == var.reminder_button_list(user_id)[0]:
                text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id])
                markup = keyboard.inline_keyboard(var.get_frequency_buttons(var.dictionary_bot[user_id]), None, 2)
                temp_list = [text, markup, 'message_with_text']
                send_message_type_list.append(temp_list)

                text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id] - 1)
                temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
                send_message_type_list.append(temp_list)

                var.enter_mode_counter_step[user_id] = 5

            elif entered_text.title() == var.reminder_button_list(user_id)[1]:
                text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id] - 1)
                temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
                send_message_type_list.append(temp_list)

                var.entered_data[user_id] += ['0', '0', '0']
                text = var.reply_text_save_add_data(user_id, var.entered_data[user_id],
                                                    'yes_allright')
                markup = keyboard.reply_keyboard(var.get_save_final_buttons_list(user_id), 2, True,
                                                 False)
                temp_list = [text, markup, 'message_with_text']
                send_message_type_list.append(temp_list)

                var.enter_mode_counter_step[user_id] = 8
        else:

            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

            text = var.dictionary_bot[user_id]['reply_answer']
            markup = ''
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

            text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id] - 1)
            markup = keyboard.inline_keyboard(var.reminder_callback_button(user_id), None, 2)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

    ######################################################################################################
    ######################################################################################################
    # STEP 5 - Проверяется корректность данных периодичности события и предлагается выбор даты напоминания
    # (опять календарь создается)
    ######################################################################################################
    ######################################################################################################
    elif var.enter_mode_counter_step[user_id] == 5:  # STEP 5
        if entered_text.lower() in var.frequency_buttons_list(user_id):

            text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id])
            markup = keyboard.inline_keyboard(calendar_buttons_creating(user_id, None, None), None, 7)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

            var.entered_data[user_id].append(entered_text.lower())

            text = var.dictionary_bot[user_id]['frequency_is_txt'] + str(var.entered_data[user_id][3])
            temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
            send_message_type_list.append(temp_list)

            var.enter_mode_counter_step[user_id] = 6

        else:
            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

            var.enter_mode_counter_step[user_id] = 5
            text = var.dictionary_bot[user_id]['enter_correct_frequency']
            markup = ''
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

            text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id] - 1)
            markup = keyboard.inline_keyboard(var.get_frequency_buttons(var.dictionary_bot[user_id]), None, 2)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

    ####################################################################################################################
    ####################################################################################################################
    # STEP 6 - Проверется введенная дата напоминания, в случае  успеха изменяется сообщение с календарем(удаляется
    # клавиатура и новая надпись вписывается) и присылается следующее сообщение "Укажите время напоминания в формате..."
    ####################################################################################################################
    ####################################################################################################################
    elif var.enter_mode_counter_step[user_id] == 6:  # STEP 6
        if check_datetime_format(entered_text, 'date'):
            text = var.dictionary_bot[user_id]['enter_time_of_the_rimender']
            temp_list = [text, '', 'message_with_text']
            send_message_type_list.append(temp_list)

            var.entered_data[user_id].append(entered_text)  # эта переменная сохраняет введенные пользователем значения

            text = var.dictionary_bot[user_id]['reminder_date_is_txt'] + str(var.entered_data[user_id][4])

            temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
            send_message_type_list.append(temp_list)
            var.enter_mode_counter_step[user_id] = 7
        else:
            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

            var.enter_mode_counter_step[user_id] = 6
            text = var.dictionary_bot[user_id]['enter_correct_date_reminder']
            markup = ''
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

            text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id] - 1)
            markup = keyboard.inline_keyboard(calendar_buttons_creating(user_id, None, None), None, 7)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

    ##################################################################################################################
    ##################################################################################################################
    # ЗРОБИТИ ОБРОБКУ
    # STEP 7 - Проверется введенное время напоминания и в случе успеха присылается финальная фраза режима ввода данных
    ##################################################################################################################
    ##################################################################################################################
    elif var.enter_mode_counter_step[user_id] == 7:  # STEP 7
        if check_datetime_format(entered_text, 'time'):
            var.entered_data[user_id].append(entered_text)  # эта переменная сохраняет введенные пользователем значения

            text = var.reply_text_save_add_data(user_id, var.entered_data[user_id], 'yes_allright')
            markup = keyboard.reply_keyboard(var.get_save_final_buttons_list(user_id), 2, True, False)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

            var.enter_mode_counter_step[user_id] = 8
        else:
            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

            var.enter_mode_counter_step[user_id] = 7
            text = var.dictionary_bot[user_id]['enter_correct_time']
            markup = ''
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

            text = var.dictionary_bot[user_id]['enter_time_of_the_rimender']
            temp_list = [text, '', 'message_with_text']
            send_message_type_list.append(temp_list)

    else:
        if entered_text == var.dictionary_bot[user_id]['yes_btn']:
            if var.current_user_action_step[user_id] == 'add_edit_event':
                event_name = var.show_month_res[user_id]['res'][var.show_month_res[user_id]['current_counter']][0]
                date_event = var.show_month_res[user_id]['res'][var.show_month_res[user_id]['current_counter']][2]
                print(event_name)
                print(date_event)
                db.delete_values_from_table(f't{user_id}', 'event', event_name, 'date_of_the_event', date_event)

                text = var.dictionary_bot[user_id]['event_edited_text']

            else:
                text = var.dictionary_bot[user_id]['save_event_final_text']

            markup = keyboard.reply_keyboard(var.main_menu_buttons(user_id), 2, True, False)
            temp_list = [text, markup, 'message_with_text']
            send_message_type_list.append(temp_list)

            if var.entered_data[user_id][3] != '0':
                frequency = var.frequency_buttons_dict(user_id, var.entered_data[user_id][3])
            else:
                frequency = '0'

            db.insert_values_in_table(f"t{user_id}", var.get_user_personal_table_columns(),
                                      f"'{var.entered_data[user_id][0]}', "
                                      f"'{var.entered_data[user_id][1]}', "
                                      f"'{var.entered_data[user_id][2]}', "
                                      f"'{frequency}', "
                                      f"'{var.entered_data[user_id][4]}', "
                                      f"'{var.entered_data[user_id][5]}'")

            set_default_values_entered_mode(user_id, 'forced_update')

        else:
            set_default_values_entered_mode(user_id, 'forced_update')
            text = var.dictionary_bot[user_id]['reply_answer']
            markup = keyboard.reply_keyboard(var.main_menu_buttons(user_id), 2, True, False)
            temp_list = [text, markup, 'reply_message']
            send_message_type_list.append(temp_list)

    return send_message_type_list


def enter_mode_show_events(user_id, entered_text):
    send_message_type_list = []
    res1 = db.select_values_from_table(f't{user_id}', '*', 'date_of_the_event', entered_text, 'yes')
    res2 = db.select_values_from_table(f't{user_id}', '*', 'event', entered_text, 'yes')
    res = res1 + res2
    var.show_month_res[user_id]['res'] = res
    var.show_month_res[user_id]['count'] = len(res)
    var.show_month_res[user_id]['current_counter'] = 0

    send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

    if len(res) > 0:
        text = var.reply_text_save_add_data(user_id, res[0], 'no_allright')
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
    else:
        text = var.dictionary_bot[user_id]['nothing_find']

        markup = keyboard.inline_keyboard(([[var.dictionary_bot[user_id]['back_button'], 'back_show_event']]), None, 1)
        temp_list = [text, markup, 'message_with_text']

    send_message_type_list.append(temp_list)

    return send_message_type_list
