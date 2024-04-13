# Built-in
import json
import random
import subprocess
import socket
import ssl
import sys
import time
import os
from configparser import ConfigParser
from datetime import datetime, timedelta, date
from functools import wraps
from pathlib import Path
from threading import Thread, Lock
from html.parser import HTMLParser
from typing import Union, Callable, Any, List, Dict, Generator
import traceback
import re

# External
import googleapiclient.discovery
import httplib2
import requests
import telebot
from colorama import Fore, Style, init
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import undetected_chromedriver
from fastapi import FastAPI
import uvicorn


init()
random.seed()
CREDS = service_account.Credentials.from_service_account_file('keys.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
MAX_ROW = 400000
MAX_RECURSION = 15
SLEEP_GOOGLE = 20
SIZE_CHUNK = 5000
START = time.time()
START_OF_MONTH = datetime.now().strftime('%Y-%m') + '-01'
TODAY = datetime.now().strftime('%Y-%m-%d')
YEAR = datetime.now().strftime('%Y')
MONTH = datetime.now().strftime('%m')
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
MSG = 'NoData'
PREFIX_MONTH = 'Month'
PATH_DB = str(Path.cwd()) + '/bot/database/'
DEBUG_MODE = False
MAX_PROCESSES = 5
os.environ['PYTHONIOENCODING'] = 'utf-8'
file_lock = Lock()
NAMES = {
    'top': 'Top V Top 🔝',
    'statist': 'WB Статистика 📊',
    'prices': 'WB Цены 🏷',
    'parsers-h': 'WB Частый парсинг ⏭',
    'parsers-d': 'WB Ежедневный парсинг ⏩',
    'funnel': 'WB Аналитика 🔍',
    'discharge': 'OZON Выгрузка 🗂',
    'checker': 'Увеличение остатков ⚡️',
    'report': 'Отчёт по дате 📅',
    'analytics': 'OZON Аналитика 🔎',
    'advert': 'WB Реклама 💸',
    'status': 'Статус обновлений 🆗',
    'farafon': 'Отчёт по приёмкам 📦',
    'pricepec': 'WB Цены по сайту 🛒',
    'monstr': 'MarketMonstr 👹',
    'selozon': 'OZON Кабинет продавца 🧾',
    'graphs': 'OZON Графики 📈',
    'stencil': 'OZON Трафареты 📐',
    'search': 'OZON Продвижение в поиске 🎛'
}


def ReadLinesFromFile(path: Union[str, Path]) -> list:
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return lines


def Inspector(name: str) -> Callable[..., Any]:
    def Decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def Wrapper(*args, **kwargs):
            if AddToDatabase(name, PATH_DB + 'active.txt', True):
                IndependentSender(f'🔴 Процесс {NAMES[name]} уже запущен, либо достигнут предел в {MAX_PROCESSES} процесса...', 'status', True)
                Stamp(f'Check failed: rejecting starting of {name}', 'w')
            else:
                Stamp(f'Check passed: starting {name}', 's')
                result = None
                try:
                    result = func(*args, **kwargs)
                    Stamp('All data uploaded successfully', 'b')
                    IndependentSender(f'🟢 Успешное обновление {NAMES[name]}', 'status')
                except KeyboardInterrupt:
                    Stamp('Keyboard interruption', 'w')
                except RecursionError:
                    Stamp('On recursion', 'e')
                    IndependentSender(f'🔴 Рекурсивная ошибка при обновлении {NAMES[name]}', 'status', True)
                except Exception as e:
                    Stamp(f'The following happened:\n{e}', 'e')
                    Stamp(traceback.format_exc(), 'e')
                    IndependentSender(f'🔴 Ошибка при обновлении {NAMES[name]}', 'status', True)
                finally:
                    RemoveFromDatabase(name, PATH_DB + 'active.txt')
                    return result
        return Wrapper
    return Decorator


def AddToDatabase(note: str, path: str, len_check: bool = False) -> bool:
    with file_lock:
        Stamp(f'Adding note {note} to DB {path}', 'i')
        found = False
        with open(Path.cwd() / path, 'r', encoding='utf-8') as f:
            for line in f:
                Stamp(line, 'i')
                if line.strip() == note:
                    found = True
                    break
        if not found:
            if len_check and SmartLen(ReadLinesFromFile(path)) >= MAX_PROCESSES:
                found = True
            else:
                with open(Path.cwd() / path, 'a') as f:
                    f.write(note + '\n')
    return found


def RemoveFromDatabase(note: str, path: str) -> bool:
    with file_lock:
        Stamp(f'Removing note {note} from DB {path}', 'i')
        found = False
        lines = ReadLinesFromFile(path)
        for line in lines:
            if line.strip() == note:
                found = True
                break
        if found:
            with open(Path.cwd() / path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.strip() != note:
                        f.write(line)
    return found


def GroupSender(msg: list[str], name: str):
    Stamp('Trying to send notifications to numerous groups', 'i')
    config, sections = ParseConfig('bot')
    token = config[sections[int(DEBUG_MODE)]]['Token']
    groups = ReadLinesFromFile(PATH_DB + name + '.txt')
    for i in range(SmartLen(groups)):
        SendTelegramNotify(f'🟢 Отображаю отчёт за {YESTERDAY}', token, groups[i])
        SendTelegramNotify(msg[i], token, groups[i])


def IndependentSender(msg: Union[str, list[str]], name: str, important: bool = False):
    Stamp('Trying to send notifications to numerous users', 'i')
    config, sections = ParseConfig('bot')
    token = config[sections[int(DEBUG_MODE)]]['Token']
    file_names = [name + '.txt', name + '_important.txt'] if important else [name + '.txt']
    for file in file_names:
        for user in ReadLinesFromFile(PATH_DB + file):
            if isinstance(msg, str):
                SendTelegramNotify(msg, token, int(user))
            elif msg:
                for m in msg:
                    SendTelegramNotify(m, token, int(user))
            else:
                SendTelegramNotify('▪️Нет изменений/пустое сообщение', token, int(user))


def SendTelegramNotify(msg: str, token: str, user: int) -> None:
    Stamp(f'Trying to send notification to user {user}', 'i')
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': user,
        'text': msg,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(url, data=payload)
    except requests.ConnectionError:
        Stamp('On connection for sending telegram notification', 'e')
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} telegram notification', 's')
        else:
            Stamp(f'Status = {response.status_code} telegram notification', 'e')


def CleanSheet(width: int, sheet_name: str, sheet_id: str, service: googleapiclient.discovery.Resource, column: str = 'A'):
    Stamp(f'Trying to clean sheet {sheet_name}', 'i')
    height = len(GetColumn(column, service, sheet_name, sheet_id))
    empty = PrepareEmpty(width, height)
    UploadData(empty, sheet_name, sheet_id, service)


def ControlRecursion(func: Callable[..., Any], maximum: int = MAX_RECURSION) -> Callable[..., Any]:
    func.recursion_depth = 0

    @wraps(func)
    def Wrapper(*args, **kwargs):
        if func.recursion_depth > maximum:
            Stamp('Max level of recursion reached', 'e')
            raise RecursionError
        if func.recursion_depth > 0:
            Stamp(f"Recursion = {func.recursion_depth}, allowed = {maximum}", 'w')
        func.recursion_depth += 1
        result = func(*args, **kwargs)
        func.recursion_depth -= 1
        return result
    return Wrapper


def SmartLen(data: Union[List, Dict]) -> int:
    try:
        length = len(data)
    except (TypeError, KeyError):
        length = 0
    return length


@ControlRecursion
def GetRow(row: int, service: googleapiclient.discovery.Resource, sheet_name: str, sheet_id: str) -> list:
    Stamp(f'Trying to get row {row} from sheet {sheet_name}', 'i')
    last_index = list(COLUMN_INDEXES.keys())[-1]
    try:
        res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'{sheet_name}!A{row}:{last_index}{row}').execute().get('values', [])
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror, HttpError, ssl.SSLEOFError) as err:
        Stamp(f'Status = {err} on getting row {row} from sheet {sheet_name}', 'e')
        Sleep(SLEEP_GOOGLE)
        res = GetRow(row, service, sheet_name, sheet_id)
    else:
        if not res:
            Stamp(f'No elements in row {row} sheet {sheet_name} found', 'w')
        else:
            res = res[0]
            Stamp(f'Found {len(res)} elements from row {row} sheet {sheet_name}', 's')
    return res


@ControlRecursion
def GetColumn(column: str, service: googleapiclient.discovery.Resource, sheet_name: str, sheet_id: str, skip_empty: bool = True, start_row: int = 2, end_row: int = MAX_ROW) -> list:
    Stamp(f'Trying to get column {column} from sheet {sheet_name}', 'i')
    try:
        res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'{sheet_name}!{column}{start_row}:{column}{end_row}').execute().get('values', [])
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror, HttpError, ssl.SSLEOFError) as err:
        Stamp(f'Status = {err} on getting column {column} from sheet {sheet_name}', 'e')
        Sleep(SLEEP_GOOGLE)
        res = GetColumn(column, service, sheet_name, sheet_id, skip_empty, start_row, end_row)
    else:
        if not res:
            Stamp(f'No elements in column {column} sheet {sheet_name} found', 'w')
        else:
            Stamp(f'Found {len(res)} elements from column {column} sheet {sheet_name}', 's')
            if skip_empty:
                res = [item for sublist in res for item in sublist]
            else:
                res = [None if not sublist else item for sublist in res for item in (sublist if sublist else [None])]
    return res


def PrepareEmpty(width: int, blank: int) -> list:
    list_of_empty = []
    one_row = [''] * width
    for k in range(blank):
        list_of_empty.append(one_row)
    return list_of_empty


def LargeUpload(list_of_rows: list, sheet_name: str, sheet_id: str, service: googleapiclient.discovery.Resource, row: int = 2) -> None:
    chunks = [list_of_rows[i:i + SIZE_CHUNK] for i in range(0, len(list_of_rows), SIZE_CHUNK)]
    for i, chunk in enumerate(chunks):
        UploadData(chunk, sheet_name, sheet_id, service, row + i * SIZE_CHUNK)


@ControlRecursion
def UploadData(list_of_rows: list, sheet_name: str, sheet_id: str, service: googleapiclient.discovery.Resource, row: int = 2) -> None:
    Stamp(f'Trying to upload data to sheet {sheet_name}', 'i')
    try:
        width = SmartLen(list_of_rows[0])
    except IndexError:
        width = 0
    try:
        res = service.spreadsheets().values().update(spreadsheetId=sheet_id,
                                                 range=f'{sheet_name}!A{row}:{COLUMN_INDEXES[width]}{row + len(list_of_rows)}',
                                                 valueInputOption='USER_ENTERED', body={'values': list_of_rows}).execute()
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror, HttpError, ssl.SSLEOFError) as err:
        Stamp(f'Status = {err} on uploading data to sheet {sheet_name}', 'e')
        Sleep(SLEEP_GOOGLE)
        UploadData(list_of_rows, sheet_name, sheet_id, service, row)
    else:
        Stamp(f"On uploading: {res.get('updatedRows')} rows in range {res.get('updatedRange')}", 's')


@ControlRecursion
def BuildService() -> googleapiclient.discovery.Resource:
    Stamp(f'Trying to build service', 'i')
    try:
        service = build('sheets', 'v4', credentials=CREDS)
    except (HttpError, TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror, ssl.SSLEOFError) as err:
        Stamp(f'Status = {err} on building service', 'e')
        Sleep(SLEEP_GOOGLE)
        BuildService()
    else:
        Stamp('Built service successfully', 's')
        return service


def Sleep(timer: int, ratio: float = 0.0) -> None:
    rand_time = random.randint(int((1 - ratio) * timer), int((1 + ratio) * timer))
    Stamp(f'Sleeping {rand_time} seconds', 'l')
    time.sleep(rand_time)


def AccurateSleep(timer: float, ratio: float = 0.0) -> None:
    rand_time = round(random.uniform((1 - ratio) * timer, (1 + ratio) * timer), 2)
    Stamp(f'Sleeping {rand_time} seconds', 'l')
    time.sleep(rand_time)


def ParseConfig(direct: str = '') -> (ConfigParser, list):
    config = ConfigParser()
    config.read(Path.cwd() / direct / 'config.ini', encoding='utf-8')
    sections = config.sections()
    return config, sections


def Stamp(message: str, level: str) -> None:
    time_stamp = datetime.now().strftime('[%m-%d|%H:%M:%S]')
    match level:
        case 'i':
            print(Fore.LIGHTBLUE_EX + time_stamp + '[INF] ' + message + '.' + Style.RESET_ALL)
        case 'w':
            print(Fore.LIGHTMAGENTA_EX + time_stamp + '[WAR] ' + message + '!' + Style.RESET_ALL)
        case 's':
            print(Fore.LIGHTGREEN_EX + time_stamp + '[SUC] ' + message + '.' + Style.RESET_ALL)
        case 'e':
            print(Fore.RED + time_stamp + '[ERR] ' + message + '!!!' + Style.RESET_ALL)
        case 'l':
            print(Fore.WHITE + time_stamp + '[SLE] ' + message + '...' + Style.RESET_ALL)
        case 'b':
            print(Fore.LIGHTYELLOW_EX + time_stamp + '[BOR] ' + message + '.' + Style.RESET_ALL)
        case _:
            print(Fore.WHITE + time_stamp + '[UNK] ' + message + '?' + Style.RESET_ALL)


def MakeColumnIndexes() -> dict:
    indexes = {}
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i, letter in enumerate(alphabet):
        indexes[i] = letter
    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            indexes[len(alphabet) + i * len(alphabet) + j] = alphabet[i] + alphabet[j]
    return indexes


COLUMN_INDEXES = MakeColumnIndexes()

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:109.0) Gecko/20100101 Firefox/116.0',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0',
]
