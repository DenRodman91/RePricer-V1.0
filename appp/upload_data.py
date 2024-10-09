import sys
import os
import pandas as pd
import time


def upload(db, cab, what, n, stat_if = ['orders', 'sales', 'last', 'unorder'], moon = False):
    send_not = 'Не удалось загрузить: '
    v = 'bad_notification'
    import sqlalchemy
    from datetime import datetime as dt
    from db_req import Database as Db
    from wb_req import WBrequest as Wb
    engine = sqlalchemy.create_engine(f'sqlite:///db/{db}.db')
    db = Db(db)
    dn = dt.now().strftime('%Y-%m-%d')
    dnh = dt.now().strftime('%Y-%m-%d %H:%M:%S')
    t = db.select('cabinet', ['tokenKontent', 'tokenStat', 'tokenPrice', 'tokenAnal'], 'cabinet = ?', [cab])
    t_k = t[0][0]
    t_s = t[0][1]
    t_p = t[0][2]
    t_a = t[0][3]
    for i in what:
        if i == 'art':
            df = Wb(t_k).wb_articuls()
            if list(df)[0] == 'data':
                df['data']['date_add'] = dn
                df['data']['cabinet'] = cab
                df['data'].rename(columns=lambda x: x.lower(), inplace=True)
                df['data'].to_sql('product', engine, if_exists='append', index=False)
            else:
                send_not += 'артикулы'
        if i == 'anal':
            if n:
                d1 = pd.read_sql("select max(date) as 'D1' from hranenie", engine)
                df = Wb(token=t_a, d1 = d1).wb_anal()
            df = Wb(t_a).wb_anal()
            if list(df)[0] == 'data':
                df['data']['date_add'] = dnh
                df['data']['cabinet'] = cab
                df['data'].rename(columns=lambda x: x.lower(), inplace=True)
                
                df['data'].to_sql('hranenie', engine, if_exists='append', index=False)
            else:
                send_not += 'хранение'                                      
        if i == 'price':
            df = Wb(t_p).wb_price()
            if list(df)[0] == 'data':
                df['data']['date_add'] = dnh
                df['data']['cabinet'] = cab
                df['data'].rename(columns=lambda x: x.lower(), inplace=True)
                df['data'].to_sql('price', engine, if_exists='append', index=False)
            else:
                send_not += 'цены'
                                                
        if i == 'stat':
            if moon:
                w.append('detaliz')
            for w in stat_if:
                if n:
                    d1 = pd.read_sql(f"select date(max(date_add)) as 'D1' from {w}", engine)
                    d1 = d1['D1'].values[0]
                    df = Wb(token=t_s, param=w, d1 = d1).wb_statistica()
                df = Wb(token=t_s, param=w).wb_statistica()
                if list(df)[0] == 'data':
                    df['data']['date_add'] = dnh
                    df['data']['cabinet'] = cab
                    df['data'].rename(columns=lambda x: x.lower(), inplace=True)
                    from sqlalchemy.sql import text
                    query = text(f'DELETE FROM `{w}` WHERE date(date_add) = current_date')
                    with engine.connect() as connection:
                        connection.execute(query)
                        connection.commit()
                    df['data'].to_sql(w, engine, if_exists='append', index=False)
                    if len(stat_if) != 1 or stat_if[-1] != w:
                        time.sleep(20)
                else:
                    send_not += w      
    print('Готово, ', send_not)                       








