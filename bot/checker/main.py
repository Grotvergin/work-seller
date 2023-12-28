from bot.checker.source import *


def PrepareChecker():
    config, sections = ParseConfig('bot/checker')
    service = BuildService()
    temp = ''
    for heading in sections:
        Stamp(f'Start of processing {heading}', 'b')
        token = config[heading]['Token']
        data = ProcessDataPackage(GetData(token))
        row, old = CreateDict(heading, TIMEOUT, NAME, SHEET_ID, LONG_SLEEP, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, data, heading, SHEET_ID, service, row)
        row, new = CreateDict(heading, TIMEOUT, NAME, SHEET_ID, LONG_SLEEP, service)
        differences = Check(old, new, heading)
        if differences:
            temp += differences + '\n'
        Stamp(f'End of processing {heading}', 'b')
    return temp


def CreateDict(heading: str, timeout: int, name: str, sheet_id: str, timer: int, service):
    Stamp(f'Start of creating dictionary', 'i')
    row = len(GetColumn('A', service, heading, timeout, name, sheet_id, timer)) + 2
    quantities = GetRow(row - 1, service, heading, TIMEOUT, NAME, SHEET_ID, LONG_SLEEP)
    articles = GetRow(row - 2, service, heading, TIMEOUT, NAME, SHEET_ID, LONG_SLEEP)
    dictionary = dict(zip(articles, quantities))
    Stamp('End of creating dictionary', 'i')
    return row, dictionary


def Check(prev: dict, cur: dict, heading: str):
    Stamp(f'Start of checking differences for {heading}','i')
    differences = []
    for key in prev:
        if key not in cur:
            differences.append(f'🔺{key}\nЭтот товар *закончился* на складе')
        elif int(cur[key]) - int(prev[key]) > MAX_DIFF:
            differences.append(f'▫️{key}\nБыло *{prev[key]}*, сейчас *{cur[key]}*, разница *{int(cur[key]) - int(prev[key])}*')
    if differences:
        differences.insert(0, f'🔳 *{heading}*')
    formatted = '\n'.join(str(item) for item in differences if item)
    Stamp(f'End of checking differences for {heading}', 'i')
    return formatted


@ControlRecursion
def GetData(token: str):
    Stamp(f'Trying to connect {URL}', 'i')
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


def ProcessDataPackage(raw: list):
    Stamp('Start of processing data', 'i')
    list_of_articles = []
    list_of_quantities = []
    list_of_time = []
    for i in range(SmartLen(raw)):
        for row in ROWS:
            match row:
                case 'supplierArticle':
                    list_of_articles.append(str(raw[i][row]) + ' – ' + str(raw[i]['warehouseName']))
                case 'quantity':
                    list_of_quantities.append(str(raw[i][row]))
                case 'time':
                    list_of_time.append(str(datetime.now().strftime('%m-%d %H:%M')))
    Stamp('End of processing data', 'i')
    return [list_of_time, list_of_articles, list_of_quantities]
