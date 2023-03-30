import re

import telebot
from telebot import types
from loger_conf import logger

from card_actions import get_card_info, get_my_cards
from change_keys import change_keys
from conf import BOT_TOKEN, ENDPOINT_CARD_BALANCE, ENDPOINT_CARD_DETAIL
from repl_actions import repl_to_db
from text import (hello_new_user, instruction_balance, instruction_rate,
                  instruction_support, instructions_put_on, instruction_status,
                  instruction_conditions)
from user_actions import check_status, check_user, user_to_db

bot = telebot.TeleBot(BOT_TOKEN)


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
                         f'привет {username}. {hello_new_user}',
                         reply_markup=markup)

    elif check_user(tg_id) == tg_id:
        if check_status(tg_id) == 'new_user':
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
                             f'привет {username}. {hello_new_user}',
                             reply_markup=markup)

        elif check_status(tg_id) == 'has_card':
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True,
                row_width=2
                )
            button_1 = types.KeyboardButton('Помощь')
            button_2 = types.KeyboardButton('Узнать баланс')
            button_3 = types.KeyboardButton('Мои карты')
            button_4 = types.KeyboardButton('Реквизиты карты')
            button_5 = types.KeyboardButton('Пополнить карту')

            markup.add(button_1, button_2, button_3, button_4, button_5)
            bot.send_message(
                message.chat.id,
                'привет {0.first_name}'.format(message.from_user),
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
                button_2 = types.KeyboardButton('Назад')
                markup.add(button_1, button_2)
                bot.send_message(
                    message.chat.id,
                    instruction_support,
                    reply_markup=markup)
            else:
                bot.send_message(
                    message.chat.id,
                    instruction_support)

        elif message.text == 'Мои карты':
            card = get_my_cards(tg_id)
            bot.send_message(
                message.chat.id,
                f'у вас оформлена карта - {card[3]} {card[2]}'
                )

        elif message.text == 'Назад':
            if check_status(tg_id) == 'has_card':
                markup = types.ReplyKeyboardMarkup(
                    resize_keyboard=True,
                    row_width=2
                    )
                button_1 = types.KeyboardButton('Помощь')
                button_2 = types.KeyboardButton('Узнать баланс')
                button_3 = types.KeyboardButton('Мои карты')
                button_4 = types.KeyboardButton('Реквизиты карты')
                button_5 = types.KeyboardButton('Пополнить карту')
                markup.add(button_1, button_2, button_3, button_4, button_5)
                bot.send_message(message.chat.id, 'Назад', reply_markup=markup)

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
                bot.send_message(message.chat.id, 'Назад', reply_markup=markup)

        elif message.text == 'Пополнить карту':
            sent = bot.reply_to(message, instruction_balance)
            bot.register_next_step_handler(sent, review)

        elif message.text == 'Тариф':
            bot.send_message(message.chat.id, instruction_rate)

        elif message.text == 'Реквизиты карты':
            endpoint = (ENDPOINT_CARD_DETAIL + get_my_cards(tg_id)[0])
            info = get_card_info(endpoint)
            bot.send_message(
                message.chat.id,
                f'реквизиты {get_my_cards(tg_id)[3]}-{get_my_cards(tg_id)[2]}:'
                )
            for key in change_keys(info):
                bot.send_message(
                    message.chat.id,
                    f'{key} - {change_keys(info)[key]}')

        elif message.text == 'Узнать баланс':
            endpoint = (ENDPOINT_CARD_BALANCE + get_my_cards(tg_id)[0])
            info = get_card_info(endpoint)
            balance = info['balance']['available']
            bot.send_message(
                    message.chat.id,
                    f'ваш баланс {balance} доллара'
            )

        elif message.text == 'Мой статус':
            bot.send_message(message.chat.id, instruction_status)

        elif message.text == 'Условия':
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True,
                row_width=2
                )
            button_1 = types.KeyboardButton('Открыть карту')
            button_2 = types.KeyboardButton('Назад')
            markup.add(button_1, button_2)
            bot.send_message(
                message.chat.id,
                instruction_conditions,
                reply_markup=markup)
        

def review(message):
    msg = message.text
    if re.match(r'[A-Za-z0-9]{10}', msg) and len(msg) == 10:
        tg_id = message.from_user.id
        if check_status(tg_id) == 'has_card':
            pay_type = 'top_up'
        else:
            pay_type = 'new_card'
        repl_to_db(msg, pay_type, tg_id)
        bot.send_message(message.chat.id, instructions_put_on)
    else:
        logger.warning('ввод невалидного значения')
        bot.send_message(
            message.chat.id,
            'невалидное значение, попробуйте еще раз')


bot.polling(non_stop=True)
