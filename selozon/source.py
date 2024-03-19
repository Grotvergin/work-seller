from common import *


HEADLESS = True
SLEEP_CLICK = 1
MEDIUM_SLEEP = 60
MAX_TIME_TABLE = 300
NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
NAME_ALL = 'All'
COLUMNS = {
    'Word': None,
    'City': None,
    'Number': 0,
    'ID': 1,
    'Summary': 2,
    'Accordance': 3,
    'Popularity': 4,
    'Sales': 5,
    'General': 6,
    'Date': None
}
POSSIBLE_XPATH_CAB = ['//*[@id="app"]/div[1]/div/div[1]/div/div/div[1]/div/span',
                      '//*[@id="app"]/div[2]/div/div[1]/div/div/div[1]/div/span']
