import schedule
import time
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import pandas as pd

# Путь к базе данных
db_path = 'db/every.db'

# Храним запланированные задачи в виде словаря
scheduled_tasks = {}

# Создаем пул потоков
executor = ThreadPoolExecutor(max_workers=10)

def fetch_users():
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, db, param, cabinet FROM every WHERE status = 'active'")
        users = cursor.fetchall()
        print(f"Fetched users: {users}")  # Отладочное сообщение
    except Exception as e:
        print(f"Error fetching users: {e}")
        users = []
    finally:
        conn.close()
    return users

def update_user_db(db_name, cab):
    try:
        from appp.upload_data import upload
        upload(db_name, cab, ['stat'], True, stat_if=['orders', 'sales', 'last', 'unorder'])
        print(f"Updating database '{db_name}' for user '{cab}' at {datetime.now()}")
    except Exception as e:
        print(f"Error updating database '{db_name}' for user '{cab}': {e}")

def update_user_db_moon():
    try:
        users = fetch_users()
        for user in users:
            user_id, db_name, interval, cab = user
            from appp.upload_data import upload
            upload(db_name, cab, ['stat', 'price', 'anal', 'art'], True, stat_if=['orders', 'sales', 'last', 'unorder'], moon=True)
            print(f"Updating database '{db_name}' for user '{cab}' at {datetime.now()}")
    except Exception as e:
        print(f"Error updating database '{db_name}' for user '{cab}': {e}")

def upd_tar():
    try:
        from appp.wb_req import WBrequest
        WBrequest().wb_comis()
        print(f"Updating database 'tarifs' at {datetime.now()}")
    except Exception as e:
        print(f"Error updating database 'tarifs")


def update_user_db_sun():
    try:
        users = fetch_users()
        for user in users:
            user_id, db_name, interval, cab = user
            from appp.upload_data import upload
            upload(db_name, cab, ['price'], True)
            print(f"Updating database '{db_name}' for user '{cab}' at {datetime.now()}")
    except Exception as e:
        print(f"Error updating database '{db_name}' for user '{cab}': {e}")

def clear_schedules():
    global scheduled_tasks
    # Отменяет все запланированные задачи, которые не активны больше
    active_user_ids = [user[0] for user in fetch_users()]
    for user_id in list(scheduled_tasks.keys()):
        if user_id not in active_user_ids:
            schedule.clear(user_id)
            scheduled_tasks.pop(user_id, None)
            print(f"Cleared task for user '{user_id}'")  # Отладочное сообщение

def schedule_updates():
    global scheduled_tasks
    users = fetch_users()
    schedule.every().day.at("23:59").do(update_user_db_moon)
    schedule.every().day.at("12:00").do(update_user_db_sun)
    schedule.every().day.at("23:59").do(update_user_db_moon)
    for user in users:
        user_id, db_name, interval, cab = user
        interval = int(interval)  # Преобразуем строку в целое число

        # Проверяем, запланирована ли уже задача с тем же интервалом
        if user_id in scheduled_tasks and scheduled_tasks[user_id] == interval:
            continue

        # Если интервал изменился, удаляем старую задачу
        if user_id in scheduled_tasks:
            schedule.clear(user_id)

        # Планируем обновления на основе интервалов
        if interval == 1:
            schedule.every(5).minutes.do(executor.submit, update_user_db, db_name, cab).tag(user_id)
        elif interval == 30:
            schedule.every(30).minutes.do(executor.submit, update_user_db, db_name, cab).tag(user_id)
        elif interval == 60:
            print('hello I was here')
            schedule.every(1).hour.do(executor.submit, update_user_db, db_name, cab).tag(user_id)
        elif interval == 120:
            schedule.every(2).hours.do(executor.submit, update_user_db, db_name, cab).tag(user_id)
        elif interval == 240:
            schedule.every(4).hours.do(executor.submit, update_user_db, db_name, cab).tag(user_id)
        elif interval == 720:
            schedule.every(12).hours.do(executor.submit, update_user_db, db_name, cab).tag(user_id)
        elif interval == 1440:
            schedule.every(1).day.do(executor.submit, update_user_db, db_name, cab).tag(user_id)
        elif interval == 2880:
            schedule.every(2).days.do(executor.submit, update_user_db, db_name, cab).tag(user_id)
        else:
            schedule.every(interval).hours.do(executor.submit, update_user_db, db_name, cab).tag(user_id)
        # Сохраняем запланированные задачи
        scheduled_tasks[user_id] = interval

def run_scheduler():
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            print(f"Error running scheduler: {e}")
        time.sleep(1)

def update_scheduler():
    while True:
        try:
            clear_schedules()
            schedule_updates()
        except Exception as e:
            print(f"Error updating scheduler: {e}")
        time.sleep(300)  # Обновляем расписание каждые 5 минут

if __name__ == '__main__':
    # Используем многопоточность для выполнения задач
    with ThreadPoolExecutor(max_workers=2) as executor_main:
        # Запуск планировщика
        executor_main.submit(run_scheduler)
        # Периодическое обновление расписания
        executor_main.submit(update_scheduler)