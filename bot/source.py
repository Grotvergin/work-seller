from bot.checker.main import *
from bot.report.main import *


config, sections = ParseConfig('bot')
bot = telebot.TeleBot(config[sections[1]]['Token'])
TIME_CHECKER = '00:00'
TIME_REPORT = '17:05:00'
PATH_TO_DB = 'bot/chats.txt'
