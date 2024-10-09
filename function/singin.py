from flask import Flask, render_template,  request, jsonify, make_response, send_file, redirect, url_for
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
from werkzeug.datastructures import ImmutableMultiDict
import sqlite3



def signin(request):
    if request.method == 'POST':
        # Получение данных из формы
        data = request.form.to_dict(flat=True)
        company_name = data['namecomp']

        # Создание пользователей в users.db
        with sqlite3.connect('db/users.db') as conn:
            cursor = conn.cursor()
            for i in range(1, 11):
                # Составление ключей для доступа к данным
                email_key = f'email{i}'
                telegram_key = f'telegram{i}'
                role_key = f'role{i}'

                # Добавление пользователя, если присутствуют все необходимые данные
                if email_key in data and telegram_key in data and role_key in data:
                    cursor.execute('INSERT INTO users (company_name, email, telegram, role) VALUES (?, ?, ?, ?)', 
                                   (company_name, data[email_key], data[telegram_key], data[role_key]))
            conn.commit()
        # Создание таблиц в базе данных компании

        with sqlite3.connect(f'db/{company_name}.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cabinet (
                    cabinet TEXT,
                    ip TEXT NOT NULL,
                    mp TEXT NOT NULL,
                    tokenKontent TEXT,
                    tokenStat TEXT,
                    tokenPrice TEXT,
                    tokenAnal TEXT,
                    dste_add DATE
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS setttings (
                    nmid INTEGER,
                    strat TEXT,
                    param TEXT 
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    cabinet TEXT,
                    who TEXT,
                    wheen DATA,
                    what TEXT
                );
            """)
            cursor.execute('''
                    CREATE TABLE "product" (
                                    id INTEGER PRIMARY KEY,
                                    cabinet TEXT,
                                    nmid INTEGER,
                                    imtid TEXT,
                                    nmuuid TEXT,
                                    dimensions_isvalid INTEGER,
                                    subjectid INTEGER,
                                    subjectname TEXT,
                                    vendorcode TEXT,
                                    brand TEXT,
                                    title TEXT,
                                    description TEXT,  
                                    dimensions_length INTEGER,   
                                    dimensions_width INTEGER, 
                                    dimensions_height INTEGER, 
                                    sizes_0_chrtid TEXT,
                                    sizes_0_techsize TEXT,
                                    sizes_0_skus_0 TEXT,
                                    "sizes_0_wbsize" TEXT,
                                    photos_0_big TEXT,
                                    photos_0_c246x328 TEXT,
                                    createdat DATE,
                                    updatedat DATE,
                                    video TEXT,
                                    date_add DATE
                                )

                ''')
            cursor.execute('''
CREATE TABLE "price" (
                    id INTEGER PRIMARY KEY,
                    cabinet TEXT,
                    nmid INTEGER,
                    vendorcode TEXT,
                    currencyisocode4217 TEXT,
                    discount INTEGER,
                    editablesizeprice BOOLEAN,
                    sizeid INTEGER,
                    price INTEGER,
                    discountedprice INTEGER,
                    techsizename TEXT,
                    date_add DATE
                )
                ''')
            cursor.execute('''
CREATE TABLE "orders" (
                    id INTEGER PRIMARY KEY,
                    cabinet TEXT,
                    date TEXT,
                    lastchangedate TEXT,
                    warehousename TEXT,
                    countryname TEXT,
                    oblastokrugname TEXT,
                    regionname TEXT,
                    supplierarticle TEXT,
                    nmid INTEGER,
                    barcode TEXT,
                    category TEXT,
                    subject TEXT,
                    brand TEXT,
                    techsize TEXT,
                    incomeid INTEGER,
                    issupply BOOLEAN,
                    isrealization BOOLEAN,
                    totalprice REAL,
                    discountpercent REAL,
                    spp REAL,
                    finishedprice REAL,
                    priceWithdisc REAL,
                    iscancel BOOLEAN,
                    canceldate TEXT,
                    ordertype TEXT,
                    sticker TEXT,
                    gnumber TEXT,
                    srid TEXT,
                    date_add DATE
                )
                ''')
            cursor.execute('''
            CREATE TABLE "sales" (
                    id INTEGER PRIMARY KEY,
                    cabinet TEXT,
                    date TEXT,
                    lastchangedate TEXT,
                    warehousename TEXT,
                    countryname TEXT,
                    oblastokrugname TEXT,
                    regionname TEXT,
                    supplierarticle TEXT,
                    nmid INTEGER,
                    barcode TEXT,
                    category TEXT,
                    subject TEXT,
                    brand TEXT,
                    techsize TEXT,
                    incomeid INTEGER,
                    issupply BOOLEAN,
                    isrealization BOOLEAN,
                    totalprice REAL,
                    discountpercent REAL,
                    spp REAL,
                    paymentsaleamount REAL,
                    forpay REAL,
                    finishedprice REAL,
                    pricewithdisc REAL,
                    saleid TEXT,
                    ordertype TEXT,
                    sticker TEXT,
                    gnumber TEXT,
                    srid TEXT,
                    date_add DATE
                )
                ''')
            cursor.execute('''
CREATE TABLE "last" (
                    id INTEGER PRIMARY KEY,
                    cabinet TEXT,
                    lastchangedate TEXT,
                    warehousename TEXT,
                    supplierarticle TEXT,
                    nmid INTEGER,
                    barcode TEXT,
                    quantity INTEGER,
                    inwaytoclient INTEGER,
                    inwayfromclient INTEGER,
                    quantityfull INTEGER,
                    category TEXT,
                    subject TEXT,
                    brand TEXT,
                    techsize TEXT,
                    price REAL,
                    discount INTEGER,
                    issupply BOOLEAN,
                    isrealization BOOLEAN,
                    sccode TEXT,
                    date_add DATE
                )
                ''')
            cursor.execute('''
CREATE TABLE "unorder" (
                    id INTEGER PRIMARY KEY,
                    cabinet TEXT,
                    date TEXT,
                    lastchangedate TEXT,
                    warehousename TEXT,
                    countryname TEXT,
                    oblastokrugname TEXT,
                    regionname TEXT,
                    supplierarticle TEXT,
                    nmid INTEGER,
                    barcode TEXT,
                    category TEXT,
                    subject TEXT,
                    brand TEXT,
                    techsize TEXT,
                    incomeid INTEGER,
                    issupply BOOLEAN,
                    isrealization BOOLEAN,
                    totalprice REAL,
                    discountpercent REAL,
                    spp REAL,
                    finishedprice REAL,
                    pricewithdisc REAL,
                    iscancel BOOLEAN,
                    canceldate TEXT,
                    ordertype TEXT,
                    sticker TEXT,
                    gnumber TEXT,
                    srid TEXT,
                    date_add DATE
                )
                ''')
            cursor.execute("""
                CREATE TABLE 'data' (
                    'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    'payment' TEXT,
                    'pay_do' DATA,
                    'balance' REAL,
                    'tarif' TEXT
                );
            """)
            cursor.execute("""INSERT INTO 'data' ('payment', 'pay_do', 'balance', 'tarif') VALUES (?,?,?,?)""", (False, None, 0, 'free'))
            conn.commit()

        return redirect(url_for('login'))
    else:
        return render_template('unauth/singin.html')
    


