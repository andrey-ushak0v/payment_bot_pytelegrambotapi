import os
import re

import telebot
from flask import Flask, Response, request
from telebot import types

from actions.card_actions import get_card_info, get_my_cards
from actions.repl_actions import check_repl, repl_to_db
from actions.transaction_actions import (check_transaction_owner,
                                         transaction_to_db)
from actions.user_actions import (check_status, check_user, update_status,
                                  user_to_db)
from actions.users_data_actions import (user_name_to_db, user_p_num_to_db,
                                        user_photo_to_db, user_selphe_to_db)
from change_keys import change_keys
from conf import BOT_TOKEN, ENDPOINT_CARD_BALANCE, ENDPOINT_CARD_DETAIL
from loger_conf import logger
from text import (hello_new_user, instructiom_ph_psprt,
                  instruction_application, instruction_auth,
                  instruction_balance, instruction_conditions,
                  instruction_finish_auth, instruction_psprt_name,
                  instruction_psprt_number, instruction_rate,
                  instruction_selphe, instruction_status, instruction_support,
                  instructions_put_on)

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.headers.get('content-type') == 'application/json':
        update = types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return Response('ok', status=200)


@app.route('/callback', methods=['POST'])
def callback():
    data = request.json
    transaction_to_db(
        data['transaction_id'],
        data['transaction_amount'],
        data['status'],
        data['transaction_type'],
        data['card_id']
    )
    user_id = check_transaction_owner(data['card_id'])
    bot.send_message(chat_id=user_id,
                     text=f'{data["transaction_type"]}\
 на {data["transaction_amount"]} {data["transaction_currency"]}')
    return Response('ok', status=200)


@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.first_name
    tg_id = message.from_user.id
    if not check_user(tg_id):
        user_to_db(tg_id)
        markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True,
                row_width=2
                )
        button_1 = types.KeyboardButton('Открыть карту')
        button_2 = types.KeyboardButton('Условия')
        button_3 = types.KeyboardButton('Помощь')
        button_4 = types.KeyboardButton('Мой статус')
        markup.add(button_1, button_2, button_3, button_4)
        bot.send_message(message.chat.id,
                         f'Здравствуйте {username}. {hello_new_user}',
                         reply_markup=markup)

    elif check_user(tg_id) == tg_id:
        if check_status(tg_id) != 'has_card':
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True,
                row_width=2
                )
            button_1 = types.KeyboardButton('Открыть карту')
            button_2 = types.KeyboardButton('Условия')
            button_3 = types.KeyboardButton('Помощь')
            button_4 = types.KeyboardButton('Мой статус')
            markup.add(button_1, button_2, button_3, button_4)
            bot.send_message(message.chat.id,
                             f'Здравствуйте {username}. {hello_new_user}',
                             reply_markup=markup)

        elif check_status(tg_id) == 'has_card':
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True,
                row_width=2
                )
            button_1 = types.KeyboardButton('Узнать баланс')
            button_2 = types.KeyboardButton('Пополнить карту')
            button_3 = types.KeyboardButton('Реквизиты карты')
            button_4 = types.KeyboardButton('Помощь')

            markup.add(button_1, button_2, button_3, button_4)
            card = get_my_cards(tg_id)
            bot.send_message(
                message.chat.id,
                f'Здравствуйте {username}! Ваша \
карта {card[3]}-{card[2]} активна',
                reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        tg_id = message.from_user.id

        if message.text == 'Помощь':
            if check_status(tg_id) == 'has_card':
                markup = types.ReplyKeyboardMarkup(
                    resize_keyboard=True,
                    row_width=2
                    )
                button_1 = types.KeyboardButton('Тариф')
                button_2 = types.KeyboardButton('В главное меню')
                markup.add(button_1, button_2)
                bot.send_message(
                    message.chat.id,
                    instruction_support,
                    reply_markup=markup)
            else:
                bot.send_message(
                    message.chat.id,
                    instruction_support)

        elif message.text == 'В главное меню':
            if check_status(tg_id) == 'has_card':
                markup = types.ReplyKeyboardMarkup(
                    resize_keyboard=True,
                    row_width=2
                    )
                button_1 = types.KeyboardButton('Узнать баланс')
                button_2 = types.KeyboardButton('Пополнить карту')
                button_3 = types.KeyboardButton('Реквизиты карты')
                button_4 = types.KeyboardButton('Помощь')
                markup.add(button_1, button_2, button_3, button_4)
                bot.send_message(message.chat.id,
                                 'В главное меню',
                                 reply_markup=markup)
            else:
                markup = types.ReplyKeyboardMarkup(
                    resize_keyboard=True,
                    row_width=2
                )
                button_1 = types.KeyboardButton('Открыть карту')
                button_2 = types.KeyboardButton('Условия')
                button_3 = types.KeyboardButton('Помощь')
                button_4 = types.KeyboardButton('Мой статус')
                markup.add(button_1, button_2, button_3, button_4)
                bot.send_message(message.chat.id,
                                 'В главное меню',
                                 reply_markup=markup)

        elif message.text == 'Пополнить карту':
            sent = bot.send_message(message.chat.id, instruction_balance)
            bot.register_next_step_handler(sent, review)

        elif message.text == 'Тариф':
            bot.send_message(message.chat.id, instruction_rate)

        elif message.text == 'Реквизиты карты':
            endpoint = (ENDPOINT_CARD_DETAIL + get_my_cards(tg_id)[0])
            info = get_card_info(endpoint)
            for key in change_keys(info):
                bot.send_message(
                    message.chat.id,
                    f'{key}\n\n{change_keys(info)[key]}'
                    )

        elif message.text == 'Узнать баланс':
            endpoint = (ENDPOINT_CARD_BALANCE + get_my_cards(tg_id)[0])
            info = get_card_info(endpoint)
            balance = info['balance']['available']
            bot.send_message(
                    message.chat.id,
                    f'баланс вашей карты:\n{balance} '
            )

        elif message.text == 'Мой статус':
            bot.send_message(message.chat.id, instruction_status)

        elif message.text == 'Условия':
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True,
                row_width=2
                )
            button_1 = types.KeyboardButton('Открыть карту')
            button_2 = types.KeyboardButton('В главное меню')
            markup.add(button_1, button_2)
            bot.send_message(
                message.chat.id,
                instruction_conditions,
                reply_markup=markup)

        elif message.text == 'Открыть карту':
            update_status(tg_id, 'pressed_card')
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True,
                row_width=2,
                one_time_keyboard=True
                )
            button_1 = types.KeyboardButton('Продолжить')
            button_2 = types.KeyboardButton('В главное меню')
            markup.add(button_1, button_2)
            bot.send_message(message.chat.id,
                             instruction_application,
                             reply_markup=markup)

        elif message.text == 'Продолжить':
            if check_status != 'has_card':
                update_status(tg_id, 'start_payment')
            sent = bot.send_message(message.chat.id, instruction_balance)
            bot.register_next_step_handler(sent, review)

        elif message.text == 'Начать идентификацию':
            update_status(tg_id, 'stared_auth')
            sent = bot.send_message(message.chat.id, instruction_psprt_name)
            bot.register_next_step_handler(sent, user_answer_name)


def review(message):
    tg_id = message.from_user.id
    msg = message.text
    if re.match(r'[A-Za-z0-9]{10}', msg) and len(msg) == 10:
        tg_id = message.from_user.id
        if check_status(tg_id) == 'has_card':
            pay_type = 'top_up'
            repl_to_db(msg, pay_type, tg_id)
            bot.send_message(message.chat.id, instructions_put_on)
        else:
            pay_type = 'new_card'
            repl_to_db(msg, pay_type, tg_id)
            if check_repl(tg_id, msg):
                update_status(tg_id, 'finished_payment')
                markup = types.ReplyKeyboardMarkup(
                                resize_keyboard=True,
                                row_width=2,
                                one_time_keyboard=True
                            )
                button_1 = types.KeyboardButton('Начать идентификацию')
                button_2 = types.KeyboardButton('В главное меню')
                markup.add(button_1, button_2)
                bot.send_message(message.chat.id,
                                 instruction_auth,
                                 reply_markup=markup)
    else:
        logger.warning('ввод невалидного значения')
        sent = bot.send_message(
            message.chat.id,
            'невалидное значение, попробуйте еще раз'
            )
        bot.register_next_step_handler(sent, review)


def user_answer_name(message):
    msg = message.text
    tg_id = message.from_user.id
    if re.match(r'[A-Z]', msg):
        user_name_to_db(msg, tg_id)
        sent = bot.send_message(message.chat.id, instruction_psprt_number)
        bot.register_next_step_handler(sent, user_answer_psprt)
    else:
        sent = bot.send_message(message.chat.id, 'невалидное имя')
        bot.register_next_step_handler(sent, user_answer_name)


def user_answer_psprt(message):
    msg = message.text
    tg_id = message.from_user.id
    user_p_num_to_db(msg, tg_id)
    if re.match(r'[0-9]{10}', msg):
        sent = bot.send_message(message.chat.id, instructiom_ph_psprt)
        bot.register_next_step_handler(sent, user_answer_psprt_ph)
    else:
        sent = bot.send_message(message.chat.id, 'невалидный номер паспорта,\
                             попробуйте еще раз')
        bot.register_next_step_handler(sent, user_answer_psprt)


def user_answer_psprt_ph(message):
    tg_id = message.from_user.id
    if message.content_type == 'photo':
        photo_id = message.photo[-1].file_id
        save_to_photos(message, photo_id)
        user_photo_to_db(photo_id, tg_id)
        sent = bot.send_message(message.chat.id, instruction_selphe)
        bot.register_next_step_handler(sent, user_answer_selphe)
    else:
        sent = bot.send_message(
            message.chat.id,
            'вы прислали не фото попробуйте еще раз'
                )
        bot.register_next_step_handler(sent, user_answer_psprt_ph)


def user_answer_selphe(message):
    tg_id = message.from_user.id
    if message.content_type == 'photo':
        photo_id = message.photo[-1].file_id
        save_to_photos(message, photo_id)
        user_selphe_to_db(photo_id, tg_id)
        update_status(tg_id, 'finished_auth')
        markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True,
                row_width=2
                )
        button_1 = types.KeyboardButton('В главное меню')
        markup.add(button_1)
        bot.send_message(message.chat.id,
                         instruction_finish_auth,
                         reply_markup=markup)
    else:
        sent = bot.send_message(
            message.chat.id,
            'вы прислали не фото, попробуйте еще раз'
            )
        bot.register_next_step_handler(sent, user_answer_selphe)


def save_to_photos(message, photo_id):
    file_ph = bot.get_file(photo_id)
    filename, file_extention = os.path.splitext(file_ph.file_path)
    downloaded_file_ph = bot.download_file(file_ph.file_path)
    src = 'photos/' + photo_id + file_extention   
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file_ph)


if __name__ == '__main__':
    app.run()
