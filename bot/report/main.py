from bot.report.source import *


@Inspector(PATH[-1])
def Main() -> None:
    msg = PrepareReport(YESTERDAY[8:10])
    IndependentSender(f'🟢 Отчёт от *{YESTERDAY}*', 'report')
    IndependentSender(msg, 'report')
    GroupSender(msg, 'report_groups')


def PrepareReport(req_date: str) -> list[str]:
    service = BuildService()
    config, _ = ParseConfig(PATH[-2] + '/' + PATH[-1])
    sheet_id = config['DEFAULT']['SheetID']
    simple = GetColumn(COLUMN_INDEXES[int(req_date) + 1], service, NAME_SIMPLE, sheet_id)
    formatted = list()
    formatted.append(f'🔳 *{HEADERS_SIMPLE}*\n\n▫️ WB\nСовершено заказов: *{simple[1]}* шт\nПо среднему чеку: *{simple[2]}* руб\n'
                     f'На сумму: *{simple[3]}* руб\n\n️▫️ OZON\nСовершено заказов: *{simple[4]}* шт\nПо среднему чеку: *{simple[5]}* руб\n'
                     f'На сумму: *{simple[6]}* руб\n\nИтого: *{simple[7]}* заказов\nНа сумму: *{simple[8]}* руб\n\n')
    detailed = GetColumn(COLUMN_INDEXES[int(req_date) + 1], service, NAME_DETAILED, sheet_id)
    for i in range(1, 51, 17):
        project = (f'🔳 *{HEADERS_DETAILED[i // 17]}*\n\n▫️ WB\nСовершено заказов всего: *{detailed[i]}* шт\nПо среднему чеку: *{detailed[i + 2]}* руб\n'
                   f'На сумму: *{detailed[i + 1]}* руб\n\nОрганических заказов: *{detailed[i + 3]}*\nПо среднему чеку: *{detailed[i + 5]}* руб\n'
                   f'На сумму: *{detailed[i + 4]}* руб\n\nСовершено самовыкупов: *{detailed[i + 6]}* штук\nНа сумму: *{detailed[i + 7]}* руб\n\n'
                   f'▫️ OZON\nСовершено заказов: *{detailed[i + 8]}* шт\nПо среднему чеку: *{detailed[i + 9]}* руб\n'
                   f'На сумму: *{detailed[i + 10]}* руб\n\nИтого: *{detailed[i + 12]}* органических заказов\nНа сумму: *{detailed[i + 14]}* руб\n\n')
        formatted.append(project)
    return formatted


if __name__ == '__main__':
    Main()
