import pickle
import json


with open('fourth_task_products.json', 'rb') as pkl_file:
    products = pickle.load(pkl_file)

with open('fourth_task_updates.json', 'r', encoding='utf-8') as json_file:
    price_updates = json.load(json_file)

for update in price_updates:
    product_name = update['name']
    method = update['method']
    param = update['param']

    for product in products:
        if product['name'] == product_name:
            if method == 'add':
                product['price'] += param
            elif method == 'sub':
                product['price'] -= param
            elif method == 'percent+':
                product['price'] *= (1 + param)
            elif method == 'percent-':
                product['price'] *= (1 - param)
            break  

with open('fourth_task_updated_products.pkl', 'wb') as pkl_file:
    pickle.dump(products, pkl_file)