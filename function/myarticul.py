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



def myarticul(*kwargs):
    user = current_user.username
    conn = sqlite3.connect('db/users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT company_name FROM users WHERE email = ?", (user, ))
    comp = cursor.fetchone()[0]
    conn = sqlite3.connect(f'db/{comp}.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM products""")
    art = cursor.fetchall()
    return render_template('auth/myarticul.html', art = art)