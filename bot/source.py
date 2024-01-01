from bot.checker.main import *
from bot.report.main import *


NAME = os.path.dirname(os.path.realpath(__file__)).rsplit('\\', 1)[-1]
config, sections = ParseConfig(NAME)
bot = telebot.TeleBot(config[sections[0]]['Token'])
TIME_CHECKER = '00:00'
TIME_REPORT = '17:05:00'
PATH_TO_DB = NAME + '/chats.txt'
