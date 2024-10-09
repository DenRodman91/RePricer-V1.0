import sys
import os
import pandas as pd
# Добавьте путь к приложению
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from celery import Celery
import time
from app import socketio, application  # Импортируйте socketio и app из основного приложения

celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
@celery.task
def add_together(a, b, sid = ''):
    print('hello world')
    time.sleep(1)  # Симуляция длительной задачи
    result = a + b
    with application.app_context():  # Использование контекста приложения
        socketio.emit('notification', {'message': f'Привет! Как дела? Результат: {result}'})  # Отправка уведомления только клиенту с идентификатором sid
    return result


@celery.task
def upload(db, cab, what, n = False, day = 0):
    send_not = 'Не удалось загрузить: '
    v = 'bad_notification'
    import sqlalchemy
    from datetime import datetime as dt
    from appp.db_req import Database as Db
    from appp.wb_req import WBrequest as Wb
    import eventlet
    eventlet.monkey_patch() 
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
                d1 = d1['D1']
                df = Wb(t_a, d1=d1).wb_anal()
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
            for w in ['orders', 'sales', 'last', 'unorder', 'detaliz']:
                if n:
                    d1 = pd.read_sql(f"select max(date_add) as 'D1' from {w}", engine)
                    print(d1, n)
                    d1 = d1['D1']
                    df = Wb(t_s, w, d1=d1).wb_statistica()
                df = Wb(token=t_s, param=w, day = day).wb_statistica()
                if list(df)[0] == 'data':
                    if day == 1:
                        df['data']['date_add'] = dnh
                    else:
                        # Преобразование колонки 'lastt' в datetime формат для нового столбца
                        df['data']['lastt_datetime'] = pd.to_datetime(df['data']['lastChangeDate'])

                        # Создание нового столбца с другим форматом времени
                        df['data']['date_add'] = df['data']['lastt_datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

                        # Удаление временного столбца 'lastt_datetime'
                        df['data'] = df['data'].drop(columns=['lastt_datetime'])
                    df['data']['cabinet'] = cab
                    df['data'].rename(columns=lambda x: x.lower(), inplace=True)
                    df['data'].to_sql(w, engine, if_exists='append', index=False)
                    time.sleep(50)
                else:
                    send_not += w       
    if send_not == 'Не удалось загрузить: ':
        v = 'notification'
        send_not = 'Успешно загружены все базы данных'
    with application.app_context():  # Использование контекста приложения
        socketio.emit(v, {'message': send_not}, namespace='/',  room=sid)  # Указание пространства имен








