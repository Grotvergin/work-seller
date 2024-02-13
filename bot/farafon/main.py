from bot.farafon.source import *


@Inspector(PATH[-1])
def PrepareAcceptance(req_col: str) -> bool:
    service = BuildService()
    config, _ = ParseConfig(PATH[-2] + '/' + PATH[-1])
    sheet_id = config['DEFAULT']['SheetID']
    if not VerifyColumn(req_col, service, sheet_id):
        return False
    num_col = GetColumn(req_col, service, NAME_SOURCE, sheet_id, False, START_ROW, END_ROW)
    id_col = GetColumn(COLUMN_ID, service, NAME_SOURCE, sheet_id, False, START_ROW, END_ROW)
    data = ProcessData(num_col, id_col)
    CleanSheet(LEN_COLS, NAME_OUTPUT, sheet_id, service)
    UploadData(data, NAME_OUTPUT, sheet_id, service)
    return True


def ProcessData(num_col: list[str], id_col: list[str]) -> list[list[str]]:
    list_of_rows = []
    for i in range(SmartLen(num_col)):
        if num_col[i] is not None:
            list_of_rows.append([str(id_col[i]), str(num_col[i])])
    return list_of_rows


def VerifyColumn(req_col: str, service: googleapiclient.discovery.Resource, sheet_id: str) -> bool:
    Stamp(f'Checking column, requested {req_col}', 'i')
    len_cols = SmartLen(GetRow(ROW_TO_CHECK, service, NAME_SOURCE, sheet_id))
    if req_col in COLUMN_INDEXES.values() and req_col < COLUMN_INDEXES[len_cols]:
        Stamp(f'Column check passed, {req_col} < {COLUMN_INDEXES[len_cols]}', 's')
        return True
    else:
        Stamp('Column check failed', 'w')
        return False
