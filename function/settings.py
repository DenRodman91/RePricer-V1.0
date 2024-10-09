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



def setting(*kwargs):
    from function.templates_json import data_
    data = data_()
    comp = data['comp_name']
    conn = sqlite3.connect(f'db/{comp}.db')
    if not check_table_exists(conn, 'sebes'):
        return render_template('auth/settings.html', error = 'Не добавлена таблица себестоимости! Добавьте ее на вкладке Кабинеты')
    from appp.pandi import calk_set
    df_merged = calk_set(conn)
  
    return render_template('auth/settings.html', df=df_merged, pd = pd)



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