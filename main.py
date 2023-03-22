from config import BOT_TOKEN, ENDPOINT_CARD_DETAIL
import telebot
from telebot import types
from text import instruction_balance, instruction_card
from my_cards import get_my_cards
from get_card_info import get_card_info


bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_1 = types.KeyboardButton('Как открыть карту?')
    button_2 = types.KeyboardButton('Как пополнить баланс?')
    button_3 = types.KeyboardButton('Мои карты')
    button_4 = types.KeyboardButton('Информация о карте')

    markup.add(button_1, button_2, button_3, button_4)
    bot.send_message(message.chat.id, 'привет {0.first_name}'.format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Как открыть карту?':
            bot.send_message(message.chat.id, instruction_card)
        
        elif message.text == 'Как пополнить баланс?':
            bot.send_message(message.chat.id, instruction_balance)
        
        elif message.text == 'Мои карты':
            for card in get_my_cards(): 
                bot.send_message(message.chat.id, f'id вашей карты {card[2]} - {card[0]}')
        
        elif message.text == 'Информация о карте':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            back_button = types.KeyboardButton('Назад')
            for i in get_my_cards():
                markup.add(types.KeyboardButton(i[2]))
            markup.add(back_button)
            bot.send_message(message.chat.id, 'выберите карту', reply_markup=markup)

        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            button_1 = types.KeyboardButton('Как открыть карту?')
            button_2 = types.KeyboardButton('Как пополнить баланс?')
            button_3 = types.KeyboardButton('Мои карты')
            button_4 = types.KeyboardButton('Информация о карте')
            markup.add(button_1, button_2, button_3, button_4)
            bot.send_message(message.chat.id, 'Назад', reply_markup=markup)



        for i in range(len(get_my_cards())):
            if message.text == get_my_cards()[i][2]:
                endpoint = (ENDPOINT_CARD_DETAIL + get_my_cards()[i][0])
                info = get_card_info(endpoint)
                for key in info:
                    bot.send_message(message.chat.id, f'ваш {key} - {info[key]}')
               
#def get_keys (info_dict):
#    a = {}
#    for key in info_dict:
#        return f'ваш {key} - {info_dict[key]}'              

bot.polling(non_stop=True)
