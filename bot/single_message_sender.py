from common import *

main = '6833627182:AAFlKnO1BOsGn1P9eIqNlNNmpNPCz6R6D1M'
test = '6811526530:AAHKNIrSMjvyfd-4u_zGPcpLVrYXTGBr4pI'


def SendMessage(path: str):
    Stamp('Preparing and sending message', 'i')
    with open(Path.cwd() / path, 'r') as f:
        user_ids = f.readlines()
    for user in user_ids:
        if msg:
            bot.send_message(user, msg, parse_mode='Markdown')
        else:
            bot.send_message(user, f'🔸 Нет изменений с последнего обновления')


bot = telebot.TeleBot(main)
msg = '❗️Предыдущее сообщение содержало тестовые данные❗️\nОбновлений по позициям:\nCU350S2 – Краснодар\nBMAT-SQS-BRN – Невинномысск\nABM-VES-SLM – Электросталь\n*НЕ БЫЛО!*'
SendMessage('bot/all_chats.txt')
