from telebot import TeleBot
from telebot import types
from hangman import HangmanGame
import random
from anekdot import anekdots

TOKEN = '7189414261:AAEdRog7x5q14lxsFcGy_tCwrzVK5u2iTfA'
bot = TeleBot(TOKEN)

hg = HangmanGame()
anekdot = random.choice(anekdots)

@bot.message_handler(commands=['start'])
def start(message):
    answer = f'<b>Привет! Сыграем,</b><u>{message.from_user.first_name}?</u>' \
             '\nЕсли хочешь сыграть в виселицу и при выйгрыше получить анекдот (за качество ответственности не несу), напиши "висилеца"' \
             '\nЕсли анекдот хочешь, но виселица это слишком сложно, напиши "ножницы"'
    bot.send_message(message.chat.id, text=answer, parse_mode='html')

@bot.message_handler()
def on_message(message):
    if hg.game_on:
        if len(message.text) > 1 and message.text!=hg.word:
            bot.send_message(message.chat.id, text='Вводить можно только буквы или слово полностью')
            return
        elif message.text==hg.word:
            hg.game_on = False
            bot.send_message(message.chat.id, text=f'\nВау, вы угадали все буквы слова {hg.word} \nВаша награда этот анекдот:\n {anekdot}')
            return
        msg = hg.game_step(message.text)
        bot.send_message(message.chat.id, text=msg)
        return

    if message.text == 'виселица':
        text = 'Выбери сложность'
        markup = types.InlineKeyboardMarkup(row_width=2)
        item = types.InlineKeyboardButton('Просто', callback_data='question_1')
        item2 = types.InlineKeyboardButton('Сложно', callback_data='question_2')
        markup.add(item, item2)

        bot.send_message(message.chat.id, text=text, reply_markup=markup)

    if message.text == 'ножницы':
        markup = types.InlineKeyboardMarkup()
        k = types.InlineKeyboardButton(text='Камень', callback_data='Камень')
        g = types.InlineKeyboardButton(text='Ножницы', callback_data='Ножницы')
        b = types.InlineKeyboardButton(text='Бумага', callback_data='Бумага')
        markup.add(k, g, b)

        bot.send_message(message.chat.id, 'Выберите один из предметов: ', reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    city_list = ['Камень', 'Ножницы', 'Бумага']
    kgb = random.choice(city_list)

    if call.message:
        if call.data == 'question_1':
            hg.start()
            text = f'Попробуй отгадать такое слово \n {hg.info()}'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text)
        elif call.data == 'question_2':
            hg.startDif()
            text = f'Попробуй отгадать слово такое сложное слово \n {hg.info()}'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text)

    if call.data == 'Камень':
        bot.answer_callback_query(callback_query_id=call.id, text='Ваш ход принят')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы выбрали: Камень', reply_markup=None)

    elif call.data == 'Ножницы':
        bot.answer_callback_query(callback_query_id=call.id, text='Ваш ход принят')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы выбрали: Ножницы', reply_markup=None)
    elif call.data == 'Бумага':
        bot.answer_callback_query(callback_query_id=call.id, text='Ваш ход принят')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы выбрали: Бумагу', reply_markup=None)

    if call.data == kgb:
        bot.send_message(call.message.chat.id,
                         f'У вас ничья! Бот выбрал: {kgb}\nК сожалению, анекдота в этом случае вам не положено \nЧто бы начать новую игру напишите: "ножницы"')

    elif call.data == 'Камень':
        if kgb == 'Ножницы':
            bot.send_message(call.message.chat.id,
                             f'Вы победили! Бот выбрал: {kgb}\nВот ваш анекдот: \n{anekdot}\nЧто бы начать новую игру напишите: "ножницы"')

        else:
            bot.send_message(call.message.chat.id,
                             f'Вы проиграли! Бот выбрал: {kgb}\nК сожалению, анекдота в этом случае вам не положено \nЧто бы начать новую игру напишите: "ножницы"')

    elif call.data == 'Бумага':
        if kgb == 'Камень':
            bot.send_message(call.message.chat.id,
                             f'Вы победили! Бот выбрал: {kgb}\nВот ваш анекдот: \n{anekdot}\nЧто бы начать новую игру напишите: "ножницы"')

        else:
            bot.send_message(call.message.chat.id,
                             f'Вы проиграли! Бот выбрал: {kgb}\nК сожалению, анекдота в этом случае вам не положено \nЧто бы начать новую игру напишите: "ножницы"')

    elif call.data == 'Ножницы':
        if kgb == 'Бумага':
            bot.send_message(call.message.chat.id,
                             f'Вы победили! Бот выбрал: {kgb}\nВот ваш анекдот: \n{anekdot}\nЧто бы начать новую игру напишите: "ножницы"')

        else:
            bot.send_message(call.message.chat.id,
                             f'Вы проиграли! Бот выбрал: {kgb}\nК сожалению, анекдота в этом случае вам не положено \nЧто бы начать новую игру напишите: "ножницы"')


if __name__ == '__main__':
    bot.polling(non_stop=True)