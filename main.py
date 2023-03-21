from config import BOT_TOKEN
import telebot
from telebot import types
from text import instruction_balance, instruction_card
from my_cards import get_my_cards


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
        if message.text == 'Как пополнить баланс?':
            bot.send_message(message.chat.id, instruction_balance)
        if message.text == 'Мои карты':
            for card in get_my_cards(): 
                bot.send_message(message.chat.id, card)
        if message.text == 'Информация о карте':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            button_1 = types.KeyboardButton('виза')
            button_2 = types.KeyboardButton('мастеркард')
            markup.add(button_1, button_2)
            bot.send_message(message.chat.id, 'выберите карту', reply_markup=markup)


        
    

bot.polling(non_stop=True)
