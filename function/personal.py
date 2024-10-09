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
import datetime
from flask_bcrypt import Bcrypt
import time
from tasks import add_together
from function.templates_json import data_

def personal(*kwargs):
    data = data_()
    print(data)
    sid = session.get('sid')
    to = datetime.datetime.now().strftime("%Y-%m-%d")
    comp = data['comp_name']
    conn = sqlite3.connect(f'db/{comp}.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT nmID FROM product""")
    art = len(cursor.fetchall())
    df = pd.read_sql("SELECT sum(quantityfull) as coc FROM `last`", conn)
    df2 = pd.read_sql("SELECT COUNT(*) as coc FROM sales WHERE date(date_add) = current_date", conn)
    df3 = pd.read_sql("SELECT COUNT(*) as coc FROM orders WHERE date(date_add) = current_date", conn)
    df30 = pd.read_sql("""SELECT AVG(daily_sales) as coc
                            FROM (
                                SELECT date(date_add) as sale_date, count(*) as daily_sales
                                FROM `orders`
                                WHERE date(date_add) > date('now', '-7 day')
                                GROUP BY date(date_add)
                            ) """, conn)
    df4 = pd.read_sql("SELECT COUNT(*) as coc FROM unorder WHERE date(date_add) = current_date", conn)
    try:
        data['art'] = art
        data['last'] = df['coc'].values[0]
        data['sales'] = df2['coc'].values[0]
        data['orders'] = df3['coc'].values[0]
        data['unorders'] = df4['coc'].values[0]
        data['days']  = df['coc'].values[0]/df30['coc'].values[0]
    except:
        data['art'] = 0
        data['last'] = 0
        data['sales'] = 0
        data['orders'] = 0
        data['unorders'] = 0
        data['days']  = 0
    return render_template('auth/personal.html', data = data, int=int)   
    

