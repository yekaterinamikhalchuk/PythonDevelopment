import telebot
import time
from telebot import types

from config import keys, TOKEN
from extention import APIException, CurrencyConverter
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['help', 'start'])

def help(message: telebot.types.Message):
    text = \
"Hello, {0.first_name}!\nI'm {1.first_name}! I will help you to avoid difficult mathematical\
calculations.".format(message.from_user, bot.get_me())
    bot.reply_to(message, text)
    buttons = [
    [
        types.InlineKeyboardButton(text="Yes", callback_data='yes'),
        types.InlineKeyboardButton(text="No", callback_data='no'),
    ],
]

    markup_inline = types.InlineKeyboardMarkup(buttons, row_width=2)

    # markup_inline.add(item_yes, item_no)
    bot.send_message(message.chat.id, 'Do you want to try', reply_markup=markup_inline)

@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    if call.data == 'yes':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("💸 Currencies available")
        item2 = types.KeyboardButton("🔎 Input example")
        markup.add(item1, item2)
        text = "To start the program enter the following information:\n\
Currency_from, Currency_to, Amount"
        bot.send_message(call.message.chat.id, text, parse_mode='html', reply_markup=markup)
        text2 = "To see available currencies press 'Currencies available 💸'\n\n\
To see input example press 'Input example 🔎'"
        bot.send_message(call.message.chat.id, text2)
    elif call.data == 'no':
        text3 = "What a pity! It worth trying... I will be waiting for you"
        bot.send_message(call.message.chat.id, text3)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):

    if message.text == "💸 Currencies available":
        text = '💸 Currencies available:'
        for key in keys.keys():
            text = '\n'.join((text, key))
        bot.reply_to(message, text)
    elif message.text == "🔎 Input example":
        bot.reply_to(message, "Ruble, Dollar, 120.5")
    elif message.text != "💸 Currencies available" and message.text != "🔎 Input example":
        try:
            input_values = message.text.split(',')
            if len(input_values) != 3:
                raise APIException('Input error! Enter 3 values separates by comma')
            cur_from, cur_to, amount = input_values
            cur_from, cur_to, amount = cur_from.strip().lower(), cur_to.strip().lower(), amount.strip().lower()
            amount_cur_to = round(CurrencyConverter.get_price(cur_from, cur_to, amount), 2)
        except APIException as e:
            bot.reply_to(message, f'User"s error!\nError: {e}')
        except Exception as e:
            bot.reply_to(message, f'Server error! The query cannot be handled. \nError: {e}')
        else:
            text = f'The price for {amount} {cur_from} is {amount_cur_to} {cur_to}'
            sticker = open('sticker.webp', 'rb')
            bot.send_sticker(message.chat.id, sticker)
            time.sleep(3)
            bot.send_message(message.chat.id, text)




bot.polling(none_stop=True)




