from bot.source import *


def main():
    polling_thr = Thread(target=Polling)
    time_thr = Thread(target=Timetable)
    polling_thr.start()
    time_thr.start()
    polling_thr.join()
    time_thr.join()


def Polling():
    while True:
        try:
            bot.polling(none_stop=True, interval=1)
        except Exception as e:
            Stamp(str(e), 'e')


def Timetable():
    while True:
        time.sleep(1)
        if datetime.now().strftime('%M:%S') == TIME_CHECKER:
            Stamp('Time for checker message', 'i')
            SendMessageAll(PATH_TO_DB, PrepareChecker())
        elif datetime.now().strftime('%H:%M:%S') == TIME_REPORT:
            Stamp('Time for report message', 'i')
            date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            SendMessageAll(PATH_TO_DB, f'🟢 Отображаю отчёт за {date}')
            SendMessageAll(PATH_TO_DB, PrepareReport(date[8:10]))


def CallbackStart(user: int):
    Stamp(f'User {user} requested /start', 'i')
    if AddToDatabase(user, PATH_TO_DB):
        SendMessage(user, '🟡 Вы уже подписаны на уведомления')
    else:
        SendMessage(user, '🟢 Режим автоматической отправки сообщений включён')


def CallbackStop(user: int):
    Stamp(f'User {user} requested /stop', 'i')
    if RemoveFromDatabase(user, PATH_TO_DB):
        SendMessage(user, '🟢 Уведомления для Вас приостановлены')
    else:
        SendMessage(user, '🟡 Вы не были подписаны на уведомления')


def VerifyDate(day: str):
    try:
        datetime(datetime.now().year, datetime.now().month, int(day))
        return True
    except ValueError:
        return False


def CallbackReport(message):
    user = message.from_user.id
    body = message.text.lower()
    if not VerifyDate(body):
        SendMessage(user, '🔴 Ошибка в предоставленной дате')
    else:
        SendMessage(user, f"🟢 Отображаю отчёт за {datetime(datetime.now().year, datetime.now().month, int(body)).strftime('%Y-%m-%d')}")
        SendMessage(user, PrepareReport(body))


def AddToDatabase(user: int, path: str):
    Stamp(f'Adding user {user} to DB', 'i')
    found = False
    with open(Path.cwd() / path, 'r') as f:
        for line in f:
            if int(line.strip()) == user:
                found = True
                break
    if not found:
        with open(Path.cwd() / path, 'a') as f:
            f.write(str(user) + '\n')
    return found


def RemoveFromDatabase(user: int, path: str):
    Stamp(f'Removing user {user} from DB', 'i')
    found = False
    with open(Path.cwd() / path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if int(line.strip()) == user:
            found = True
            break
    if found:
        with open(Path.cwd() / path, 'w') as f:
            for line in lines:
                if int(line.strip()) != user:
                    f.write(line)
    return found
    
    
def SendMessage(user: int, msg: str):
    Stamp(f'Sending message to user {user}', 'i')
    if msg:
        if len(msg) > MAX_LEN:
            for x in range(0, len(msg), MAX_LEN):
                bot.send_message(user, msg[x:x + MAX_LEN], parse_mode='Markdown')
        else:
            bot.send_message(user, msg, parse_mode='Markdown')
    else:
        bot.send_message(user, '▪️Нет изменений', parse_mode='Markdown')


def SendMessageAll(path: str, msg: str):
    Stamp('Sending message to all users', 'i')
    with open(Path.cwd() / path, 'r') as f:
        users = f.readlines()
    for user in users:
        SendMessage(int(user), msg)


@bot.message_handler(content_types=['text'])
def MessageAccept(message):
    user = message.from_user.id
    body = message.text.lower()
    Stamp(f'Got message from user {user} – {body}', 'i')
    match body:
        case '/start':
            CallbackStart(user)
        case '/stop':
            CallbackStop(user)
        case '/report':
            SendMessage(user, '❔ Введите число текущего месяца:')
            bot.register_next_step_handler(message, CallbackReport)
        case _:
            SendMessage(user, '🔴 Я вас не понял...\n'
                              '/start – подписаться на уведомления\n'
                              '/stop – отписаться от уведомлений\n'
                              '/report – получить отчёт')


if __name__ == '__main__':
    main()
