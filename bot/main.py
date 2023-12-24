from bot.source import *
import logging


# TODO Improve safety by the depth of recursion
def main():
    config, sections = ParseConfig('bot')
    service = BuildService()
    message = []
    for heading in sections:
        Stamp(f'Start of processing {heading}', 'b')
        token = config[heading]['Token']
        data = GetData(token)
        data = ProcessDataPackage(data, heading)
        row = len(GetColumn('A', service, heading, TIMEOUT, NAME, SHEET_ID, LONG_SLEEP)) + 2
        prev_quantities = GetRow(row - 1, service, heading, TIMEOUT, NAME, SHEET_ID, LONG_SLEEP)
        prev_articles = GetRow(row - 2, service, heading, TIMEOUT, NAME, SHEET_ID, LONG_SLEEP)
        prev_dict = dict(zip(prev_articles, prev_quantities))
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, data, heading, SHEET_ID, service, row)
        cur_quantities = GetRow(row + 2, service, heading, TIMEOUT, NAME, SHEET_ID, LONG_SLEEP)
        cur_articles = GetRow(row + 1, service, heading, TIMEOUT, NAME, SHEET_ID, LONG_SLEEP)
        cur_dict = dict(zip(cur_articles, cur_quantities))
        list_of_differences = Check(prev_dict, cur_dict)
        message.append(list_of_differences)
        Stamp(f'End of processing {heading}', 'b')
    return message


def Check(prev: dict, cur: dict):
    list_of_differences = []
    for key in prev:
        if key not in cur:
            list_of_differences.append(f'Отсутствует комбинация товар – склад: *{key}*')
        elif int(cur[key]) - int(prev[key]) > MAX_DIFF:
            list_of_differences.append(
                f'{key} – было *{prev[key]}*, сейчас *{cur[key]}*, разница *{int(cur[key]) - int(prev[key])}*')
    return list_of_differences


def GetData(token: str):
    Stamp(f'Trying to connect {URL}', 'i')
    # TODO Control the depth of recursion
    try:
        response = requests.get(URL, headers={'Authorization': token}, params={'dateFrom': DATE_FROM})
    except requests.ConnectionError:
        Stamp(f'On connection {URL}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(token)
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on {URL}', 's')
            if response.content:
                raw = response.json()
            else:
                Stamp('Response in empty', 'w')
                raw = []
        else:
            Stamp(f'Status = {response.status_code} on {URL}', 'e')
            Sleep(LONG_SLEEP)
            raw = GetData(token)
    return raw


def ProcessDataPackage(raw: list, heading: str):
    try:
        height = len(raw)
    except TypeError:
        height = 0
        Stamp(f'For sheet {heading} found NO rows', 'w')
    else:
        Stamp(f'For sheet {heading} found {height} rows', 'i')
    list_of_articles = []
    list_of_quantities = []
    list_of_time = []
    for i in range(height):
        for row in ROWS:
            match row:
                case 'supplierArticle':
                    list_of_articles.append(str(raw[i][row]) + ' – ' + str(raw[i]['warehouseName']))
                case 'quantity':
                    list_of_quantities.append(str(raw[i][row]))
                case 'time':
                    list_of_time.append(str(datetime.now().strftime('%m-%d %H:%M')))
    return [list_of_time, list_of_articles, list_of_quantities]


def Pend(message):
    bot.send_message(message.from_user.id, f'Сверяю данные...\nМаксимальное отклонение = {MAX_DIFF}')
    result = main()
    formatted_result = '\n'.join(str(item) for sublist in result for item in sublist if item)
    if formatted_result:
        bot.send_message(message.from_user.id, f'Произошли такие изменения:\n{formatted_result}', parse_mode='Markdown')
    else:
        bot.send_message(message.from_user.id, f'Ничего не изменилось с прошлого обновления...')


bot = telebot.TeleBot('6833627182:AAFlKnO1BOsGn1P9eIqNlNNmpNPCz6R6D1M')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет, я великолепный бот-помогатор. Напиши /help')
    elif message.text.lower() == '/pend':
        Pend(message)
    elif message.text.lower() == '/auto':
        while True:
            Pend(message)
            Sleep(INTERVAL)
    elif message.text.lower() == '/help':
        bot.send_message(message.from_user.id, f'/auto – автоматическое обновление раз в {INTERVAL / 3600} час(а)\n'
                                               f'/pend – узнать текущую ситуацию')
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю. Напиши /help')


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        logging.error(e)
