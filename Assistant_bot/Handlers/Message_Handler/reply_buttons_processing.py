from PythonFiles.functions import get_select_event_count
from PythonFiles.variables import main_menu_buttons, settings_menu_buttons, events_menu_buttons, \
    languages_callback_button_tuples
import Keyboard.keyboard as keyboard
import PythonFiles.variables as var


########################################################################################################################
# Processing menu buttons ##############################################################################################
########################################################################################################################
def process_menu_buttons_handler(message, language, user_id):
    send_message_type_list = []
    # about bot button
    if message.text == var.dictionary_bot[user_id]['aboutbot_button']:
        text = var.dictionary_bot[user_id]['aboutbot_text']
        markup = keyboard.reply_keyboard([var.dictionary_bot[user_id]['back_button']], 2, True, False)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

    # back button
    elif message.text == var.dictionary_bot[user_id]['back_button']:
        text = message.text
        markup = keyboard.reply_keyboard(main_menu_buttons(user_id), 2, True, False)
        temp_list = [text, markup, 'simple_message']
        send_message_type_list.append(temp_list)

    # settings button
    elif message.text == var.dictionary_bot[user_id]['settings_button']:
        text = message.text
        markup = keyboard.reply_keyboard(settings_menu_buttons(user_id), 2, True, True)
        temp_list = [text, markup, 'simple_message']
        send_message_type_list.append(temp_list)

    # change language button
    elif message.text == var.dictionary_bot[user_id]['change_language_button']:
        var.current_user_action_step[user_id] = 'change_language_button'  # set current user step

        text = var.dictionary_bot[user_id]['current_language_message']
        markup = keyboard.inline_keyboard(languages_callback_button_tuples(user_id, language), None, 3)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

    # events button
    elif message.text == var.dictionary_bot[user_id]['events_button']:
        text = message.text
        markup = keyboard.reply_keyboard(events_menu_buttons(user_id), 3, True, False)
        temp_list = [text, markup, 'simple_message']
        send_message_type_list.append(temp_list)

    # add_event button
    elif message.text == var.dictionary_bot[user_id]['add_event']:
        var.current_user_action_step[user_id] = 'add_event'  # set current user step

        # get enter mode step text by the get_enter_mode function
        text = var.enter_mode_text(user_id, var.enter_mode_counter_step[user_id])
        markup = keyboard.reply_keyboard(var.dictionary_bot[user_id]['main_menu'], 1, True, False)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)
        var.enter_mode[user_id] = True
        var.enter_mode_counter_step[user_id] = 1

    elif message.text == var.dictionary_bot[user_id]['show_events']:
        var.current_user_action_step[user_id] = 'show_events'

        count_of_event = get_select_event_count(user_id)

        text = f"{var.dictionary_bot[user_id]['show_month_events_txt1']} {count_of_event}{var.notes_smile}"
        markup = keyboard.reply_keyboard(var.dictionary_bot[user_id]['main_menu'], 1, True, True)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

        text = var.dictionary_bot[user_id]['show_month_events_txt2']
        markup = keyboard.inline_keyboard(var.get_show_events_inline_buttons(user_id), None, 2)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

    elif message.text == var.dictionary_bot[user_id]['edit_event']:
        var.current_user_action_step[user_id] = 'edit_event'

        count_of_event = get_select_event_count(user_id)

        text = f"{var.dictionary_bot[user_id]['show_month_events_txt1']} {count_of_event}{var.notes_smile}"
        markup = keyboard.reply_keyboard(var.dictionary_bot[user_id]['main_menu'], 1, True, True)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

        text = var.dictionary_bot[user_id]['show_month_events_txt2']
        markup = keyboard.inline_keyboard(var.get_show_events_inline_buttons(user_id), None, 2)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

    elif message.text == var.dictionary_bot[user_id]['remove_event']:
        var.current_user_action_step[user_id] = 'remove_event'

        count_of_event = get_select_event_count(user_id)

        text = f"{var.dictionary_bot[user_id]['show_month_events_txt1']} {count_of_event}{var.notes_smile}"
        markup = keyboard.reply_keyboard(var.dictionary_bot[user_id]['main_menu'], 1, True, True)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

        text = var.dictionary_bot[user_id]['show_month_events_txt2']
        markup = keyboard.inline_keyboard(var.get_show_events_inline_buttons(user_id), None, 2)
        temp_list = [text, markup, 'message_with_text']
        send_message_type_list.append(temp_list)

    return send_message_type_list


########################################################################################################################
# Processing main menu button ##########################################################################################
########################################################################################################################
def process_main_menu_button(user_id, text):
    send_message_type_list = []
    markup = keyboard.reply_keyboard(var.main_menu_buttons(user_id), 2, True, False)
    temp_list = [text, markup, 'simple_message']
    send_message_type_list.append(temp_list)

    try:
        send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])
    except BaseException:
        pass

    return send_message_type_list
