from flask import Flask, render_template,  request, jsonify, make_response, send_file, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import base64
import pandas as pd
import sqlite3
from io import BytesIO
from datetime import timedelta
from flask import session
import datetime
from datetime import datetime
from flask_bcrypt import Bcrypt
import json

import time


def unit(*kwargs):
    comp = current_user.comp
    conn = sqlite3.connect(f'db/{comp}.db')
    if not check_table_exists(conn, 'sebes'):
        return render_template('auth/unit.html', error = 'Не добавлена таблица себестоимости! Добавьте ее на вкладке Кабинеты')
    from appp.pandi import calk as calk
    df_mp = calk(conn)
    return render_template('auth/unit.html', df=df_mp, enumerate=enumerate)





def check_table_exists(conn,table_name ):
    try:
        cursor = conn.cursor()
        # Выполняем запрос для проверки наличия таблицы
        cursor.execute("""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' AND name=?;
        """, (table_name,))
        # Получаем результат
        result = cursor.fetchone()
        # Если результат не None, значит таблица существует
        return result is not None
    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return False
    

change = {'Себестоимость':'sebest', 'Мин. маржа, %':'m_mar', 'Расходы внутр.':'timeintime_izd'}
def upload_new_unit(data):
    from function.templates_json import data_
    user = data_()
    conn = sqlite3.connect(f'db/{user["comp_name"]}.db')
    cursor = conn.cursor()
    for art in data:
        try:
            df_data = pd.DataFrame([art])
            df_data.rename(columns={'article': 'nmid', list(art)[1]: change[list(art)[1]]}, inplace=True)
            column_name = list(art)[1]
            new_column_name = change[column_name]
            nmid = art['article']
            value = art[column_name]
            
            if new_column_name == 'timeintime_izd':
                value = int(value) / 100
            elif new_column_name == 'm_mar':
                df = pd.read_sql_query("SELECT sebest FROM sebes WHERE nmid = ?", conn, params=(nmid,))
                if df.empty:
                    raise ValueError(f"No record found for nmid = {nmid}")
                value = int(value) / df['sebest'].iloc[0]
            else:
                value = int(value)

            cursor.execute(f"UPDATE sebes SET {new_column_name} = ? WHERE nmid = ?", (value, nmid))
            conn.commit()
        except Exception as e:
            print(f"Ошибка при добавлении данных: {e}")
            continue
    conn.close()
    return 'Все ок'

    


 