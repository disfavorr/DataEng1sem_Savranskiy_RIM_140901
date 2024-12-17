import csv
import pymongo
import json

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "task1lr5"
COLLECTION_NAME = "pkl"

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Из CSV в MongoDB
def load_csv_to_mongo(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        data = []
        for row in reader:
            data.append({
                "job": row["job"],
                "salary": float(row["salary"]),
                "id": int(row["id"]),
                "city": row["city"],
                "year": int(row["year"]),
                "age": int(row["age"]),
            })
        collection.insert_many(data)

# Загрузим данные в коллекцию
load_csv_to_mongo("task_2_item.csv")

# min, avg, max salary
def salary_stats():
    pipeline = [
        {"$group": {
            "_id": None,
            "min_salary": {"$min": "$salary"},
            "avg_salary": {"$avg": "$salary"},
            "max_salary": {"$max": "$salary"}
        }}
    ]
    result = list(collection.aggregate(pipeline))
    write_to_json(result, "salary_stats_output.json", "Минимальная, средняя, максимальная зарплата")

# Вывод количества данных по представленным профессиям
def job_count():
    pipeline = [
        {"$group": {
            "_id": "$job",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}}  # Сортируем по количеству
    ]
    result = list(collection.aggregate(pipeline))
    write_to_json(result, "job_count_output.json", "Количество данных по профессиям")

# min, avg, max salary по id city
def salary_by_city():
    pipeline = [
        {"$group": {
            "_id": "$city",
            "min_salary": {"$min": "$salary"},
            "avg_salary": {"$avg": "$salary"},
            "max_salary": {"$max": "$salary"}
        }},
        {"$sort": {"_id": 1}}  # Сортируем города
    ]
    result = list(collection.aggregate(pipeline))
    write_to_json(result, "salary_by_city_output.json", "Минимальная, средняя, максимальная зарплата по городу")

# min, avg, max salary по id job
def salary_by_job():
    pipeline = [
        {"$group": {
            "_id": "$job",
            "min_salary": {"$min": "$salary"},
            "avg_salary": {"$avg": "$salary"},
            "max_salary": {"$max": "$salary"}
        }},
        {"$sort": {"_id": 1}}  # Сортируем профессии
    ]
    result = list(collection.aggregate(pipeline))
    write_to_json(result, "salary_by_job_output.json", "Минимальная, средняя, максимальная зарплата по профессии")

# min, avg, max age по id city
def age_by_city():
    pipeline = [
        {"$group": {
            "_id": "$city",
            "min_age": {"$min": "$age"},
            "avg_age": {"$avg": "$age"},
            "max_age": {"$max": "$age"}
        }},
        {"$sort": {"_id": 1}}  # Сортируем города
    ]
    result = list(collection.aggregate(pipeline))
    write_to_json(result, "age_by_city_output.json", "Минимальный, средний, максимальный возраст по городу")

# min, avg, max age по id job
def age_by_job():
    pipeline = [
        {"$group": {
            "_id": "$job",
            "min_age": {"$min": "$age"},
            "avg_age": {"$avg": "$age"},
            "max_age": {"$max": "$age"}
        }},
        {"$sort": {"_id": 1}}  # Сортируем профессии
    ]
    result = list(collection.aggregate(pipeline))
    write_to_json(result, "age_by_job_output.json", "Минимальный, средний, максимальный возраст по профессии")

# max selery min age
def max_salary_min_age():
    pipeline = [
        {"$group": {
            "_id": "$age",
            "max_salary": {"$max": "$salary"}
        }},
        {"$sort": {"_id": 1}}  # Сортируем по возрасту
    ]
    result = list(collection.aggregate(pipeline))
    min_age = min([item["_id"] for item in result])
    for item in result:
        if item["_id"] == min_age:
            write_to_json([item], "max_salary_min_age_output.json", f"Максимальная зарплата при минимальном возрасте ({min_age})")
            break

# min salary max age
def min_salary_max_age():
    pipeline = [
        {"$group": {
            "_id": "$age",
            "min_salary": {"$min": "$salary"}
        }},
        {"$sort": {"_id": -1}}  # Сортируем по возрасту с убывающем
    ]
    result = list(collection.aggregate(pipeline))
    max_age = max([item["_id"] for item in result])
    for item in result:
        if item["_id"] == max_age:
            write_to_json([item], "min_salary_max_age_output.json", f"Минимальная зарплата при максимальном возрасте ({max_age})")
            break

# min, avg, max age по id city, salary < 50 000, avg age убывает
def age_by_city_salary_above_50000():
    pipeline = [
        {"$match": {"salary": {"$gt": 50000}}},
        {"$group": {
            "_id": "$city",
            "min_age": {"$min": "$age"},
            "avg_age": {"$avg": "$age"},
            "max_age": {"$max": "$age"}
        }},
        {"$sort": {"avg_age": -1}}  # Сортируем по возрасту по убыванию
    ]
    result = list(collection.aggregate(pipeline))
    write_to_json(result, "age_by_city_salary_above_50000_output.json", "Возраст по городу с зарплатой > 50000, сортировка по avg")

# min, avg, max salary, city job age произвольные условия
def salary_in_ranges():
    pipeline = [
        {"$match": {"age": {"$gt": 18, "$lt": 25}, "salary": {"$gt": 50000, "$lt": 75000}}},
        {"$group": {
            "_id": {"city": "$city", "job": "$job"},
            "min_salary": {"$min": "$salary"},
            "avg_salary": {"$avg": "$salary"},
            "max_salary": {"$max": "$salary"}
        }}
    ]
    result = list(collection.aggregate(pipeline))
    write_to_json(result, "salary_in_ranges_output.json", "Минимальная, средняя, максимальная зарплата в диапазонах по городу, профессии и возрасту")

# Произвольный запрос с $match, $group, $sort
def arbitrary_query():
    pipeline = [
        {"$match": {"salary": {"$gte": 60000}}},
        {"$group": {
            "_id": "$job",
            "avg_salary": {"$avg": "$salary"}
        }},
        {"$sort": {"avg_salary": -1}}  # Сортируем по средней зарплате по убыванию
    ]
    result = list(collection.aggregate(pipeline))
    write_to_json(result, "arbitrary_query_output.json", "Произвольный запрос с $match, $group, $sort")

# Запись данных в json
def write_to_json(data, file_name, description):
    output = {"Описание запроса": description, "Результаты": data}
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"Результат запроса сохранен в {file_name}")

salary_stats() # 1 (33)
job_count() # 2 (46)
salary_by_city() # 3 (58)
salary_by_job() # 4 (72)
age_by_city() # 5 (86)
age_by_job() # 6 (100)
max_salary_min_age() # 7 (114)
min_salary_max_age() # 8 (130)
age_by_city_salary_above_50000() # 9 (146)
salary_in_ranges() # 10 (161)
arbitrary_query() # 11 (175)

# Закрываем подключение к MongoDB
client.close()
