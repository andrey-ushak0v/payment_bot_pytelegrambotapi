import telebot
from telebot import types

from conf import BOT_TOKEN, ENDPOINT_CARD_DETAIL, ENDPOINT_CARD_BALANCE
from card_actions import get_my_cards, get_card_info
from user_actions import user_to_db, check_user, check_status
from text import (instruction_balance,
                  instruction_support,
                  hello_new_user,
                  instruction_rate,
                  instructions_put_on)

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.first_name
    tg_id = message.from_user.id
    if not check_user(tg_id):
        user_to_db(tg_id)
        bot.send_message(message.chat.id,
                         f'привет {username}. {hello_new_user}')
    elif check_user(tg_id) == tg_id:
        if check_status(tg_id) == 'new_user':
            bot.send_message(message.chat.id,
                             f'привет {username}. {hello_new_user}')
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

        elif message.text == 'Мои карты':
            card = get_my_cards(tg_id)
            bot.send_message(
                message.chat.id,
                f'у вас оформлена карта - {card[3]} {card[2]}'
                )

        elif message.text == 'Назад':
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

        elif message.text == 'Пополнить карту':
            bot.send_message(message.chat.id, instruction_balance)
            if message.text == 'MYHASH' + r'[a-zA-Z0-9]{10}':
                bot.send_message(message.chat.id, instructions_put_on)

        elif message.text == 'Тариф':
            bot.send_message(message.chat.id, instruction_rate)

        elif message.text == 'Реквизиты карты':
            endpoint = (ENDPOINT_CARD_DETAIL + get_my_cards(tg_id)[0])
            info = get_card_info(endpoint)
            bot.send_message(
                message.chat.id,
                f'реквизиты {get_my_cards(tg_id)[3]}-{get_my_cards(tg_id)[2]}:'
                )
            for key in info:
                bot.send_message(
                    message.chat.id,
                    f'{key} - {info[key]}')

        elif message.text == 'Узнать баланс':
            endpoint = (ENDPOINT_CARD_BALANCE + get_my_cards(tg_id)[0])
            info = get_card_info(endpoint)
            balance = info['balance']['available']
            bot.send_message(
                    message.chat.id,
                    f'ваш баланс {balance} доллара'
            )


bot.polling(non_stop=True)
