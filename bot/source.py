from bot.checker.main import *
from bot.report.main import *
from bot.farafon.main import *


NAME = os.path.dirname(os.path.realpath(__file__)).rsplit('\\', 1)[-1]
config, sections = ParseConfig(NAME)
bot = telebot.TeleBot(config[sections[int(DEBUG_MODE)]]['Token'])
REJECT = '❌ Не получать уведомления'
ACCEPT = '✅ Получать все уведомления'
SOME_CHECKER = '✔️ Получать только непустые уведомления'
SOME_STATUS = '✔️ Получать только уведомления о провалах'
CHOOSE = '❔ Сделайте выбор:'
MANAGE_SERVICE = 'Обновить сервис 📊'
MANAGE_NOTIFY = 'Управление уведомлениями 🔔'
UNKNOWN = '🔴 Неизвестная опция...'
CABINETS_ACCEPTANCE = {
    'Освещение (LUMIRE) 💡': 'Lighting',
    'Сантехника (WODOR) 🚰': 'Bathroom',
    'Посуда (FOODTERIA) 🍽': 'Dishes',
    'Вернуться на главную ◀️': '/start'
}
CUR_CAB_ACCEPTANCE = None
