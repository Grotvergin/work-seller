import configparser
import ssl
import httplib2
import json
import random
import smtplib
import socket
import sys
import time
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from functools import wraps
from threading import Thread


import requests
from colorama import Fore, Style, init
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import telebot

init()
random.seed()
START = time.time()
CREDS = service_account.Credentials.from_service_account_file('keys.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
MAX_ROW = 10000
MAX_RECURSION = 10


def ControlRecursion(func, maximum=MAX_RECURSION):
    func.recursion_depth = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        if func.recursion_depth >= maximum:
            Stamp('Max level of recursion reached', 'e')
            return None
        func.recursion_depth += 1
        Stamp(f"Recursion = {func.recursion_depth}, allowed = {maximum}", 'i')
        result = func(*args, **kwargs)
        func.recursion_depth -= 1
        return result
    return wrapper


def SmartLen(data):
    try:
        length = len(data)
    except TypeError:
        length = 0
    return length


def GetRow(row: int, service, sheet_name: str, timeout: int, name: str, sheet_id: str, timer: int):
    Stamp(f'Trying to get row {row} from sheet {sheet_name}', 'i')
    ControlTimeout(timeout, name)
    last_index = list(COLUMN_INDEXES.keys())[-1]
    try:
        res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'{sheet_name}!A{row}:{last_index}{row}').execute().get('values', [])
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror, HttpError, ssl.SSLEOFError) as err:
        Stamp(f'Status = {err} on getting row {row} from sheet {sheet_name}', 'e')
        Sleep(timer)
        res = GetRow(row, service, sheet_name, timeout, name, sheet_id, timer)
    else:
        if not res:
            Stamp(f'No elements in row {row} sheet {sheet_name} found', 'w')
        else:
            res = res[0]
            Stamp(f'Found {len(res)} elements from row {row} sheet {sheet_name}', 's')
    return res


def GetColumn(column: str, service, sheet_name: str, timeout: int, name: str, sheet_id: str, timer: int):
    Stamp(f'Trying to get column {column} from sheet {sheet_name}', 'i')
    ControlTimeout(timeout, name)
    try:
        res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'{sheet_name}!{column}2:{column}{MAX_ROW}').execute().get('values', [])
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror, HttpError, ssl.SSLEOFError) as err:
        Stamp(f'Status = {err} on getting column {column} from sheet {sheet_name}', 'e')
        Sleep(timer)
        res = GetColumn(column, service, sheet_name, timeout, name, sheet_id, timer)
    else:
        if not res:
            Stamp(f'No elements in column {column} sheet {sheet_name} found', 'w')
        else:
            Stamp(f'Found {len(res)} elements from column {column} sheet {sheet_name}', 's')
            res = [item for sublist in res for item in sublist]
    return res


def Finish(timeout: int, name: str):
    ControlTimeout(timeout, name)
    SendEmail(f'{name} OK: elapsed {int(time.time() - START)}')
    Stamp('All data was uploaded successfully', 'b')


def PrepareEmpty(width: int, blank: int):
    list_of_empty = []
    one_row = [''] * width
    for k in range(blank):
        list_of_empty.append(one_row)
    return list_of_empty


def UploadData(list_of_rows: list, sheet_name: str, sheet_id: str, service, row=2):
    body = {'values': list_of_rows}
    try:
        width = len(list_of_rows[0])
    except (IndexError, KeyError):
        width = 1
    try:
        res = service.spreadsheets().values().update(spreadsheetId=sheet_id,
                                                     range=f'{sheet_name}!A{row}:{COLUMN_INDEXES[width]}{row + len(list_of_rows)}',
                                                     valueInputOption='USER_ENTERED', body=body).execute()
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror, HttpError, ssl.SSLEOFError) as err:
        Stamp(f'Status = {err} on uploading data to sheet {sheet_name}', 'e')
        return False
    else:
        Stamp(f"On uploading: {res.get('updatedRows')} rows in range {res.get('updatedRange')}", 's')
        return True


def SwitchIndicator(color: str, sheet_name: str, width: int, sheet_id: str, service):
    Stamp(f'Trying to switch sheet {sheet_name}', 'i')
    sample = {
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
    if color == 'r':
        sample['requests'][0]['repeatCell']['cell']['userEnteredFormat']['backgroundColor']['red'] = 1.0
    else:
        sample['requests'][0]['repeatCell']['cell']['userEnteredFormat']['backgroundColor']['green'] = 1.0
    sample['requests'][0]['repeatCell']['range']['endColumnIndex'] = width
    try:
        response = service.spreadsheets().get(spreadsheetId=sheet_id, ranges=[sheet_name], includeGridData=False).execute()
        sample['requests'][0]['repeatCell']['range']['sheetId'] = response.get('sheets')[0].get('properties').get('sheetId')
        service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body=sample).execute()
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror, HttpError, ssl.SSLEOFError) as err:
        Stamp(f'Status = {err} on switching sheet {sheet_name}', 'e')
        return False
    else:
        Stamp(f'On switching sheet {sheet_name}', 's')
        return True


def BuildService():
    Stamp(f'Trying to build service', 'i')
    try:
        service = build('sheets', 'v4', credentials=CREDS)
    except (HttpError, TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror, ssl.SSLEOFError) as err:
        Stamp(f'Status = {err} on building service', 'e')
        Sleep(60)
        BuildService()
    else:
        Stamp('Built service successfully', 's')
        return service


def ExecuteRetry(timeout: int, name: str, timer: int, func, *args, ratio=0.0):
    while not func(*args):
        ControlTimeout(timeout, name)
        Sleep(timer, ratio)


def Sleep(timer: int, ratio=0.0):
    rand_time = random.randint(int((1 - ratio) * timer), int((1 + ratio) * timer))
    Stamp(f'Sleeping for {rand_time} seconds', 'l')
    for _ in range(rand_time):
        time.sleep(1)


def ControlTimeout(timeout: int, name: str):
    elapsed = int(time.time() - START)
    if elapsed > timeout:
        Stamp(f'Timeout: elapsed {elapsed}, while allowed is {timeout}', 'e')
        SendEmail(f'{name} FAIL: elapsed {elapsed}, allowed {timeout}!')
        sys.exit()
    else:
        Stamp(f'Timeout OK: elapsed time is {elapsed}, while allowed is {timeout}', 'i')


def ParseConfig(direct=''):
    config = configparser.ConfigParser()
    config.read(Path.cwd() / direct / 'config.ini', encoding='utf-8')
    sections = config.sections()
    return config, sections


def ParseGmailConfig(config):
    user = config['Gmail']['Login']
    password = config['Gmail']['Password']
    receiver = config['Gmail']['Receiver']
    return user, password, receiver


def SendEmail(theme: str):
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


def Stamp(message: str, level: str):
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


def MakeColumnIndexes():
    indexes = {}
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i, letter in enumerate(alphabet):
        indexes[i] = letter
    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            indexes[len(alphabet) + i * len(alphabet) + j] = alphabet[i] + alphabet[j]
    return indexes


COLUMN_INDEXES = MakeColumnIndexes()
