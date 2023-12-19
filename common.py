import configparser
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

import requests
from colorama import Fore, Style, init
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

init()
random.seed()
START = time.time()
CREDS = service_account.Credentials.from_service_account_file('keys.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])


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
    except IndexError:
        width = 1
    try:
        res = service.spreadsheets().values().update(spreadsheetId=sheet_id,
                                                     range=f'{sheet_name}!A{row}:{COLUMN_INDEXES[width]}{row + len(list_of_rows)}',
                                                     valueInputOption='USER_ENTERED', body=body).execute()
    except HttpError as err:
        Stamp(f'Status = {err} on uploading data to sheet {sheet_name}', 'e')
        return False
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror):
        Stamp(f'Connection on uploading data to sheet {sheet_name}', 'e')
        return False
    else:
        Stamp(f'On uploading: {res.get('updatedRows')} rows in range {res.get('updatedRange')}', 's')
        return True


def SwitchIndicator(color: str, sheet_name: str, width: int, sheet_id: str, service):
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
        response = service.spreadsheets().get(spreadsheetId=sheet_id, ranges=[sheet_name],
                                              includeGridData=False).execute()
        sample['requests'][0]['repeatCell']['range']['sheetId'] = response.get('sheets')[0].get('properties').get(
            'sheetId')
        service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body=sample).execute()
    except HttpError as err:
        Stamp(f'Status = {err} on switching indicator for sheet {sheet_name}', 'e')
        return False
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror):
        Stamp(f'Connection on switching indicator for sheet {sheet_name}', 'e')
        return False
    else:
        Stamp(f'On switching sheet {sheet_name}', 's')
        return True


def BuildService():
    Stamp(f'Trying to build service', 'i')
    try:
        service = build('sheets', 'v4', credentials=CREDS)
    except (HttpError, TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror):
        Stamp('Connection error on building service', 'e')
        Sleep(60, 0)
        BuildService()
    else:
        Stamp('Built service successfully', 's')
        return service


def ExecuteRetry(start: int, timeout: int, name: str, timer: int, func, *args, ratio=0.0):
    while not func(*args):
        ControlTimeout(start, timeout, name)
        Sleep(timer, ratio)


def Sleep(timer: int, ratio=0.0):
    rand_time = random.randint(int((1 - ratio) * timer), int((1 + ratio) * timer))
    Stamp(f'Sleeping for {rand_time} seconds', 'l')
    for _ in range(rand_time):
        time.sleep(1)


def ControlTimeout(start: int, timeout: int, name: str):
    elapsed = int(time.time() - start)
    if elapsed > timeout:
        Stamp(f'Timeout: elapsed {elapsed}, while allowed is {timeout}', 'e')
        SendEmail(f'{name} FAIL: elapsed {elapsed}, allowed {timeout}!')
        sys.exit()
    else:
        Stamp(f'Timeout OK: elapsed time is {elapsed}, while allowed is {timeout}', 'i')


def ParseConfig(direct: str):
    config = configparser.ConfigParser()
    config.read(Path.cwd() / direct / 'config.ini', encoding='utf-8')
    sections = config.sections()
    return config, sections


def ParseGmailConfig():
    config = configparser.ConfigParser()
    config.read(Path.cwd() / 'config.ini', encoding='utf-8')
    user = config['Gmail']['Login']
    password = config['Gmail']['Password']
    receiver = config['Gmail']['Receiver']
    return user, password, receiver


def SendEmail(theme: str):
    user, password, receiver = ParseGmailConfig()
    msg = MIMEMultipart()
    msg['Subject'] = theme
    try:
        Stamp('Trying to send the letter', 'i')
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
        Stamp('An error occurred: ' + str(e), 'e')


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


COLUMN_INDEXES = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
    10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T',
    20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z', 26: 'AA', 27: 'AB', 28: 'AC', 29: 'AD',
    30: 'AE', 31: 'AF', 32: 'AG', 33: 'AH', 34: 'AI', 35: 'AJ', 36: 'AK', 37: 'AL', 38: 'AM', 39: 'AN',
    40: 'AO', 41: 'AP', 42: 'AQ', 43: 'AR', 44: 'AS', 45: 'AT', 46: 'AU', 47: 'AV', 48: 'AW', 49: 'AX',
    50: 'AY', 51: 'AZ', 52: 'BA', 53: 'BB', 54: 'BC', 55: 'BD', 56: 'BE', 57: 'BF', 58: 'BG', 59: 'BH',
    60: 'BI', 61: 'BJ', 62: 'BK', 63: 'BL', 64: 'BM', 65: 'BN', 66: 'BO', 67: 'BP', 68: 'BQ', 69: 'BR'
}
