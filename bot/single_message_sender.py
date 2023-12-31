from common import *


def SendMessage(path: str):
    Stamp('Preparing and sending message', 'i')
    with open(Path.cwd() / path, 'r') as f:
        user_ids = f.readlines()
    for user in user_ids:
        if msg:
            bot.send_message(user, msg, parse_mode='Markdown')
        else:
            bot.send_message(user, f'🔸 Нет изменений с последнего обновления')


bot = telebot.TeleBot('INSERT TOKEN')
msg = '❗️Предыдущее сообщение содержало тестовые данные❗️\nОбновлений по позициям:\nCU350S2 – Краснодар\nBMAT-SQS-BRN – Невинномысск\nABM-VES-SLM – Электросталь\n*НЕ БЫЛО!*'
SendMessage('bot/all_chats.txt')
