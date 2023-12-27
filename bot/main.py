from bot.source import *


def main():
    main_thread = Thread(target=MainThread)
    another_thread = Thread(target=PollingThread)
    another_thread.start()
    main_thread.start()
    another_thread.join()
    main_thread.join()


def PollingThread():
    while True:
        try:
            bot.polling(none_stop=True, interval=1)
        except Exception as e:
            Stamp(str(e), 'e')


def MainThread():
    while True:
        time.sleep(1)
        if datetime.now().strftime('%M:%S') == '00:00':
            Stamp('Time to send message', 'i')
            SendMessage('bot/chats.txt')


def CallbackStart(user: int):
    Stamp(f'User id {user} requested /start', 'i')
    if AddToDatabase(user, 'bot/chats.txt'):
        bot.send_message(user, '🟡 Вы уже подписаны на уведомления')
    else:
        bot.send_message(user, '🟢 Режим автоматической отправки сообщений включён')


def CallbackEnd(user: int):
    Stamp(f'User id {user} requested /stop', 'i')
    if RemoveFromDatabase(user, 'bot/chats.txt'):
        bot.send_message(user, '🟢 Уведомления для Вас приостановлены')
    else:
        bot.send_message(user, '🟡 Вы не были подписаны на уведомления')


def VerifyDate(day: str):
    try:
        datetime(datetime.now().year, datetime.now().month, int(day))
        return True
    except ValueError:
        return False


def CallbackReport(message):
    body = message.text.lower()
    user = message.from_user.id
    if not VerifyDate(body):
        bot.send_message(user, '🔴 Ошибка в предоставленной дате')
    else:
        bot.send_message(user, f"🟢 Отображаю отчёт за {datetime(datetime.now().year, datetime.now().month, int(body)).strftime('%Y-%m-%d')}")
        bot.send_message(user, PrepareReport(body), parse_mode='Markdown')


def AddToDatabase(user_id: int, path: str):
    Stamp(f'Adding user id {user_id} to DB', 'i')
    found = False
    with open(Path.cwd() / path, 'r') as f:
        for line in f:
            if line.strip() == str(user_id):
                found = True
                break
    if not found:
        with open(Path.cwd() / path, 'a') as f:
            f.write(str(user_id) + '\n')
    return found


def RemoveFromDatabase(user_id: int, path: str):
    Stamp(f'Removing user id {user_id} from DB', 'i')
    found = False
    with open(Path.cwd() / path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.strip() == str(user_id):
            found = True
            break
    if found:
        with open(Path.cwd() / path, 'w') as f:
            for line in lines:
                if line.strip() != str(user_id):
                    f.write(line)
    return found


def SendMessage(path: str):
    Stamp('Preparing and sending message', 'i')
    msg = PrepareMessage()
    with open(Path.cwd() / path, 'r') as f:
        user_ids = f.readlines()
    for user in user_ids:
        if msg:
            if len(msg) > MAX_LEN:
                for x in range(0, len(msg), MAX_LEN):
                    bot.send_message(user, msg[x:x+MAX_LEN], parse_mode='Markdown')
            else:
                bot.send_message(user, msg, parse_mode='Markdown')
        else:
            bot.send_message(user, f'🔸 Нет изменений с последнего обновления')


@bot.message_handler(content_types=['text'])
def GetOther(message):
    user = message.from_user.id
    body = message.text.lower()
    Stamp(f'Got message from user id {user} – {message.text}', 'i')
    if body == '/start':
        CallbackStart(user)
    elif body == '/stop':
        CallbackEnd(user)
    elif body == '/report':
        bot.send_message(user, '❔ Введите число текущего месяца:')
        bot.register_next_step_handler(message, CallbackReport)
    else:
        bot.send_message(user, '🔴 Я вас не понял...\n/start – подписаться на уведомления\n/stop – отписаться от уведомлений\n/report – получить отчёт')


if __name__ == '__main__':
    main()
