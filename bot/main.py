from bot.source import *


def Main() -> None:
    while True:
        try:
            bot.polling(none_stop=True, interval=1)
        except Exception as e:
            Stamp(f'Error {e} happened', 'e')
            Stamp(traceback.format_exc(), 'e')


def ProvideThread(back_name: str, message: telebot.types.Message, module: str = 'main', flag: str = '') -> None:
    Stamp(f'User {message.from_user.id} requested thread for {back_name}', 'i')
    SendMessage(message.from_user.id, f'🟡 Запускаю процесс {message.text}...')
    CallbackStart(message)
    thread = Thread(target=subprocess.run, args=(['python', '-m', back_name + '.' + module, flag],), kwargs={'check': False})
    thread.start()
    while thread.is_alive():
        time.sleep(1)


def CallbackStart(message: telebot.types.Message) -> None:
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn_service = telebot.types.KeyboardButton(MANAGE_SERVICE)
    btn_notify = telebot.types.KeyboardButton(MANAGE_NOTIFY)
    markup.row(btn_service, btn_notify)
    bot.send_message(message.from_user.id, CHOOSE, reply_markup=markup)


def CallbackService(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.id} requested {message.text}', 'i')
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    service_names = NAMES.values()
    buttons = list(map(lambda x: telebot.types.KeyboardButton(x), service_names))
    rows = [[buttons[i], buttons[i + 1]] for i in range(0, len(buttons), 2)]
    for row in rows:
        markup.row(*row)
    bot.send_message(message.from_user.id, CHOOSE, reply_markup=markup)
    bot.register_next_step_handler(message, ChosenService)


def ChosenService(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.id} requested {message.text}', 'i')
    if message.text == NAMES['report']:
        SendMessage(message.from_user.id, '❔ Введите число текущего месяца:')
        bot.register_next_step_handler(message, CallbackReport)
    elif message.text == NAMES['farafon']:
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        cab_names = CABINETS_ACCEPTANCE.keys()
        buttons = list(map(lambda x: telebot.types.KeyboardButton(x), cab_names))
        rows = [[buttons[i], buttons[i + 1]] for i in range(0, len(buttons), 2)]
        for row in rows:
            markup.row(*row)
        bot.send_message(message.from_user.id, '❔ Выберите желаемый кабинет:', reply_markup=markup)
        bot.register_next_step_handler(message, CallbackAcceptanceCabinet)
    elif message.text == NAMES['parsers-h']:
        ProvideThread('parsers', message, 'main', '-h')
    elif message.text == NAMES['parsers-d']:
        ProvideThread('parsers', message, 'main', '-d')
    elif message.text in NAMES.values():
        ProvideThread(list(filter(lambda x: NAMES[x] == message.text, NAMES))[0], message)
    else:
        SendMessage(message.from_user.id, UNKNOWN)
        CallbackStart(message)


def CallbackAcceptanceColumn(message: telebot.types.Message) -> None:
    if PrepareAcceptance(message.text.upper(), CABINETS_ACCEPTANCE[CUR_CAB_ACCEPTANCE]):
        SendMessage(message.from_user.id, f'🟢 Отчёт по столбцу {message.text.upper()} подготовлен')
    else:
        SendMessage(message.from_user.id, f'🔴 Некорректный столбец {message.text.upper()}, проверьте его существование...')
    CallbackStart(message)


def CallbackAcceptanceCabinet(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.id} requested {message.text}', 'i')
    if message.text in CABINETS_ACCEPTANCE.keys():
        global CUR_CAB_ACCEPTANCE
        CUR_CAB_ACCEPTANCE = message.text
        SendMessage(message.from_user.id, '❔ Напишите желаемый столбец, например, AI')
        bot.register_next_step_handler(message, CallbackAcceptanceColumn)
    else:
        SendMessage(message.from_user.id, UNKNOWN)
        CallbackStart(message)


def CallbackNotify(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.id} requested {message.text}', 'i')
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    service_names = [NAMES['report'], NAMES['checker'], NAMES['status']]
    buttons = list(map(lambda x: telebot.types.KeyboardButton(x), service_names))
    markup.row(*buttons)
    bot.send_message(message.from_user.id, CHOOSE, reply_markup=markup)
    bot.register_next_step_handler(message, ChosenNotifyType)


def ChosenNotifyType(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.id} requested {message.text}', 'i')
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
    Stamp(f'User {message.from_user.id} requested {message.text}', 'i')
    if message.text == ACCEPT:
        CallbackSub(message.from_user.id, PATH_DB + 'status.txt')
        RemoveFromDatabase(str(message.from_user.id), PATH_DB + 'status_important.txt')
    elif message.text == SOME_STATUS:
        CallbackSub(message.from_user.id, PATH_DB + 'status_important.txt')
        RemoveFromDatabase(str(message.from_user.id), PATH_DB + 'status.txt')
    elif message.text == REJECT:
        CallbackStop(message.from_user.id, [PATH_DB + 'status.txt', PATH_DB + 'status_important.txt'])
    else:
        SendMessage(message.from_user.id, UNKNOWN)
    CallbackStart(message)


def DecisionChecker(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.id} requested {message.text}', 'i')
    if message.text == ACCEPT:
        CallbackSub(message.from_user.id, PATH_DB + 'checker.txt')
        RemoveFromDatabase(str(message.from_user.id), PATH_DB + 'checker_important.txt')
    elif message.text == SOME_CHECKER:
        CallbackSub(message.from_user.id, PATH_DB + 'checker_important.txt')
        RemoveFromDatabase(str(message.from_user.id), PATH_DB + 'checker.txt')
    elif message.text == REJECT:
        CallbackStop(message.from_user.id, [PATH_DB + 'checker.txt', PATH_DB + 'checker_important.txt'])
    else:
        SendMessage(message.from_user.id, UNKNOWN)
    CallbackStart(message)


def DecisionReport(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.id} requested {message.text}', 'i')
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


def CallbackReport(message: telebot.types.Message) -> None:
    user = message.from_user.id
    body = message.text.lower()
    if not VerifyDate(body):
        SendMessage(user, '🔴 Ошибка в предоставленной дате...')
    else:
        SendMessage(user, f"🟢 Отчёт от *{datetime(datetime.now().year, datetime.now().month, int(body)).strftime('%Y-%m-%d')}*")
        SendMessage(user, PrepareReport(body))
    CallbackStart(message)


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
    Stamp(f'User {user} requested {body}', 'i')
    if body == '/start':
        SendMessage(user, f'Здравствуй, {message.from_user.first_name}!')
        CallbackStart(message)
    elif body == MANAGE_NOTIFY:
        CallbackNotify(message)
    elif body == MANAGE_SERVICE:
        CallbackService(message)
    else:
        SendMessage(user, '⤵️ Воспользуйтесь кнопками')
        CallbackStart(message)


if __name__ == '__main__':
    Main()
