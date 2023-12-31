from bot.checker.main import *
from bot.report.main import *


NAME = 'Bot'
config, sections = ParseConfig(NAME.lower())
bot = telebot.TeleBot(config[sections[0]]['Token'])
TIME_CHECKER = '00:00'
TIME_REPORT = '17:05:00'
PATH_TO_DB = NAME.lower() + '/chats.txt'
