import PythonFiles.variables as var
from Handlers.Callback_Handlers.callback_buttons_processing import language_callback_buttons_processing, \
    main_menu_callback_button_processing, add_mode_calendar_buttons_processing, reminder_set_callback_processing, \
    frequency_callback_processing, show_events_callback_processing, show_event_mode_calendar_buttons_processing, \
    switch_event_button_processing, remove_callback_button_processing, yes_no_buttons_processing, \
    edit_event_callback_button_processing
from PythonFiles.send_message import simple_message, message_with_text, delete_message, edit_message
from PythonFiles.functions import set_default_values_entered_mode, print_info


async def callback_handler_processing(bot, query, answer_data, user_id):
    set_default_values_entered_mode(user_id, 'default_update')

    send_message_type_list = []
    sent_message = ''

    ####################################################################################################################
    #  language settings ###############################################################################################
    ####################################################################################################################
    if answer_data in var.get_language_callback_button_list():
        send_message_type_list = language_callback_buttons_processing(answer_data, user_id)

    ####################################################################################################################
    #  calendar's buttons processing ###################################################################################
    ####################################################################################################################
    elif answer_data in var.get_calendar_callback_button_list():
        if var.current_user_action_step[user_id] == 'add_event' or var.current_user_action_step[user_id] == 'add_edit_event':
            send_message_type_list = add_mode_calendar_buttons_processing(answer_data, user_id)
        elif var.current_user_action_step[user_id] == 'show_events' or \
                var.current_user_action_step[user_id] == 'remove_event' or \
                var.current_user_action_step[user_id] == 'edit_event':
            send_message_type_list = show_event_mode_calendar_buttons_processing(answer_data, user_id)

        else:
            if var.enter_mode_counter_step[user_id] == 0:
                text = var.dictionary_bot[user_id]['something_happened']
                markup = ''
                temp_list = [text, markup, 'edit_message']
                send_message_type_list.append(temp_list)

    ####################################################################################################################
    #  set reminder buttons processing #################################################################################
    ####################################################################################################################
    elif answer_data in var.reminder_callback_button_list():
        send_message_type_list = reminder_set_callback_processing(answer_data, user_id)

    ####################################################################################################################
    #  choose frequency buttons processing #############################################################################
    ####################################################################################################################
    elif answer_data in var.frequency_callback_buttons_list():
        send_message_type_list = frequency_callback_processing(answer_data, user_id)

    ####################################################################################################################
    #  show events buttons processing ##################################################################################
    ####################################################################################################################
    elif answer_data in var.show_event_inline_button_list():
        send_message_type_list = show_events_callback_processing(answer_data, user_id)

    ####################################################################################################################
    #  switch events buttons processing ################################################################################
    ####################################################################################################################
    elif answer_data in var.get_buttons_check_events_list():
        send_message_type_list = switch_event_button_processing(answer_data, user_id)

    elif answer_data == 'remove_event_short':
        send_message_type_list = remove_callback_button_processing(user_id)

    elif answer_data == 'edit_event_short':
        send_message_type_list = edit_event_callback_button_processing(user_id)

    elif answer_data == 'yes_btn' or answer_data == 'no_btn':
        send_message_type_list = yes_no_buttons_processing(answer_data, user_id)

    ####################################################################################################################
    #  main menu inline keyboard #######################################################################################
    ####################################################################################################################
    elif answer_data == 'main_menu':
        send_message_type_list = main_menu_callback_button_processing(user_id)

    ####################################################################################################################
    #  send message block ##############################################################################################
    ####################################################################################################################
    for i in send_message_type_list:
        if i[2] == "edit_message":
            sent_message = edit_message(bot, query.from_user.id, query.message.message_id, i[0], i[1])
        elif i[2] == "simple_message":
            sent_message = simple_message(bot, query.from_user.id, i[0], i[1])
        elif i[2] == "message_with_text":
            sent_message = message_with_text(bot, query, i[0], i[1])
        elif i[2] == 'delete_message':
            sent_message = delete_message(bot, query.from_user.id, query.message.message_id)

        await sent_message

    print_info(user_id)
