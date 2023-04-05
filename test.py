from __future__ import print_function
import time
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from usd_to_rub import get_currency_rate

import psycopg2
from psycopg2 import Error

from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1f-qZEX1k_3nj5cahOzntYAnvO4ignbyesVO7yuBdv_g'
SAMPLE_RANGE_NAME = 'Лист1'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        return values

    except HttpError as err:
        print(err)





def create_rows():
    try:
        # Подключиться к существующей базе данных
        connection = psycopg2.connect(
            user="postgres",
            # пароль, который указали при установке PostgreSQL
            password="812314",
            host="127.0.0.1",
            port="5432",
            database="test_sheets")

        # Создайте курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # # SQL-запрос для создания новой таблицы
        # create_table_query = '''CREATE TABLE orders
        #                       (ID  BIGSERIAL PRIMARY KEY   ,
        #                       № INT NOT NULL,
        #                       ЗАКАЗ_№           INT    NOT NULL,
        #                       СТОИМОСТЬ_$         REAL,
        #                       СРОК_ПОСТАВКИ DATE,
        #                       СТОИМОСТЬ_Р REAL); '''
        # # # Выполнение команды: это создает новую таблицу

        # cursor.execute(create_table_query)
        # connection.commit()
        # print("Таблица успешно создана в PostgreSQL")
        
        

        
        
        cursor.execute('''DELETE FROM orders;''')
        for i,value in enumerate(values[1:]):
            
            rate_ruble=float(value[2])*get_currency_rate()
            print(rate_ruble)
            command=f'''INSERT INTO orders (№, ЗАКАЗ_№, СТОИМОСТЬ_$, СРОК_ПОСТАВКИ, СТОИМОСТЬ_Р)
            VALUES ({value[0]}, {value[1]},{value[2]},'{value[3].replace(".","-")}', {rate_ruble});'''
            
            cursor.execute(command)
        print("все добавилось")
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
            
time_script=time.time()
while True:
    if time.time()-time_script>5:
        time_script=time.time()
        values = main()
        create_rows()
    