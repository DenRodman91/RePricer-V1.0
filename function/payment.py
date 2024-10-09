import pandas as pd
import datetime as dt
import time
import sqlite3
from flask import request, render_template, jsonify
from flask_login import current_user
import requests
from appp.db_req import Database
import sqlite3
import datetime
def payment_first(request, sum, tarif):
    r = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    comp = current_user.comp
    conn = sqlite3.connect('db/'+comp+'.db')   
    cur = conn.cursor()
    cur.execute(f"UPDATE data SET 'balance' = ?, 'tarif' =?, 'pay_do' = ?, 'payment' = ?", (sum, tarif, r, 1))
    conn.commit()
    conn.close()


