from common import *
import telebot
from telegram.ext import JobQueue, CommandHandler

LONG_SLEEP = 90
SHORT_SLEEP = 1
BLANK_ROWS = 50000
NAME = 'Bot'
URL = 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks'
ROWS = ['supplierArticle', 'quantity', 'time']
DATE_FROM = '2023-06-06'
TIMEOUT = 360000
SHEET_ID = '1rmXz1joBFlYDkPK4gY0BkbNaqAzhQ9F6Nle6xe-w4LE'
MAX_DIFF = 10
INTERVAL = 3600
