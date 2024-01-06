from bot.report.source import *


@Inspector(NAMES[PATH[-1]])
def Main() -> None:
    msg = PrepareReport(YESTERDAY[8:10])
    IndependentSender(f'🟢 Отображаю отчёт за {YESTERDAY}', 'report')
    IndependentSender(msg, 'report')


def PrepareReport(req_date: str) -> str:
    service = BuildService()
    config, _ = ParseConfig(PATH[-2] + '/' + PATH[-1])
    sheet_id = config['DEFAULT']['SheetID']
    result = GetColumn(COLUMN_INDEXES[int(req_date) + 1], service, SHEET_NAME, sheet_id)
    formatted = str()
    headers = ('Посуда', 'Сантехника', 'Бижутерия', 'Освещение')
    for i in range(1, 36, 9):
        formatted += (f'🔳\t\t*{headers[i//9]}*\n\n▫️ WB\nСовершено заказов: {result[i]} шт\nПо среднему чеку: {result[i+1]} руб\n'
                      f'На сумму: {result[i+2]} руб\n\n️▫️ OZON\nСовершено заказов: {result[i+3]} шт\nПо среднему чеку: {result[i+4]} руб\n'
                      f'На сумму: {result[i+5]} руб\n\nИтого: {result[i+6]} заказов\nНа сумму: {result[i+7]} руб\n\n')
    return formatted


if __name__ == '__main__':
    Main()
