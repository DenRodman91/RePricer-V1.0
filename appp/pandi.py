import pandas as pd
import sqlite3
def calk(db, param = None):
    # Соединение с базами данных
    conn_db = db
    conn_comis = sqlite3.connect('db/commis.db')

    # Извлечение данных из таблиц
    df_art = pd.read_sql_query("""SELECT nmid AS 'Артикул МП', 
                                        cabinet AS 'Кабинет',
                                        title AS 'Название', 
                                        photos_0_big FROM product""",  conn_db)
    df_pri = pd.read_sql_query("""SELECT nmid AS 'Артикул МП',
                                         discountedprice AS 'Цена с СПП' FROM price
                                    """,  conn_db)
    df_sebes = pd.read_sql_query("""SELECT nmid AS 'Артикул МП',
                                            sebest AS 'Себестоимость',
                                            m_mar*100 AS 'Мин. маржа, %',
                                            (timeintime_izd) AS 'Расходы внутр.'
                                     FROM sebes""",  conn_db)

    df_last = pd.read_sql_query(f"""SELECT nmid AS 'Артикул МП',
                                        SUM(quantityfull) AS 'Остаток'
                               FROM last
                                WHERE date(date_add) = current_date
                               GROUP BY nmid""",  conn_db)
    if param == 'skald':
        df_skald = pd.read_sql_query(f"""SELECT warehousename,
                                        FROM last
                                        WHERE date(date_add) = current_date""",  conn_db)['warehousename'].tolist()

        
    df_pr = pd.read_sql_query("""
        SELECT nmid AS 'Артикул МП', 
                (dimensions_length*dimensions_width*dimensions_height/1000) AS 'Размер'
        FROM product
    """, conn_db)

    df_comis = pd.read_sql_query("""
        SELECT kgvpMarketplace, kgvpSupplier, kgvpSupplierExpress, paidStorageKgvp
        FROM commisions
        WHERE subjectID = 4144
    """, conn_comis)
    if param =='skald':
        sklad_list = "', '".join(df_skald)
        sklad_list = f"'{sklad_list}'"
        df_co = pd.read_sql_query(f"""
            SELECT AVG(boxDeliveryBase) AS de, AVG(boxDeliveryLiter) AS de_d,
                AVG(boxStorageBase) AS hr, AVG(boxStorageLiter) AS hr_d
            FROM box
            WHERE warehouseName IN ({sklad_list})
        """, conn_comis)
    else:
        df_co = pd.read_sql_query("""
            SELECT AVG(boxDeliveryBase) AS 'de', AVG(boxDeliveryLiter) AS 'de_d',
                AVG(boxStorageBase) AS 'hr', AVG(boxStorageLiter) AS 'hr_d'
            FROM box
        """, conn_comis)


    # Заполнение значений из df_co, если они существуют
    if not df_co.empty:
        de = df_co['de'].iloc[0] if pd.notna(df_co['de'].iloc[0]) else 0
        co = df_comis['paidStorageKgvp'].iloc[0] if pd.notna(df_comis['paidStorageKgvp'].iloc[0]) else 0
        de_d = df_co['de_d'].iloc[0] if pd.notna(df_co['de_d'].iloc[0]) else 0
        hr = df_co['hr'].iloc[0] if pd.notna(df_co['hr'].iloc[0]) else 0
        hr_d = df_co['hr_d'].iloc[0] if pd.notna(df_co['hr_d'].iloc[0]) else 0
        # Рассчеты для каждого продукта
        df_pr['Логистика'] = (de + (df_pr['Размер'] - 1) * de_d).round(1)
        df_pr['Хранение'] = ((hr + (df_pr['Размер'] - 1) * hr_d)*30).round(1)
        df_pr['Комиссия'] = co
        df_pr = df_pr.drop(columns=['Размер'])
        df_pr['Расходы МП'] = df_pr['Логистика'] + df_pr['Хранение']
        df_merged = pd.merge(df_art, df_pr, on='Артикул МП', how='left')
        df_merged = pd.merge(df_merged,df_pri, on='Артикул МП', how='left')
        df_merged = pd.merge(df_merged, df_sebes, on='Артикул МП', how='left')
        df_merged = pd.merge(df_merged, df_last, on='Артикул МП', how='left')
        df_merged['Комисся, руб'] = (df_merged['Комиссия']/100*df_merged['Цена с СПП']).round(1)
        df_merged['Мин. цена'] = ((df_merged['Себестоимость'] + df_merged['Расходы МП'] + df_merged['Себестоимость']*df_merged['Расходы внутр.']/100) * (1 + df_merged['Мин. маржа, %']/100)) / (1 - df_merged['Комиссия']/100)    
        df_merged['Расходы МП'] = (df_merged['Расходы МП']+df_merged['Комисся, руб']).round(1)
        df_merged['Мин. цена'] = df_merged['Мин. цена'].round(1)
        df_merged['Маржа сейчас'] = (((df_merged['Цена с СПП'] - (df_merged['Себестоимость'] + df_merged['Расходы МП'] + df_merged['Себестоимость']*df_merged['Расходы внутр.']/100)) / df_merged['Цена с СПП']) * 100).round(1)    
        df_merged['Расходы внутр.'] = df_merged['Расходы внутр.'].round(1)
        return df_merged
    else:
        print("Ошибка: df_co пустой или содержит некорректные данные")







def calk_set(db):
    # Соединение с базами данных
    conn_db = db
    conn_comis = sqlite3.connect('db/commis.db')

    # Извлечение данных из таблиц
    df_art = pd.read_sql_query("""SELECT nmid AS 'Артикул МП', 
                                        cabinet AS 'Кабинет',
                                        title AS 'Название', 
                                        brand AS 'Бренд',
                                        photos_0_big FROM product""",  conn_db)
    df_pri = pd.read_sql_query("""SELECT nmid AS 'Артикул МП',
                                         discountedprice AS 'Цена с СПП' FROM price
                                    """,  conn_db)
    df_sebes = pd.read_sql_query("""SELECT nmid AS 'Артикул МП',
                                            sebest AS 'Себестоимость',
                                            m_mar*100 AS 'Мин. маржа, %',
                                            (sebest*timeintime_izd) AS 'Расходы внутр.'
                                     FROM sebes""",  conn_db)

    df_last = pd.read_sql_query("""SELECT nmid AS 'Артикул МП',
                                        SUM(quantityfull) AS 'Остаток'
                               FROM last
                                WHERE date(date_add) = current_date
                               GROUP BY nmid""",  conn_db)
    df_pr = pd.read_sql_query("""
        SELECT nmid AS 'Артикул МП', 
                (dimensions_length*dimensions_width*dimensions_height/1000) AS 'Размер'
        FROM product
    """, conn_db)
    df_sett = pd.read_sql_query("""
        SELECT nmid AS 'Артикул МП', 
                strat AS 'Стратегия'
        FROM setttings
    """, conn_db)

    df_comis = pd.read_sql_query("""
        SELECT kgvpMarketplace, kgvpSupplier, kgvpSupplierExpress, paidStorageKgvp
        FROM commisions
        WHERE subjectID = 4144
    """, conn_comis)

    df_co = pd.read_sql_query("""
        SELECT AVG(boxDeliveryBase) AS 'de', AVG(boxDeliveryLiter) AS 'de_d',
            AVG(boxStorageBase) AS 'hr', AVG(boxStorageLiter) AS 'hr_d'
        FROM box
    """, conn_comis)

    # Шаг 1: Получаем данные о продажах за последние 7 дней
    query_sales = """
    SELECT nmid AS 'Артикул МП', date(date_add) AS 'Дата', COUNT(*) AS 'Продажи'
    FROM sales
    WHERE date(date_add) >= date('now', '-7 days') AND date(date_add) != current_date
    GROUP BY nmid, date(date_add)
    """

    df_sales = pd.read_sql_query(query_sales, conn_db)

    # Шаг 2: Преобразование столбца 'Дата' в тип datetime и группировка данных
    df_sales['Дата'] = pd.to_datetime(df_sales['Дата'])
    df_sales = df_sales.groupby(['Артикул МП', 'Дата']).sum().reset_index()

    # Шаг 3: Определение тренда для каждого артикула
    def calculate_trend(df):
        if len(df) < 2:
            return 0
        sales_diff = df['Продажи'].diff().dropna()
        trend = sales_diff.mean()
        return 1 if trend > 0 else 0
    try:
        df_trend = df_sales.groupby('Артикул МП').apply(calculate_trend).reset_index(name='Тренд')
    except:
        df_trend = df_sales[['Артикул МП']]
        df_trend['Тренд'] = 0
    
    df_merged = pd.merge(df_art, df_pri, on='Артикул МП', how='left')


    # Закрытие соединения с базой данных
    conn_db.close()

    # Вывод результата

    if not df_co.empty:
        de = df_co['de'].iloc[0] if pd.notna(df_co['de'].iloc[0]) else 0
        co = df_comis['paidStorageKgvp'].iloc[0] if pd.notna(df_comis['paidStorageKgvp'].iloc[0]) else 0
        de_d = df_co['de_d'].iloc[0] if pd.notna(df_co['de_d'].iloc[0]) else 0
        hr = df_co['hr'].iloc[0] if pd.notna(df_co['hr'].iloc[0]) else 0
        hr_d = df_co['hr_d'].iloc[0] if pd.notna(df_co['hr_d'].iloc[0]) else 0
        # Рассчеты для каждого продукта
        df_pr['Логистика'] = (de + (df_pr['Размер'] - 1) * de_d).round(1)
        df_pr['Хранение'] = ((hr + (df_pr['Размер'] - 1) * hr_d)*30).round(1)
        df_pr['Комиссия'] = co
        df_pr = df_pr.drop(columns=['Размер'])
        df_pr['Расходы МП'] = df_pr['Логистика'] + df_pr['Хранение']
        df_merged = pd.merge(df_art, df_pr, on='Артикул МП', how='left')
        df_merged = pd.merge(df_merged,df_pri, on='Артикул МП', how='left')
        df_merged = pd.merge(df_merged, df_sebes, on='Артикул МП', how='left')
        df_merged = pd.merge(df_merged, df_last, on='Артикул МП', how='left')
        df_merged['Комисся, руб'] = (df_merged['Комиссия']/100*df_merged['Цена с СПП']).round(1)
        df_merged['Мин. цена'] = ((df_merged['Себестоимость'] + df_merged['Расходы МП'] + df_merged['Себестоимость']*df_merged['Расходы внутр.']/100) * (1 + df_merged['Мин. маржа, %']/100)) / (1 - df_merged['Комиссия']/100)    
        df_merged['Расходы МП'] = (df_merged['Расходы МП']+df_merged['Комисся, руб']).round(1)
        df_merged['Мин. цена'] = df_merged['Мин. цена'].round(1)
        df_merged['Маржа сейчас'] = (((df_merged['Цена с СПП'] - (df_merged['Себестоимость'] + df_merged['Расходы МП'] + df_merged['Себестоимость']*df_merged['Расходы внутр.']/100)) / df_merged['Цена с СПП']) * 100).round(1)    
        df_merged['Расходы внутр.'] = df_merged['Расходы внутр.'].round(1)
        df_merged = pd.merge(df_merged, df_sett, on='Артикул МП', how='left')
        df_merged = pd.merge(df_merged, df_trend, on='Артикул МП', how='left')
        return df_merged
    else:
        print("Ошибка: df_co пустой или содержит некорректные данные")





