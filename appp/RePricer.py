import pandas as pd
import gspread
import os
import os.path
import requests
import subprocess
import time
import json
import shlex
import datetime
from datetime import timedelta
from datetime import datetime as dt
import json
import sqlite3
from appp.pandi import calk

def repricer(db_name):
    # Путь к файлу базы данных
    db_file = f'db/{db_name}.db'
    # Подключение к базе данных
    conn = sqlite3.connect(db_file)
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()
    # Получение списка таблиц в базе данных
    df = pd.read_sql_query('SELECT * FROM setttings', conn)
    conn.close()

    artikuls_list = df['nmid'].tolist()
    for art_id in artikuls_list:
        strategy = df[df['nmid'] == art_id]['strat'].tolist()[0]
        df_calk = calk(db_name, 'skald')#мин цена
        df_zakaz = pd.read_sql_query(f'SELECT * FROM orders WHERE date_add >= {(dt.now()-timedelta(days=5)).strftime("%Y-%m-%d")} AND date_add != {(dt.now()).strftime("%Y-%m-%d")}', conn)
        sebestoimost = 275.09
        min_marga = 0.05
        desired_marga = 0.2
        mp_costs = 0.376 #тут можно более подробно - хранение, комиссии, рекламы... можно брать из детализаций!))
        company_costs1 = 0.168
        company_costs2 = 0.098  #тут намного точнее цифрой... иначе делаем уточнение, что эти проценты будут правдой только 
                                #при правильном рассчете этих процентов - значит при выполнении плана. за это мы ответственности не несем...
        auto_approve = False
        period_analiza = 2 #дней
        step = 50 #Шаг в рублях или процентах. Определяем по флагу
        interval_normalnosti = 20 #то есть 20% - коридор нормальности... то есть плс и минус 10% от среднего - норма, остальное выше или ниже!
        min_rekomended_price = round((sebestoimost / (1 - min_marga - mp_costs - company_costs1 - company_costs2)),2)
        period_posle_izmeneniy = 49 #часов НАДО ПОДУМАТЬ ОТКУДА ЭТО БРАТЬ... БД видимо...
        date_format = '%d-%m-%Y'
        DATA_VCHERA = datetime.date.today()- timedelta (days=2*period_analiza)
        d1=DATA_VCHERA.strftime("%Y-%m-%d")

        if strategy == 'max_profit':
            suggested_price = None
            sales_by_art = art_id
            if len(df_zakaz['date_add'].unique()) > 4: #проверяем на количество дней продаж - не новинка ли???
                sales_before = df_zakaz[(df_zakaz['date_add'] <= (dt.now()-timedelta(days=3)).strftime('%Y-%m-%d')) & (df_zakaz['nmid'] == art_id)]
                sales_now = df_zakaz[(df_zakaz['date_add'] > (dt.now()-timedelta(days=3)).strftime('%Y-%m-%d'))& (df_zakaz['nmid'] == art_id)]


                sell_rate_before = len(sales_before['date_add'].tolist()) / 2 #SDP
                sell_rate_now = len(sales_now['date_add'].tolist()) / 2 #SDP
                

                if sell_rate_now >= sell_rate_before:
                    new_price = df_calk[df_calk['Артикул МП'] == art_id]['Цена с СПП'] +  step #в скрипте переменная, потом из бд
                    
                elif sell_rate_now < sell_rate_before*(1-interval_normalnosti/200):
                    new_price = df_calk[df_calk['Артикул МП'] == art_id]['Цена с СПП'] -  step
                    if new_price < df_calk[df_calk['Артикул МП'] == art_id]['Мин. цена']:
                        new_price = df_calk[df_calk['Артикул МП'] == art_id]['Мин. цена']
                        
                else:
                    print('цена не изменилась')#send to log
                    new_price = 0
                df[df['nmid'] == art_id]['new_price'] = new_price
                df[df['nmid'] == art_id]['cab'] = df_zakaz[df_zakaz['nmid'] == art_id]['cabinet'].unique().tolist()[0]
                new_disk(df, db_name)
            else:
                print('Нет данных для анализа')#send to log
        else:
            pass
        





def new_disk(df, db_name):
    # Путь к файлу базы данных
    db_file = f'db/{db_name}.db'
    # Подключение к базе данных
    conn = sqlite3.connect(db_file)
    tokens = pd.read_sql_query('SELECT cabinet, tokenPrice FROM cabinet', conn)

    df_price = pd.read_sql_query('SELECT * FROM price', conn)
    df_big = pd.merge(df, df_price, on='nmid')
    df_big = df_big.dropna(subset=['new_price'])
    df_big['disc_new'] = (df_big['price'] - df_big['new_price'])/df_big['price']*100

    for cab in tokens['cabinet'].tolist():
        df_big[df_big['cabinet'] == cab]['token'] = tokens[tokens['cabinet'] == cab]['tokenPrice'].tolist()[0]
    update_price_on_WB(df_big)




def update_price_on_WB( df: pd.DataFrame):
    from appp.wb_req import WBrequest
    art_ap = []
    for cab in df['cab'].unique():
        df_cab = df[df['cab'] == cab]   
        for row in df_cab.iterrows():
            d = {
                "nmID": row.nmid,
                "discount": row.disc_new    #пересчет скидки
                }
            art_ap.append(d)

        json = {
            "data": art_ap
            }

        headers = {
            'accept': 'application/json',
            'Authorization': df_cab['token'].unique()[0]
        }

        response = requests.post('https://discounts-prices-api.wildberries.ru/api/v2/upload/task',headers=headers, json=json ) 
        print(response.status_code, response.text) #log history





