import eventlet
eventlet.monkey_patch()

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from flask import Flask, render_template, request, jsonify, make_response, send_file, redirect, url_for, flash
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
import random
import telebot
from function.login import login as log
from function.login import User
from function.singin import signin as sin
from function.mydata import handle_mydata, check_tok, download_excel, download_excel2
from function.myarticul import myarticul as myart
from function.settings import setting as sett
from function.payment import payment_first as pf

from flask_socketio import SocketIO, emit

bot = telebot.TeleBot("6549083633:AAFJyBrN9wnCAl03aWSW8jsrm3iQ1316Csw")
application = Flask(__name__)
application.config.from_object('config.Config')
socketio = SocketIO(application, async_mode='eventlet', message_queue='redis://localhost:6379/0')

bcrypt = Bcrypt(application)
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, user_id, email, comp, payment, tarif, do):
        self.id = user_id
        self.username = email
        self.comp = comp
        self.payment = payment
        self.tarif = tarif
        self.do = do

application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=48)
clients = {}
@socketio.on('connect')
def handle_connect():
    clients[request.sid] = request.sid
    session['sid'] = request.sid
    print('Client connected')
    print(f'Transport used: {request.environ.get("HTTP_CONNECTION")}')

@socketio.on('disconnect')
def handle_disconnect():
    clients.pop(request.sid, None)
    session.pop('sid', None)
    print('Client disconnected')

@socketio.on('send_message')
def handle_send_message(json):
    from function.unit import upload_new_unit as uu
    message = uu(json)
    emit('notification', {'message': message}, broadcast=True)
 

@login_manager.user_loader
def load_user(email):
    conn = sqlite3.connect('db/users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    conn = sqlite3.connect(f'db/{user[1]}.db')
    df = pd.read_sql_query(f"SELECT * FROM data", conn)
    if user:
        return User(user_id=user[4], email=user[2], comp=user[1], 
                    payment=df['payment'].values[0], tarif=df['tarif'].values[0], do=df['pay_do'].values[0])
    return None

@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@application.route('/login', methods=['GET', 'POST'])
def login():
    return log(bcrypt, request, flash)

@application.route('/request-password', methods=['POST'])
def request_password():
    data = request.get_json()
    email = data.get('email')
    with sqlite3.connect('db/users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT telegram FROM users WHERE email = ?', (email,))
        tg = cursor.fetchone()[0]
    
    if not email:
        return jsonify(message="Email не указан."), 400
    
    new_code = str(random.randint(100000, 999999))
    
    try:
        with sqlite3.connect('db/users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET code = ? WHERE email = ?', (new_code, email))
            if cursor.rowcount == 0:
                return jsonify(message="Email не найден."), 404
            conn.commit()
            bot.send_message(chat_id=tg, text=f"НИКОМУ НЕ СООБЩАЙТЕ КОД! \nВаш код: {new_code}")
    except sqlite3.Error as e:
        return jsonify(message=f"Ошибка базы данных: {e}"), 500

    return jsonify(message="Пароль успешно отправлен на указанный email.")

@application.route('/singin', methods=['GET', 'POST'])
def singin():
    what = sin(request)
    return what

@application.route("/", methods=['GET', 'POST'])
def index():
    return render_template('unauth/index.html')

@application.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('unauth/about.html')

@application.route("/tarif", methods=['GET', 'POST'])
def tarif():
    return render_template('unauth/tarif.html')

@application.route("/whatwecan", methods=['GET', 'POST'])
def whatwecan():
    return render_template('unauth/superpower.html')

@application.route("/personal", methods=['GET', 'POST'])
@login_required
def personal():
    from function.personal import personal as pers
    return pers()

@application.route("/learn", methods=['GET', 'POST'])
@login_required
def learn():
    return render_template('auth/learn.html')

@application.route("/news", methods=['GET', 'POST'])
@login_required
def news():
    return render_template('auth/news.html')

@application.route("/myarticul", methods=['GET', 'POST'])
@login_required
def myarticul():
    return myart()

@application.route("/unit", methods=['GET', 'POST'])
@login_required
def unit():
    from function.unit import unit as unitka
    return unitka(request)

@application.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    return sett(request)

@application.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('auth/dashboard.html')

@application.route('/upload_excel', methods=['POST'])
@login_required
def upload_excel():
    output, error_response, error_status = download_excel(request)
    if error_response is not None:
        return error_response, error_status
    return send_file(
        output,
        download_name='download.xlsx',
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@application.route('/upload_excel2', methods=['POST'])
@login_required
def upload_excel2():
    return download_excel2(request)

@application.route("/mydata", methods=['GET', 'POST'])
@application.route("/mydata/<string:str_param>", methods=['GET', 'POST'])
@login_required
def mydata_route(str_param=None):
    return handle_mydata(request, str_param)

@application.route('/validate', methods=['POST'])
@login_required
def validate():
    data = request.json
    print(data)
    if not check_tok(data['k'], data['p'], data['s'], data['q']):
        return jsonify({'success': False, 'message': 'Invalid tokens provided.'}), 400
    return jsonify({'success': True})

@application.route("/payment", methods=['GET', 'POST'])
@login_required
def payment():
    if request.method == 'POST':
        sum_value = request.args.get('sum')
        tarif = request.args.get('tarif')
        if sum_value:
            pf(request, sum_value, tarif)
            print(f"Received payment sum: {sum_value}")
            return jsonify({"status": "success", "message": f"Payment received with sum: {sum_value}"})
    return render_template('auth/payment.html')

@application.route("/history", methods=['GET', 'POST'])
@login_required
def history():
    return render_template('auth/history.html')

@application.route('/addparam', methods=['POST'])
def handle_data():
    print('-'*100)
    print(request)
    if request.is_json:
        print('-'*100)
        data = request.get_json()
        print("Received data:", data)
        con = sqlite3.connect(f'db/{current_user.comp}.db')
        cursor = con.cursor()
        for art in data['articuls']:
            cursor.execute("INSERT INTO setttings (nmid, strat, param) VALUES (?, ?, ?)", (art, data['strat'], data['metrics'][1]['value']))
            con.commit()
        return jsonify({"status": "success", "message": "Data processed successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

@application.route("/secret", methods=['GET', 'POST'])
def secret():
    return render_template('unauth/secret.html')

import subprocess



if __name__ == "__main__":
    import eventlet
    import eventlet.wsgi
    eventlet.monkey_patch()
    socketio.run(application, port=33066, debug=True)