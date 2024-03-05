from common import *

PATH = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')
NAME_SOURCE = 'Приёмки на складах ФФ'
NAME_OUTPUT = 'Report'
COLUMN_ID = 'B'
START_ROW = 6
END_ROWS = {
    'Bathroom': 185,
    'Lighting': 92,
    'Dishes': 93
}
LEN_COLS = 2
ROW_TO_CHECK = 4
