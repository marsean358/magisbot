import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('7007425117:AAGLzDQ7D_aDN9MOoWNW7xETwovlEPcsifc')


@bot.message_handler(commands=['start'])
def start(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard = True)
    db_btn=types.KeyboardButton('Список пользователей')
    markup.add(db_btn)
    bot.send_message(message.chat.id,"Что хочешь?",reply_markup=markup)

@bot.message_handler(content_types=['text'])
def Db_list(message):
    if message.text == 'Список пользователей':
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        id = (cursor.execute("SELECT id FROM users")).fetchall()
        logins = (cursor.execute("SELECT login FROM users")).fetchall()
        passwords = (cursor.execute("SELECT password FROM users")).fetchall()
        user_name= (cursor.execute("SELECT user_name FROM users")).fetchall()
        for i in range(len(id)):
            bot.send_message(message.chat.id, f"Id:{id[i][0]}\nLogin:{logins[i][0]}\nPassword:{passwords[i][0]}\nUser_name:http://t.me/{user_name[i][0]}" )
        cursor.close()


bot.polling(none_stop=True)