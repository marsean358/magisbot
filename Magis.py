import telebot
import webbrowser
import sqlite3
from telebot import types
import time


bot = telebot.TeleBot('7036414832:AAFUFwOLBIrcw1pP1O5MLhPdUfWdNiieZfI')

change = types.InlineKeyboardMarkup()
clothes = types.InlineKeyboardButton('Одежда',callback_data= "Одежда")
shoes = types.InlineKeyboardButton('Обувь', callback_data= "Обувь")
change.add(clothes,shoes)
shop_clothes = types.InlineKeyboardMarkup()
shop_shoes = types.InlineKeyboardMarkup()
back_choose = types.InlineKeyboardMarkup()
art = types.InlineKeyboardButton('Артикул', callback_data='Артикул')
screen = types.InlineKeyboardButton('Скриншот',callback_data='Скриншот')
name = types.InlineKeyboardButton('Название',callback_data='Название')
back = types.InlineKeyboardButton('Назад',callback_data='Назад')
shop_clothes.row(screen, name)
shop_clothes.row(back)
shop_shoes.row(art)
shop_shoes.row(screen,name)
shop_shoes.row(back)
back_choose.add(back)


def register_user(message):
    chat_id = message.chat.id
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text= "Введите свой логин:")
    bot.register_next_step_handler(message, process_login_step)



def process_login_step(message):
    chat_id = message.chat.id
    login = message.text
    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.send_message(message.chat.id, "Теперь введите свой пароль:")
    bot.register_next_step_handler(message, process_password_step,login)


def process_password_step(message,login):
    user_name= message.from_user.username
    password = message.text
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_name, login, password) VALUES (?, ?, ?)", (user_name, login, password))
    conn.commit()
    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.send_message(message.chat.id,"Вы успешно зарегистрированы!")
    time.sleep(0.5)
    cursor.close()



@bot.message_handler(commands=['start'])
def send_welcome(message):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_name FROM users WHERE user_name = ?", (message.from_user.username,))
    data = cursor.fetchall()
    conn.close()
    if len(data) == 0:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Регистрация', callback_data='register'))
        bot.send_message(message.chat.id,f"Привет, {message.from_user.first_name}! \nЧтобы продолжить, необходимо зарегистрироваться!",reply_markup=markup)
    else:
        bot.send_message(message.chat.id,f"Добро пожаловать,{message.from_user.username}!")
    change_menu(message)

def change_menu(message):
    bot.send_message(message.chat.id, "Что бы вы хотели заказать:", reply_markup=change)







@bot.callback_query_handler(func=lambda callbak: True)
def callback_message(callback):
    if callback.data == 'register':
        register_user(callback.message)
    if callback.data == 'Обувь':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id,"Как будем искать товар?",reply_markup=shop_shoes)
    if callback.data == 'Одежда':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Как будем искать товар?", reply_markup=shop_clothes)
    if callback.data == 'Назад':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        change_menu(callback.message)
    if callback.data == "Артикул":
        bot.delete_message(callback.message.chat.id,callback.message.message_id)
        bot.send_message(callback.message.chat.id,"Введите артикул товара", reply_markup=back_choose)
    if callback.data == "Скриншот":
        bot.delete_message(callback.message.chat.id,callback.message.message_id)
        bot.send_message(callback.message.chat.id,"Пришлите фото товара", reply_markup=back_choose)
    if callback.data == "Название":
        bot.delete_message(callback.message.chat.id,callback.message.message_id)
        bot.send_message(callback.message.chat.id,"Введите название товара", reply_markup=back_choose)





bot.polling(none_stop=True)