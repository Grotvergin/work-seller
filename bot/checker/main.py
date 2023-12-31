from bot.checker.source import *


def PrepareChecker() -> list:
    config, sections = ParseConfig('bot/' + NAME.lower())
    service = BuildService()
    list_of_differences = []
    for heading in sections:
        Stamp(f'Start of processing {heading}', 'b')
        token, sheet_id = ParseCurrentHeading(config, heading, TYPOLOGY)
        data = ProcessDataPackage(GetData(token))
        row, old = CreateDict(heading, TIMEOUT, NAME, sheet_id, LONG_SLEEP, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, data, heading, sheet_id, service, row)
        row, new = CreateDict(heading, TIMEOUT, NAME, sheet_id, LONG_SLEEP, service)
        list_of_differences.append(Check(old, new, heading))
    return PrepareMessages(list_of_differences)


def ParseCurrentHeading(config: ConfigParser, heading: str, typage: str) -> (str, str):
    token = config[heading]['Token']
    sheet_id = config['DEFAULT'][typage + 'SheetID']
    return token, sheet_id


def PrepareMessages(list_of_differences: list) -> list:
    total = [item for sublist in list_of_differences for item in sublist]
    messages = []
    current = ''
    for item in total:
        if len(current + item) < MAX_LEN:
            current += item
        else:
            messages.append(current)
            current = item
    if current:
        messages.append(current)
    return messages


def CreateDict(heading: str, timeout: int, name: str, sheet_id: str, timer: int, service: googleapiclient.discovery.Resource) -> (int, dict):
    Stamp(f'Creating dictionary', 'i')
    row = len(GetColumn('A', service, heading, timeout, name, sheet_id, timer)) + 2
    quantities = GetRow(row - 1, service, heading, TIMEOUT, NAME, sheet_id, LONG_SLEEP)
    articles = GetRow(row - 2, service, heading, TIMEOUT, NAME, sheet_id, LONG_SLEEP)
    dictionary = dict(zip(articles, quantities))
    return row, dictionary


def Check(prev: dict, cur: dict, heading: str) -> list:
    Stamp(f'Checking differences for {heading}','i')
    differences = []
    for key in prev:
        if key not in cur:
            differences.append(f'▪️ {key}\nЗакончился\n')
        elif int(cur[key]) - int(prev[key]) > MAX_DIFF:
            differences.append(f'▫️ {key}\nБыло *{prev[key]}*, сейчас *{cur[key]}*, разница *{int(cur[key]) - int(prev[key])}*\n')
    if differences:
        differences.insert(0, f'\n🔳 *{heading.upper()}*\n\n')
    return differences


@ControlRecursion
def GetData(token: str) -> list:
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


def ProcessDataPackage(raw: list) -> [list, list, list]:
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
    return [list_of_time, list_of_articles, list_of_quantities]
