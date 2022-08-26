import Keyboard.keyboard as keyboard
import PythonFiles.variables as var
from Handlers.Message_Handler.enter_data_processing import enter_mode_processing, enter_mode_show_events
from Handlers.Message_Handler.reply_buttons_processing import process_menu_buttons_handler, process_main_menu_button
from PythonFiles.send_message import message_with_text, simple_message, reply_message, delete_message, edit_message
from PythonFiles.functions import set_default_values_entered_mode, print_info


async def message_handler(bot, message, user_id):
    # setting default values (if bot has stopped)
    set_default_values_entered_mode(user_id, 'default_update')

    send_message_type_list = []  # variable which get message to send in type of list (there may be several messages)
    sent_message = ''  # helping variable to store message

    # delete message with choosing language if current_user_step is "change_language_button"
    if var.current_user_action_step[user_id] == 'change_language_button':
        text = var.dictionary_bot[user_id]['current_language_message']
        temp_list = [text, '', 'edit_message_text', user_id, var.message_to_edit[user_id][-1]]
        send_message_type_list.append(temp_list)

    ####################################################################################################################
    # Main menu button #################################################################################################
    ####################################################################################################################
    if message.text == var.dictionary_bot[user_id]['main_menu']:
        # delete last message if it was enter mode before
        if len(var.message_to_edit[user_id]) > 0 and (var.current_user_action_step[user_id] == 'add_event' or
                                                      var.current_user_action_step[user_id] == 'edit_event' or
                                                      var.current_user_action_step[user_id] == 'remove_event' or
                                                      var.current_user_action_step[user_id] == 'show_events' or
                                                      var.current_user_action_step[user_id] == 'show_event_enter_mode'):
            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

        set_default_values_entered_mode(user_id, 'forced_update')
        send_message_type_list += process_main_menu_button(user_id, message.text)

    ####################################################################################################################
    # Menu buttons processing ##########################################################################################
    ####################################################################################################################
    elif message.text in var.get_menu_buttons_list(user_id):
        # delete last message if it was enter mode before
        if len(var.message_to_edit[user_id]) > 0 and var.current_user_action_step[user_id] == 'add_event':
            send_message_type_list.append([var.message_to_edit[user_id][-1], '', 'delete_message'])

        set_default_values_entered_mode(user_id, 'forced_update')
        send_message_type_list += process_menu_buttons_handler(message, var.language_var[user_id], user_id)

    ####################################################################################################################
    # Enter mode processing ############################################################################################
    ####################################################################################################################
    elif var.enter_mode[user_id]:
        send_message_type_list += enter_mode_processing(user_id, message.text)

    elif var.current_user_action_step[user_id] == 'show_event_enter_mode' or var.current_user_action_step[user_id] == \
            'remove_event' or var.current_user_action_step[user_id] == 'edit_event':
        send_message_type_list += enter_mode_show_events(user_id, message.text)
    ####################################################################################################################
    # Random words #####################################################################################################
    # Answer with reply message to random words ########################################################################
    ####################################################################################################################
    else:
        text = var.dictionary_bot[user_id]['reply_answer']
        markup = keyboard.reply_keyboard(var.main_menu_buttons(user_id), 2, True, False)
        temp_list = [text, markup, "reply_message"]
        send_message_type_list.append(temp_list)

    ####################################################################################################################
    # Send message block ###############################################################################################
    ####################################################################################################################
    for i in send_message_type_list:
        try:
            if i[2] == "edit_message_text":
                sent_message = edit_message(bot, i[3], i[4], i[0], i[1])
            elif i[2] == "message_with_text":
                sent_message = message_with_text(bot, message, i[0], i[1])
            elif i[2] == "simple_message":
                sent_message = simple_message(bot, user_id, i[0], i[1])
            elif i[2] == "reply_message":
                sent_message = reply_message(message, i[0], i[1])
            elif i[2] == 'delete_message':
                sent_message = delete_message(bot, user_id, i[0])

            await sent_message

        except BaseException:
            pass

    print_info(user_id)
