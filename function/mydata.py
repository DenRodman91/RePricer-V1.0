import re
import sqlite3
import pandas as pd
from flask import request, render_template, jsonify
from flask_login import current_user
import requests, datetime
from appp.wb_req import WBrequest
import time

import io

def check_tok(content_token, price_token, stats_token, anal_token):
    price = WBrequest(token=price_token ).wb_price()
    stat = WBrequest(token=stats_token, param='last').wb_statistica()
    cont = WBrequest(token=content_token).wb_articuls()
    anal = WBrequest(token=anal_token).wb_anal('ch')
    if list(stat)[0] == 'error':
        print('st')
        return False
    if list(price)[0] == 'error':
        print('pr')
        return False
    if list(cont)[0] == 'error':
        print('cont')
        return False
    if not anal:
        print('anal')
        return False
    return True

def handle_mydata(request, str_param):
    from function.templates_json import data_
    from tasks import upload
    data = data_()
    comp = data['comp_name']

    if str_param is not None:#обновление данных токена или кабинета
        param = str_param.split('-')
        conn = sqlite3.connect(f'db/{comp}.db')
        df_cabinet = pd.read_sql(f'SELECT * FROM cabinet WHERE ip = ? AND cabinet = ?', conn, params=(param[0], param[1]))
        dict_cabinet = df_cabinet.to_dict('records')
        return render_template('auth/mydatacab.html', cabinets=dict_cabinet)

    if request.method == 'POST': #добавление нового кабинета
        data = request.json
        conn = sqlite3.connect(f'db/{comp}.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO cabinet (cabinet, ip, mp, tokenKontent, tokenStat,tokenPrice, tokenAnal) VALUES (?, ?, ?,?,?,?, ?)', (data['m'][0]+data['i'][:2], data['i'], data['m'] ,data['k'] ,data['s'] ,data['p'],data['q'] ))
        conn.commit()
        conn.close()
        conn = sqlite3.connect(f'db/every.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO every (cabinet, db, param, status) VALUES (?, ?, ?, ?)', (data['m'][0]+data['i'][:2], comp, data['u_d'], 'active'  ))
        conn.commit()
        cursor.execute('INSERT INTO every_price ( db, param, status) VALUES ( ?, ?, ?)', ( comp, data['u_p'], 'active'  ))
        conn.commit()
        conn.close()
        upload.delay(comp, data['m'][0]+data['i'][:2], ['art', 'price',  'stat'], day = 0)
        return jsonify({'success': True})

    conn = sqlite3.connect(f'db/{comp}.db')
    df_cabinet = pd.read_sql('SELECT ip, cabinet FROM cabinet', conn)
    dict_cabinet = df_cabinet.to_dict('records')
    return render_template('auth/mydata.html', cabinets=dict_cabinet)




def download_excel(request):
    data = request.get_json()
    ip = data.get('ip')
    if not ip:
        return None, jsonify({"error": "IP is required"}), 400
    # Подключение к базе данных и выборка данных
    con = sqlite3.connect(f'db/{current_user.comp}.db')
    query = f'SELECT * FROM product WHERE cabinet = ?'
    df = pd.read_sql(query, con, params=(ip,))
    df = df[['nmid','vendorcode','cabinet','title']]
    df['Себестоимость'] = ""
    df['Мин. маржа, %'] = ""
    df['Расходы внутренние, %'] = ""
    con.close()

    # Создание Excel файла
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)

    return output, None, None


def validate_excel(file):
    try:
        df = pd.read_excel(file)
        if list(df)== ['nmid', 'vendorcode', 'cabinet', 'title', 'Себестоимость',   'Мин. маржа, %',  'Расходы внутренние, %'  ]:
            return True, None
        else:
            return False, "Столбцы были добавлены не верно"               
    except Exception as e:
        return False, str(e)

def download_excel2(request):
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400

    is_valid, error_message = validate_excel(file)
    if not is_valid:
        print(error_message)
        return jsonify({"success": False, "message": f"Invalid Excel file: {error_message}"}), 400
    # Обработка файла
    file.seek(0)
    df = pd.read_excel(file)
    con = sqlite3.connect(f'db/{current_user.comp}.db')
    df.rename(columns={'Себестоимость': 'sebest', 'Мин. маржа, %': 'm_mar', 'Расходы внутренние, %':'timeintime_izd'}, inplace=True)
    df['date_add'] = datetime.datetime.now().strftime('%Y-%m-%d')
    df.to_sql('sebes', con, if_exists='replace', index=False)
    con.close()
    return jsonify({"success": True, "message": "File processed successfully."})
