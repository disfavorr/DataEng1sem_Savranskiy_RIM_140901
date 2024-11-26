import json
import msgpack
import os

input_file = "third_task.json" 
output_file_json = "aggregated_data.json"
output_file_msgpack = "aggregated_data.msgpack"


with open(input_file, "r", encoding="utf-8") as file:
    products = json.load(file)

# Агрегация данных по каждому товару
aggregated_data = {}

for product in products:
    product_name = product['name'] 
    price = product['price'] 

    if product_name not in aggregated_data:
        aggregated_data[product_name] = {
            'prices': []
        }

    aggregated_data[product_name]['prices'].append(price)

for product_name, data in aggregated_data.items():
    prices = data['prices']

    average_price = sum(prices) / len(prices)
    max_price = max(prices)
    min_price = min(prices)

    aggregated_data[product_name] = {
        'average_price': average_price,
        'max_price': max_price,
        'min_price': min_price,
    }

# Сохранение в JSON
with open(output_file_json, "w", encoding="utf-8") as file:
    json.dump(aggregated_data, file, ensure_ascii=False, indent=4)

# Сохранение в MsgPack
with open(output_file_msgpack, "wb") as file:
    msgpack.pack(aggregated_data, file)

# Сравнение 
json_size = os.path.getsize(output_file_json)
msgpack_size = os.path.getsize(output_file_msgpack)

print(f"Размер JSON файла: {json_size} байт")
print(f"Размер MsgPack файла: {msgpack_size} байт")
