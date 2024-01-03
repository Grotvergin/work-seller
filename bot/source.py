from bot.checker.main import *
from bot.report.main import *


NAME = os.path.dirname(os.path.realpath(__file__)).rsplit('\\', 1)[-1]
config, sections = ParseConfig(NAME)
bot = telebot.TeleBot(config[sections[1]]['Token'])
TIME_CHECKER = '00:70'
TIME_REPORT = '17:05:00'
PATH_TO_DB = NAME + '/database/'
REJECT = '❌ Не получать уведомления'
ACCEPT = '✅ Получать все уведомления'
SOME_CHECKER = '✔️ Получать только непустые уведомления'
SOME_STATUS = '✔️ Получать только уведомления о провалах'
CHOOSE = '❔ Сделайте выбор:'
MANAGE_SERVICE = 'Обновить сервис 📊'
MANAGE_NOTIFY = 'Управление уведомлениями 🔔'
UNKNOWN = '🔴 Неизвестная опция...'
MAX_PROCESSES = 2
