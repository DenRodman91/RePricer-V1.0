import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import time
import sqlite3
token_statistics = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwMjI2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyNzc0NzAzMiwiaWQiOiI4MjVjZGE3Ni1hZTg4LTRlY2UtOThjMi01Yjg5M2Y0MmMxYTEiLCJpaWQiOjgxNzA1NzQxLCJvaWQiOjU3Mjg2MSwicyI6MzIsInNpZCI6ImNiYmU3NjBjLWQ0N2MtNDVkZC04ZjNiLWE5MjZmYzBlY2ViMSIsInQiOmZhbHNlLCJ1aWQiOjgxNzA1NzQxfQ.7-xstjidF9SKZgCFOAFT7pQETVDt0xuL21GdmkEPHRPbZAPVml1G4PTWMEGDcaQzYT72XNw3WiyT86NJaeJY4A'
token_price = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwMjI2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyNzc0NzAwNywiaWQiOiIwYmQ2MTY5Zi00YzhlLTRlMjEtYmMzOS1iMDg0MmNiMzM0ZjQiLCJpaWQiOjgxNzA1NzQxLCJvaWQiOjU3Mjg2MSwicyI6OCwic2lkIjoiY2JiZTc2MGMtZDQ3Yy00NWRkLThmM2ItYTkyNmZjMGVjZWIxIiwidCI6ZmFsc2UsInVpZCI6ODE3MDU3NDF9.kyzbiTlPdEIKr11JTaFT0eNm9LLJYpRciQxz7Fdq4ltL6CugRGRUnVx5YwrJEPn0qnZso3hCylucn6dpcU4Uow'
token_content = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwMjI2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyNzc0NzA1NiwiaWQiOiJkMTAxMzFlZi1iOWMyLTQ4NmUtOTdkMS00YTMzN2FkZTgwNzAiLCJpaWQiOjgxNzA1NzQxLCJvaWQiOjU3Mjg2MSwicyI6Miwic2lkIjoiY2JiZTc2MGMtZDQ3Yy00NWRkLThmM2ItYTkyNmZjMGVjZWIxIiwidCI6ZmFsc2UsInVpZCI6ODE3MDU3NDF9.V8TI9BQAkdSulbdD-xAABqbmWeE_Z1yDZqdf01W4X2q9U1I-JpSLKjjcsBG_PZfBytHWdfEF1WmNRoNh2fhTkw'
token_anal = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwNTA2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTczMzE4MzUzMCwiaWQiOiJmN2M4MWU5OC0wZDMyLTRkY2YtYjBmMy03ZGEzMmQwZDJlYTEiLCJpaWQiOjgxNzA1NzQxLCJvaWQiOjU3Mjg2MSwicyI6NjgsInNpZCI6ImNiYmU3NjBjLWQ0N2MtNDVkZC04ZjNiLWE5MjZmYzBlY2ViMSIsInQiOmZhbHNlLCJ1aWQiOjgxNzA1NzQxfQ.VhMK0l7WvSFV21gx2xH6Ofcel958tcLJJABFTdaf2vfdtJYzJct-jji2HyEUd-N-9KGXGZEiwDFUehIkU-v2tQ'
class WBrequest():
    def __init__(self, token, d1 = None, d2 = None, param = None, art = None, day = 1):
        self.param = param
        self.token = token
        self.art = art
        self.day  = day
        if not d1:
            if param == 'detaliz':
                self.d1 = (datetime.today() - timedelta(days=60)).strftime('%Y-%m-%d')
            else:
                self.d1 = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        else:
             self.d1 = d1
        if not d2:
            self.d2 = datetime.today().strftime('%Y-%m-%d')
        else:
            self.d2 = d2

    def wb_articuls(self):
        """Получение карточек товара по АПИ всех доступных на данный момент, 
        используется итеративный способ запросов в несколько подходов с лимитом 100"""
        api_url = "https://suppliers-api.wildberries.ru/content/v2/get/cards/list"  # Замените на реальный URL API
        headers = {
            'Authorization': self.token, 
            'Content-Type': 'application/json'
        }
        data_template = {
            "settings": {
                "cursor": {
                    "limit": 100
                },
                "filter": {
                    "withPhoto": -1
                }
            }
    }
        # transformed_data = transform_json(json_data, keys_to_remove, keys_to_expand)

# print(json.dumps(transformed_data, indent=4, ensure_ascii=False))
        list1 = []
        # try:
        response = requests.post(api_url, headers=headers, json=data_template)
        if response.status_code == 200:
            data = response.json()['cards']
            
            list1.extend(self.transform_json(i, ['tags', 'characteristics'], {'photos': {'keys': ['big'], 'num': 1}}) for i in data)
            total = response.json()['cursor']['total']
            while total == 100:
                json1 = {
                        "settings": {
                            "cursor": {
                                "updatedAt": response.json()['cursor']['updatedAt'],
                                "nmID": response.json()['cursor']['nmID'],
                                "limit": 100
                            },
                            "filter": {
                                "withPhoto": -1
                            }
                        }
                    }
                response = requests.post(api_url, headers=headers, json=json1)
                data = response.json()['cards']
                list1.extend(self.transform_json(i, ['tags', 'characteristics'], {'photos': {'keys': ['big'], 'num': 1}}) for i in data)       
                total = response.json()['cursor']['total']
        
        else:
            return {'error': 'Ошибка при запросе данных'}

        return {'data':pd.DataFrame(list1)}                       
        # except:
        #     return {'error': 'Error request'}

    def jsonchick(self, data):
        result = []
        for item in data:
            flattened_data = {}
            for key, value in item.items():
                if isinstance(value, list) and key == 'sizes' and len(value) > 0:
                    for inner_item in value:
                        for inner_key, inner_value in inner_item.items():
                            flattened_data[inner_key] = inner_value
                else:
                    flattened_data[key] = value
            result.append(flattened_data)
        return result

    def wb_price(self):
        url = f'https://discounts-prices-api.wb.ru/api/v2/list/goods/filter?limit=500'
        headers = {
            'accept': 'application/json',
            'Authorization': self.token
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Проверка на HTTP ошибки
            data = response.json()
            itog = self.jsonchick(data.get('data', {}).get('listGoods', []))
            while len(data.get('data', {}).get('listGoods', [])) > 499:
                offset = len(itog)
                url2 = f'https://discounts-prices-api.wb.ru/api/v2/list/goods/filter?limit=500&offset={offset}'
                response2 = requests.get(url2, headers=headers)
                response2.raise_for_status()  # Проверка на HTTP ошибки
                data = response2.json()
                new_goods = data.get('data', {}).get('listGoods', [])
                itog.extend(self.jsonchick(new_goods))
            return {'data':pd.DataFrame(itog).drop_duplicates()}
        except requests.RequestException as e:

            return {'error':'Ошибка HTTP' + str(e)}
        
    def wb_anal(self, w = None):
        url = f'https://seller-analytics-api.wildberries.ru/api/v1/paid_storage'
        headers = {
            'accept': 'application/json',
            'Authorization': self.token
        }
        try:
            ch_res = True
            while ch_res:
                response = requests.get(url, headers=headers, params={'dateFrom':self.d1,'dateTo':self.d2 })
                data = response.json()
                try:
                    print(data)
                    id = data['data']['taskId']
                    break
                except Exception as e:
                    print('fuckin error ', str(e))
                    time.sleep(60)
            if w == 'ch':   
                if 'data' in list(data):
                    return True
                else:
                    return False
            ch = True
            while ch:
                time.sleep(20)
                url_1 = f'https://seller-analytics-api.wildberries.ru/api/v1/paid_storage/tasks/{id}/download'
                response = requests.get(url_1, headers=headers, params={'taskId':id})
                if response.status_code  ==  200:
                    data = response.json()
                    data = pd.DataFrame(data)
                    ch = False
                    return {'data': data}
        except requests.RequestException as e:
            return {'error':'Ошибка HTTP' + str(e)}
        
    def wb_statistica(self):
        what = self.param
        url_order = f'https://statistics-api.wildberries.ru/api/v1/supplier/orders?flag={self.day}'
        url_sale = f'https://statistics-api.wildberries.ru/api/v1/supplier/sales?flag={self.day}'
        url_last = 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks?dateFrom=2019-07-01'
        url_detaliz = 'https://statistics-api.wildberries.ru/api/v5/supplier/reportDetailByPeriod'
        headers = {'Authorization': self.token, 
                'Content-Type': 'application/json'}
        if what == None:
            print('Не указан параметр или указан неверный')
            return {'error': 'Не указан параметр или указан неверный'}
        elif 'orders' in what:
            respose = requests.get(url_order, headers=headers, params={'dateFrom':self.d1})
            print(respose)
            if respose.status_code != 200:
                return {'error': 'Ошибка при запросе данных'}
            data = pd.DataFrame(respose.json())
            print(data)
            return {'data': data}
        elif 'sales' in what:
            respose = requests.get(url_sale, headers=headers, params={'dateFrom':self.d1})
            if respose.status_code != 200:
                return {'error': 'Ошибка при запросе данных'}
            data = pd.DataFrame(respose.json())
            return {'data': data}
        elif 'last' in what:
            respose = requests.get(url_last, headers=headers)
            if respose.status_code != 200:
                mes = f'Ошибка при запросе данных: {respose.status_code, respose.text}'
                print(mes)
                return {'error': mes}
            data = pd.DataFrame(respose.json())
            return {'data': data}
        elif 'unorder' in what:
            respose = requests.get(url_order, headers=headers, params={'dateFrom':self.d1})
            if respose.status_code != 200:
                return {'error': 'Ошибка при запросе данных'}
            data = pd.DataFrame(respose.json())
            data = data[data['orderType'] != 'Клиентский']
            return {'data': data}
        elif 'detaliz' in what:
            respose = requests.get(url_detaliz, headers=headers, params={ 'dateFrom':'2024-04-01','dateTo':'2024-09-02'} )
            if respose.status_code != 200:
                return {'error': 'Ошибка при запросе данных'}
            data = pd.DataFrame(respose.json())
            return {'data': data}
        return {'error':'Произошла непредвиденная ошибка скрипта!'}    

    def flatten_json(self,y):
        out = {}

        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(y)
        return out

    def transform_json(self,data, keys_to_remove, keys_to_expand):
        import json
        # Удаляем указанные ключи
        for key in keys_to_remove:
            if key in data:
                del data[key]

        # Раскрываем указанные ключи и оставляем только нужные под-ключи
        for key, sub_keys in keys_to_expand.items():
            if key in data:
                if isinstance(data[key], list) and sub_keys.get('num', -1) > 0:
                    expanded_items = []
                    for item in data[key][:sub_keys['num']]:
                        expanded_item = {sub_key: item[sub_key] for sub_key in sub_keys['keys'] if sub_key in item}
                        expanded_items.append(expanded_item)
                    data[key] = expanded_items
                elif isinstance(data[key], dict):
                    expanded_item = {sub_key: data[key][sub_key] for sub_key in sub_keys['keys'] if sub_key in data[key]}
                    data[key] = expanded_item

        # Проверка на ключ 'video' и обновление его значения
        if 'video' in data:
            data['video'] = True
        else:
            data['video'] = False

        # Делаем JSON одноуровневым
        flat_data = self.flatten_json(data)
        return flat_data

    def wb_comis(self):
        t = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwMjI2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyNzc0NzA1NiwiaWQiOiJkMTAxMzFlZi1iOWMyLTQ4NmUtOTdkMS00YTMzN2FkZTgwNzAiLCJpaWQiOjgxNzA1NzQxLCJvaWQiOjU3Mjg2MSwicyI6Miwic2lkIjoiY2JiZTc2MGMtZDQ3Yy00NWRkLThmM2ItYTkyNmZjMGVjZWIxIiwidCI6ZmFsc2UsInVpZCI6ODE3MDU3NDF9.V8TI9BQAkdSulbdD-xAABqbmWeE_Z1yDZqdf01W4X2q9U1I-JpSLKjjcsBG_PZfBytHWdfEF1WmNRoNh2fhTkw'
        d = {'comm':'https://common-api.wildberries.ru/api/v1/tariffs/commission', 
             'box':'https://common-api.wildberries.ru/api/v1/tariffs/box', 
             'palet':'https://common-api.wildberries.ru/api/v1/tariffs/pallet',
             'ret':'https://common-api.wildberries.ru/api/v1/tariffs/return'}
        headers = {'Authorization': t, 
                'Content-Type': 'application/json'}
        respose = requests.get(d['comm'], headers=headers)
        data_com = pd.DataFrame(respose.json()['report'])
        data_com.to_excel('commision.xlsx')
        data_com.replace(',', '.').to_sql('commisions', sqlite3.connect('db/commis.db') , if_exists='replace', index=False)
        time.sleep(10)
        #___
        respose = requests.get(d['box'], headers=headers, params={'date':self.d1})
        data_box = pd.DataFrame(respose.json()['response']['data']['warehouseList'])
        for column in data_box.select_dtypes(include=[object]):
            data_box[column] = data_box[column].str.replace(',', '.')
        data_box.to_excel('box.xlsx')
        data_box.to_sql('box', sqlite3.connect('db/commis.db') , if_exists='replace', index=False)
        time.sleep(10)
        #___
        respose = requests.get(d['palet'], headers=headers, params={'date':self.d1})
        data_palet = pd.DataFrame(respose.json()['response']['data']['warehouseList'])
        for column in data_palet.select_dtypes(include=[object]):
            data_palet[column] = data_palet[column].str.replace(',', '.')
        data_palet.to_sql('palet', sqlite3.connect('db/commis.db') , if_exists='replace', index=False)

    def ch_price(self, art, new_discont):
        body = {
          "data": [
            {
              "nmID": art,
              "discount": new_discont  
            }
          ]
        }
        headers = {
            'accept': 'application/json',
            'Authorization': self.token
        }
        response = requests.post('https://discounts-prices-api.wildberries.ru/api/v2/upload/task',headers=headers, json=body ) 



headers = {'Authorization': token_statistics, 
    'Content-Type': 'application/json'}
url_sale = f'https://statistics-api.wildberries.ru/api/v1/supplier/sales?flag=0'

respose = requests.get(url_sale, headers=headers, params={'dateFrom':'2024-08-01'})
df = pd.DataFrame(respose.json())
print(df[
    (df['lastChangeDate'] < '2024-09-01') &
    (df['orderType'] == 'Клиентский')
    ])
print(df[df['lastChangeDate'] < '2024-09-01']['orderType'].unique())


