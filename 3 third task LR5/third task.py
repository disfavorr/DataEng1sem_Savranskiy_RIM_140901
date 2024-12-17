import msgpack
import pymongo
from bson import json_util
import json


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["task1lr5"] 
collection = db["pkl"] 


with open("task_3_item.msgpack", "rb") as file:
    data = msgpack.unpackb(file.read(), raw=False)

# Вставка данных в коллекцию
collection.insert_many(data)
print("Данные успешно добавлены в коллекцию.")

# Удаление salary < 25,000 || salary > 175,000
collection.delete_many({"$or": [{"salary": {"$lt": 25000}}, {"salary": {"$gt": 175000}}]})
print("Удалены документы с зарплатой вне диапазона 25,000 - 175,000.")

# Увеличение age всех документов на 1
collection.update_many({}, {"$inc": {"age": 1}})
print("Возраст увеличен на 1 для всех документов.")

# Поднять selery на 5% для job
jobs_to_update = ["Повар", "Учитель", "Программист"]  # Любые из документа
collection.update_many({"job": {"$in": jobs_to_update}}, {"$mul": {"salary": 1.05}})
print("Зарплата увеличена на 5% для выбранных профессий.")

# Поднять selery на 7% для city
cities_to_update = ["Москва", "Санхенхо", "Ереван"]  # Любые из документа
collection.update_many({"city": {"$in": cities_to_update}}, {"$mul": {"salary": 1.07}})
print("Зарплата увеличена на 7% для выбранных городов.")

# Поднять selery на 10% для сложного предиката
complex_predicate = {
    "city": "Будапешт",  # Произвольный город
    "job": {"$in": ["Программист", "Инженер"]},  # Любые из документа
    "age": {"$gte": 30, "$lte": 60}  # Разумный ручной выбор
}
collection.update_many(complex_predicate, {"$mul": {"salary": 1.10}})
print("Зарплата увеличена на 10% для сложного предиката.")

# Удаление записей по произвольному предикату
collection.delete_many({"year": {"$lt": 2005}})  # year < 2005
print("Удалены записи по произвольному предикату.")

# Результаты в JSON 
all_documents = list(collection.find())
with open("output_results.json", "w", encoding="utf-8") as json_file:
    json.dump(all_documents, json_file, default=json_util.default, ensure_ascii=False, indent=4)
print("Результаты сохранены в файл output_results.json.")

client.close()
