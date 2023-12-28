from bot.report.source import *


def PrepareReport(date: str):
    service = BuildService()
    result = GetColumn(COLUMN_INDEXES[int(date) + 1], service, SHEET_NAME, TIMEOUT, NAME, SHEET_ID, LONG_SLEEP)
    formatted = ''
    headers = ('Посуда', 'Сантехника', 'Бижутерия', 'Освещение')
    for i in range(1, 36, 9):
        formatted += (f'🔳 {headers[i//9]}\n\n▫️ *WB*\nСовершено заказов: {result[i]} шт\nПо среднему чеку: {result[i+1]} руб\n'
                      f'На сумму: {result[i+2]} руб\n\n️▫️ *OZON*\nСовершено заказов: {result[i+3]} шт\nПо среднему чеку: {result[i+4]} руб\n'
                      f'На сумму: {result[i+5]} руб\n\nИтого: {result[i+6]} заказов\nНа сумму: {result[i+7]} руб\n\n')
    return formatted
