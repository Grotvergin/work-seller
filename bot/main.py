from bot.source import *


def Main() -> None:
    threads = [
        Thread(target=Polling),
        Thread(target=Timetable)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def Polling() -> None:
    while True:
        try:
            bot.polling(none_stop=True, interval=1)
        except Exception as e:
            Stamp(f'Error {e} happened', 'e')


def ProvideThread(back_name: str, message: telebot.types.Message, module: str = 'main') -> None:
    Stamp(f'User {message.from_user.id} requested thread for {back_name}', 'i')
    if not AddToDatabase(back_name, PATH_DB + 'active.txt', True):
        Stamp(f'Check passed: starting {back_name}', 's')
        SendMessage(message.from_user.id, f'🟢 Процесс {message.text} запущен по запросу')
        CallbackStart(message)
        thread = Thread(target=subprocess.run, args=(['python3', '-m', back_name + '.' + module],), kwargs={'check': False})
        thread.start()
        while thread.is_alive():
            time.sleep(1)
        RemoveFromDatabase(back_name, PATH_DB + 'active.txt')
    else:
        Stamp(f'Check failed: rejecting starting of {back_name}', 'w')
        SendMessage(message.from_user.id, f'🔴 Процесс {message.text} уже запущен, либо вы достигли предела в {MAX_PROCESSES} процесса...')
        CallbackStart(message)


def Timetable() -> None:
    while True:
        time.sleep(1)
        if datetime.now().strftime('%M:%S') == TIME_CHECKER:
            Stamp('Time for checker message', 'i')
            msg = PrepareChecker()
            SendMessageAll(PATH_DB + 'checker_all.txt', msg)
            if msg:
                SendMessageAll(PATH_DB + 'checker_some.txt', msg)
        elif datetime.now().strftime('%H:%M:%S') == TIME_REPORT:
            Stamp('Time for report message', 'i')
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            SendMessageAll(PATH_DB + 'report.txt', f'🟢 Отображаю отчёт за {yesterday}')
            SendMessageAll(PATH_DB + 'report.txt', PrepareReport(yesterday[8:10]))


def CallbackStart(message: telebot.types.Message) -> None:
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn_service = telebot.types.KeyboardButton(MANAGE_SERVICE)
    btn_notify = telebot.types.KeyboardButton(MANAGE_NOTIFY)
    markup.row(btn_service, btn_notify)
    bot.send_message(message.from_user.id, CHOOSE, reply_markup=markup)


def CallbackService(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.id} requested <<{message.text}>>', 'i')
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    service_names = [NAMES['advert'], NAMES['analytics'], NAMES['report'], NAMES['discharge'], NAMES['funnel'],
                     NAMES['day_main'], NAMES['hour_main'], NAMES['prices'], NAMES['statist'], NAMES['top']]
    buttons = list(map(lambda x: telebot.types.KeyboardButton(x), service_names))
    rows = [[buttons[i], buttons[i + 1]] for i in range(0, len(buttons), 2)]
    for row in rows:
        markup.row(*row)
    bot.send_message(message.from_user.id, CHOOSE, reply_markup=markup)
    bot.register_next_step_handler(message, ChosenService)


def ChosenService(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.id} requested <<{message.text}>>', 'i')
    if message.text == NAMES['report']:
        SendMessage(message.from_user.id, '❔ Введите число текущего месяца:')
        bot.register_next_step_handler(message, CallbackReport)
    elif message.text == NAMES['hour_main']:
        ProvideThread('parsers', message, 'hour_main')
    elif message.text == NAMES['day_main']:
        ProvideThread('parsers', message, 'day_main')
    elif message.text in NAMES.values():
        ProvideThread(list(filter(lambda x: NAMES[x] == message.text, NAMES))[0], message)
    else:
        SendMessage(message.from_user.id, UNKNOWN)
        CallbackStart(message)


def CallbackNotify(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.id} requested <<{message.text}>>', 'i')
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    service_names = [NAMES['report'], NAMES['checker'], NAMES['status']]
    buttons = list(map(lambda x: telebot.types.KeyboardButton(x), service_names))
    markup.row(*buttons)
    bot.send_message(message.from_user.id, CHOOSE, reply_markup=markup)
    bot.register_next_step_handler(message, ChosenNotifyType)


def ChosenNotifyType(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.id} requested <<{message.text}>>', 'i')
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    notifications = {
        NAMES['report']: {'buttons': [ACCEPT, REJECT], 'handler': DecisionReport},
        NAMES['checker']: {'buttons': [ACCEPT, SOME_CHECKER, REJECT], 'handler': DecisionChecker},
        NAMES['status']: {'buttons': [ACCEPT, SOME_STATUS, REJECT], 'handler': DecisionStatus},
    }
    notify_type = notifications.get(message.text)
    if notify_type:
        buttons = [telebot.types.KeyboardButton(button) for button in notify_type['buttons']]
        markup.row(*buttons)
        bot.send_message(message.from_user.id, CHOOSE, reply_markup=markup)
        bot.register_next_step_handler(message, notify_type['handler'])
    else:
        SendMessage(message.from_user.id, UNKNOWN)


def DecisionStatus(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.id} requested <<{message.text}>>', 'i')
    if message.text == ACCEPT:
        CallbackSub(message.from_user.id, PATH_DB + 'status_all.txt')
        RemoveFromDatabase(str(message.from_user.id), PATH_DB + 'status_some.txt')
    elif message.text == SOME_STATUS:
        CallbackSub(message.from_user.id, PATH_DB + 'status_some.txt')
        RemoveFromDatabase(str(message.from_user.id), PATH_DB + 'status_all.txt')
    elif message.text == REJECT:
        CallbackStop(message.from_user.id, [PATH_DB + 'status_all.txt', PATH_DB + 'status_some.txt'])
    else:
        SendMessage(message.from_user.id, UNKNOWN)
    CallbackStart(message)


def DecisionChecker(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.id} requested <<{message.text}>>', 'i')
    if message.text == ACCEPT:
        CallbackSub(message.from_user.id, PATH_DB + 'checker_all.txt')
        RemoveFromDatabase(str(message.from_user.id), PATH_DB + 'checker_some.txt')
    elif message.text == SOME_CHECKER:
        CallbackSub(message.from_user.id, PATH_DB + 'checker_some.txt')
        RemoveFromDatabase(str(message.from_user.id), PATH_DB + 'checker_all.txt')
    elif message.text == REJECT:
        CallbackStop(message.from_user.id, [PATH_DB + 'checker_all.txt', PATH_DB + 'checker_some.txt'])
    else:
        SendMessage(message.from_user.id, UNKNOWN)
    CallbackStart(message)


def DecisionReport(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.id} requested <<{message.text}>>', 'i')
    if message.text == ACCEPT:
        CallbackSub(message.from_user.id, PATH_DB + 'report.txt')
    elif message.text == REJECT:
        CallbackStop(message.from_user.id, [PATH_DB + 'report.txt'])
    else:
        SendMessage(message.from_user.id, UNKNOWN)
    CallbackStart(message)


def CallbackSub(user: int, path: str) -> None:
    Stamp(f'User {user} requested subscription to DB {path}', 'i')
    if AddToDatabase(str(user), path):
        SendMessage(user, '🟡 Вы уже подписаны этот тип уведомлений')
    else:
        SendMessage(user, '🟢 Вы успешно подписались на этот тип уведомлений')


def CallbackStop(user: int, path: list[str]) -> None:
    Stamp(f'User {user} requested removing from DBs {path}', 'i')
    was_deleted = False
    for db in path:
        was_deleted = RemoveFromDatabase(str(user), db)
        if was_deleted:
            break
    if was_deleted:
        SendMessage(user, '🟢 Уведомления этого типа для Вас приостановлены')
    else:
        SendMessage(user, '🟡 Вы не были подписаны на этот тип уведомлений')


def VerifyDate(day: str) -> bool:
    try:
        datetime(datetime.now().year, datetime.now().month, int(day))
        return True
    except ValueError:
        return False


def CallbackReport(message: telebot.types.Message) -> None:
    user = message.from_user.id
    body = message.text.lower()
    if not VerifyDate(body):
        SendMessage(user, '🔴 Ошибка в предоставленной дате')
    else:
        SendMessage(user, f"🟢 Отображаю отчёт за {datetime(datetime.now().year, datetime.now().month, int(body)).strftime('%Y-%m-%d')}")
        SendMessage(user, PrepareReport(body))
    CallbackStart(message)


def AddToDatabase(note: str, path: str, len_check: bool = False) -> bool:
    Stamp(f'Adding note {note} to DB {path}', 'i')
    found = False
    with open(Path.cwd() / path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() == note:
                found = True
                break
    if not found:
        lines = ReadLinesFromFile(path)
        if len_check and SmartLen(lines) >= MAX_PROCESSES:
            found = True
        else:
            with open(Path.cwd() / path, 'a') as f:
                f.write(note + '\n')
    return found


def RemoveFromDatabase(note: str, path: str) -> bool:
    Stamp(f'Removing note {note} from DB {path}', 'i')
    found = False
    lines = ReadLinesFromFile(path)
    for line in lines:
        if line.strip() == note:
            found = True
            break
    if found:
        with open(Path.cwd() / path, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.strip() != note:
                    f.write(line)
    return found


def SendMessage(user: int, msg: Union[str, list[str]]) -> None:
    Stamp(f'Sending message to one user {user}', 'i')
    if isinstance(msg, str):
        bot.send_message(user, msg, parse_mode='Markdown')
    elif msg:
        for m in msg:
            bot.send_message(user, m, parse_mode='Markdown')
    else:
        bot.send_message(user, '▪️Нет изменений', parse_mode='Markdown')


def SendMessageAll(path: str, msg: Union[str, list[str]]) -> None:
    Stamp('Sending message to numerous users', 'i')
    users = ReadLinesFromFile(path)
    for user in users:
        SendMessage(int(user), msg)


@bot.message_handler(content_types=['text'])
def MessageAccept(message: telebot.types.Message) -> None:
    user = message.from_user.id
    body = message.text
    Stamp(f'User {user} requested <<{body}>>', 'i')
    if body == '/start':
        SendMessage(user, f'Здравствуй, {message.from_user.first_name}!')
        CallbackStart(message)
    elif body == MANAGE_NOTIFY:
        CallbackNotify(message)
    elif body == MANAGE_SERVICE:
        CallbackService(message)
    else:
        SendMessage(user, '🔴 Я вас не понял... Воспользуйтесь кнопками')
        CallbackStart(message)


if __name__ == '__main__':
    Main()
