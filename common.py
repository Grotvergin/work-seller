# Built-in
import json
import random
import smtplib
import socket
import ssl
import sys
import time
import os
from configparser import ConfigParser
from datetime import datetime, timedelta, date
from email.mime.multipart import MIMEMultipart
from functools import wraps
from pathlib import Path
from pprint import pprint
from threading import Thread
from typing import Union, Callable, Any, List, Dict


# External
import googleapiclient.discovery
import httplib2
import requests
import telebot
from colorama import Fore, Style, init
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


init()
random.seed()
CREDS = service_account.Credentials.from_service_account_file('keys.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
MAX_ROW = 50000
MAX_RECURSION = 10
SLEEP_GOOGLE = 20
MSG = 'NoData'
START = time.time()
PREFIX_MONTH = 'Month'
START_OF_MONTH = datetime.now().strftime('%Y-%m') + '-01'
TODAY = datetime.now().strftime('%Y-%m-%d')
YEAR = datetime.now().strftime('%Y')
MONTH = datetime.now().strftime('%m')


def CleanSheet(width: int, sheet_name: str, sheet_id: str, service: googleapiclient.discovery.Resource, column: str = 'A'):
    Stamp(f'Trying to clean sheet {sheet_name}', 'i')
    height = len(GetColumn(column, service, sheet_name, sheet_id))
    empty = PrepareEmpty(width, height)
    UploadData(empty, sheet_name, sheet_id, service)


def ControlRecursion(func: Callable[..., Any], maximum: int = MAX_RECURSION) -> Callable[..., Any]:
    func.recursion_depth = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        if func.recursion_depth > maximum:
            Stamp('Max level of recursion reached', 'e')
            SendEmail('Recursion FAIL')
            sys.exit()
        if func.recursion_depth > 0:
            Stamp(f"Recursion = {func.recursion_depth}, allowed = {maximum}", 'w')
        func.recursion_depth += 1
        result = func(*args, **kwargs)
        func.recursion_depth -= 1
        return result
    return wrapper


def SmartLen(data: Union[List, Dict]) -> int:
    try:
        length = len(data)
    except TypeError:
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
def GetColumn(column: str, service: googleapiclient.discovery.Resource, sheet_name: str, sheet_id: str) -> list:
    Stamp(f'Trying to get column {column} from sheet {sheet_name}', 'i')
    try:
        res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'{sheet_name}!{column}2:{column}{MAX_ROW}').execute().get('values', [])
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror, HttpError, ssl.SSLEOFError) as err:
        Stamp(f'Status = {err} on getting column {column} from sheet {sheet_name}', 'e')
        Sleep(SLEEP_GOOGLE)
        res = GetColumn(column, service, sheet_name, sheet_id)
    else:
        if not res:
            Stamp(f'No elements in column {column} sheet {sheet_name} found', 'w')
        else:
            Stamp(f'Found {len(res)} elements from column {column} sheet {sheet_name}', 's')
            res = [item for sublist in res for item in sublist]
    return res


def Finish(name: str) -> None:
    SendEmail(f'{name} OK: elapsed {int(time.time() - START)}')
    Stamp('All data was uploaded successfully', 'b')


def PrepareEmpty(width: int, blank: int) -> list:
    list_of_empty = []
    one_row = [''] * width
    for k in range(blank):
        list_of_empty.append(one_row)
    return list_of_empty


@ControlRecursion
def UploadData(list_of_rows: list, sheet_name: str, sheet_id: str, service: googleapiclient.discovery.Resource, row: int = 2) -> None:
    Stamp(f'Trying to upload data to sheet {sheet_name}', 'i')
    try:
        width = SmartLen(list_of_rows[0])
    except IndexError:
        width = 0
    SwitchIndicator('r', sheet_name, width, sheet_id, service)
    body = {'values': list_of_rows}
    try:
        res = service.spreadsheets().values().update(spreadsheetId=sheet_id,
                                                     range=f'{sheet_name}!A{row}:{COLUMN_INDEXES[width]}{row + len(list_of_rows)}',
                                                     valueInputOption='USER_ENTERED', body=body).execute()
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror, HttpError, ssl.SSLEOFError) as err:
        Stamp(f'Status = {err} on uploading data to sheet {sheet_name}', 'e')
        Sleep(SLEEP_GOOGLE)
        UploadData(list_of_rows, sheet_name, sheet_id, service, row)
    else:
        SwitchIndicator('g', sheet_name, width, sheet_id, service)
        Stamp(f"On uploading: {res.get('updatedRows')} rows in range {res.get('updatedRange')}", 's')


@ControlRecursion
def SwitchIndicator(color: str, sheet_name: str, width: int, sheet_id: str, service: googleapiclient.discovery.Resource) -> None:
    Stamp(f'Trying to switch sheet {sheet_name}', 'i')
    sample = SAMPLE_SWITCH.copy()
    if color == 'r':
        sample['requests'][0]['repeatCell']['cell']['userEnteredFormat']['backgroundColor']['red'] = 1.0
        sample['requests'][0]['repeatCell']['cell']['userEnteredFormat']['backgroundColor']['green'] = 0.0
    else:
        sample['requests'][0]['repeatCell']['cell']['userEnteredFormat']['backgroundColor']['green'] = 1.0
        sample['requests'][0]['repeatCell']['cell']['userEnteredFormat']['backgroundColor']['red'] = 0.0
    sample['requests'][0]['repeatCell']['range']['endColumnIndex'] = width
    try:
        response = service.spreadsheets().get(spreadsheetId=sheet_id, ranges=[sheet_name], includeGridData=False).execute()
        sample['requests'][0]['repeatCell']['range']['sheetId'] = response.get('sheets')[0].get('properties').get('sheetId')
        service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body=sample).execute()
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror, HttpError, ssl.SSLEOFError) as err:
        Stamp(f'Status = {err} on switching sheet {sheet_name}', 'e')
        Sleep(SLEEP_GOOGLE)
        SwitchIndicator(color, sheet_name, width, sheet_id, service)
    else:
        Stamp(f'On switching sheet {sheet_name}', 's')


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
    for _ in range(rand_time):
        time.sleep(1)


def ParseConfig(direct: str = '') -> (ConfigParser, list):
    config = ConfigParser()
    config.read(Path.cwd() / direct / 'config.ini', encoding='utf-8')
    sections = config.sections()
    return config, sections


def ParseGmailConfig(config: ConfigParser) -> (str, str, str):
    user = config['DEFAULT']['Login']
    password = config['DEFAULT']['Password']
    receiver = config['DEFAULT']['Receiver']
    return user, password, receiver


def SendEmail(theme: str) -> None:
    config, sections = ParseConfig()
    user, password, receiver = ParseGmailConfig(config)
    msg = MIMEMultipart()
    msg['Subject'] = theme
    Stamp('Trying to send the letter', 'i')
    try:
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login(user, password)
        Stamp('Gmail authorization success', 's')
        smtp_server.sendmail(user, receiver, msg.as_string())
        Stamp('Gmail letter sending success', 's')
    except smtplib.SMTPAuthenticationError:
        Stamp('Authentication failed', 'e')
    except smtplib.SMTPRecipientsRefused:
        Stamp('Server refused the recipient address', 'e')
    except Exception as e:
        Stamp(f'An error occurred: {e}', 'e')


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

SAMPLE_SWITCH = {
        'requests': [
            {
                'repeatCell': {
                    'range': {
                        'startRowIndex': 0,
                        'endRowIndex': 1,
                        'startColumnIndex': 0
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': {
                                'red': 0.0,
                                'green': 0.0,
                                'blue': 0.0,
                                'alpha': 0.5
                            }
                        }
                    },
                    'fields': 'userEnteredFormat.backgroundColor'
                }
            }
        ]
    }
