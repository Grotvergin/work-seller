from bot.checker.main import *
from bot.report.main import *


config, sections = ParseConfig('bot')
bot = telebot.TeleBot(config[sections[0]]['Token'])
MAX_LEN = 3000
TIME_CHECKER = '00:00'
TIME_REPORT = '17:05:00'
PATH_TO_DB = 'bot/chats.txt'
