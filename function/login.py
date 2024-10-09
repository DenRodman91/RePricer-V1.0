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
class User(UserMixin):
    def __init__(self, user_id, email, comp):
        self.id = user_id
        self.username = email
        self.comp = comp

def login(bcrypt, request, flash):
    if current_user.is_authenticated:
        return redirect(url_for('personal'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = sqlite3.connect('db/users.db')
        cursor = conn.cursor()

        cursor.execute('SELECT code FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if password == user[0] and password != None:
            cursor.execute('UPDATE users SET code = ? WHERE email = ?', ('NULL', email))
            conn.commit()
            cursor.execute('SELECT company_name FROM users WHERE email = ?', (email,))
            comp = cursor.fetchone()
            conn.close()
            user_obj = User(user_id=email, email=email, comp = comp[0])
            login_user(user_obj)
            return redirect(url_for('personal'))
        else:
            flash("Неверный код", "error")
            today = datetime.now().strftime(format='%Y-%m-%d')
            cursor.execute('UPDATE users SET code = ? WHERE email = ?', (None, email))
            conn.commit()
            cursor.execute('UPDATE users SET last_log = ? WHERE email = ?', (today, email))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))

    return render_template('unauth/login.html')
