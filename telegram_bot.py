import os
import telebot

MARIA = os.getenv('MARIA')
SERGEY = os.getenv('SERGEY')
TOKEN = os.getenv('TOKEN')
ADMIN_URL = os.getenv('ADMIN_URL')

bot = telebot.TeleBot(TOKEN)


def send_message(name, phone, event_date, text):
    message = (f'Заявка от {name}\n'
               f'Дата мероприятия: {event_date} \n'
               f'Сообщение: {text} \n'
               f'Перезвонить: {phone} \n'
               f'. \n'
               f'посмотреть все заявки http://127.0.0.1:5000{ADMIN_URL}')
    bot.send_message(SERGEY, message)
