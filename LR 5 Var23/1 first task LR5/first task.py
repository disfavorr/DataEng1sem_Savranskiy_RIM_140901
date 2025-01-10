import pickle
import pymongo
import json

# Параметры в mongo
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "task1lr5" # database name
COLLECTION_NAME = "pkl" # collection name

def load_pkl(file_path):
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data

# Загрузки данных в Mongo
def insert_to_mongo(data):
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    collection.delete_many({})  # Очистка коллекции перед вставкой
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)
    print("Данные загружены в MongoDB.")
    client.close()

# Первые 10 записей, по убыванию salary
def query1():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    result = collection.find({}, {"_id": 0}).sort("salary", -1).limit(10)
    write_to_json(result, "query1_output.json", "Запрос 1: Первые 10 записей по убыванию зарплаты")
    client.close()

# Первые 15 записей age < 30, по убыванию salary
def query2():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    result = collection.find({"age": {"$lt": 30}}, {"_id": 0}).sort("salary", -1).limit(15)
    write_to_json(result, "query2_output.json", "Запрос 2: Первые 15 записей с age < 30 и зарплатой по убыванию")
    client.close()

# Записи из city ='Махадаонда' и 3 jobs, по возрастанию age
def query3():
    city = "Махадаонда"
    professions = ["IT-специалист", "Психолог", "Инженер"]
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    result = collection.find(
        {"city": city, "job": {"$in": professions}},
        {"_id": 0}
    ).sort("age", 1).limit(10)
    write_to_json(result, "query3_output.json", f"Запрос 3: Записи из города {city} и профессий {professions}")
    client.close()

# Count записей с фильтрацией по age, year и salary
def query4():
    age_range = {"$gte": 25, "$lte": 45}
    years = [2019, 2020, 2021, 2022]
    salary_filter = {
        "$or": [
            {"salary": {"$gt": 50000, "$lte": 75000}},
            {"salary": {"$gt": 125000, "$lt": 150000}}
        ]
    }
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    count = collection.count_documents({
        "age": age_range,
        "year": {"$in": years},
        **salary_filter
    })
    
    # Преобразование количества в структуру, которую можно передать в write_to_json т.к. здесь работаем не с выборкой данных, а с подсчётом документов
    write_to_json([{"Количество записей": count}], "query4_output.json", "Запрос 4: Количество записей с age, year и salary фильтрами")
    client.close()

# Запись результатов в JSON
def write_to_json(cursor, file_name, description):
    result_list = list(cursor)
    for item in result_list:
        if "salary" in item:
            item["salary"] = float(item["salary"])  # Конвертация во float, для чисел, чтобы можно было читать
    output = {"Описание запроса": description, "Результаты": result_list}
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"Результат запроса сохранен в {file_name}")


def main():
    # Путь к .pkl
    file_path = "task_1_item.pkl"

    # Загрузка данных из файла и вставка в MongoDB
    data = load_pkl(file_path)
    print(f"Данные из {file_path} загружены.") # Для проверки загрузки в бд
    insert_to_mongo(data)

    query1()
    query2()
    query3()
    query4()

if __name__ == "__main__":
    main()
