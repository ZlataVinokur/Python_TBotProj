from telebot import TeleBot
from hangman import HangmanGame

TOKEN = '7189414261:AAEdRog7x5q14lxsFcGy_tCwrzVK5u2iTfA'
bot = TeleBot(TOKEN)

hg = HangmanGame()

@bot.message_handler(commands=['start'])
def start(message):
    answer = f'<b>Привет! Сыграем?</b> <u>{message.from_user.first_name}</u> <u>{message.from_user.last_name}</u>'
    bot.send_message(message.chat.id, text=answer, parse_mode='html')

@bot.message_handler()
def on_message(message):
    if hg.game_on:
        if len(message.text) > 1:
            bot.send_message(message.chat.id, text='Вводить можно только буквы')
            return
        msg = hg.game_step(message.text)
        bot.send_message(message.chat.id, text=msg)
        return
    if message.text == 'виселица':
        hg.start()
        text = f'Попробуй отгадать слово \n {hg.info()}'
        bot.send_message(message.chat.id, text=text)

if __name__ == '__main__':
    bot.polling(non_stop=True)