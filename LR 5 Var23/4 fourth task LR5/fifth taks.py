import pymongo
import pandas as pd
import json
import os
from bson.json_util import dumps

# Функция сохранения JSON-файлов
def save_to_json(folder, filename, data):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(dumps(data, indent=4, ensure_ascii=False))

# Подключение к MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["task5lr5"]

# Очистка базы перед загрузкой
db["games"].drop()  

# Импорт из games.json 
with open("games.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)
filtered_json_data = [
    {**{k: v for k, v in doc.items() if k not in ["№", "link", "store_asset_mod_time", "players_right_now", "24_hour_peak"]},
     "source": "json"}  # Добавляем источник
    for doc in json_data
]
db["games"].insert_many(filtered_json_data)

# Импорт из games.csv 
csv_data = pd.read_csv("games.csv")
filtered_csv_data = csv_data.drop(columns=["english", "platforms", "required_age", "categories", "steamspy_tags", "achievements"]).to_dict(orient="records")
for record in filtered_csv_data:
    record["source"] = "csv"  # Добавляем источник
db["games"].insert_many(filtered_csv_data)

# Выборка
folder_selection = "Выборка"

# Найти все игры жанра "Action"
action_games = list(db["games"].find({"primary_genre": {"$regex": "Action"}}))
save_to_json(folder_selection, "selection_action_games.json", action_games)

# Найти игры с рейтингом выше 95
high_rating_games = list(db["games"].find({"rating": {"$gte": "95.0"}}))
save_to_json(folder_selection, "selection_high_rating.json", high_rating_games)

# Найти игры разработчика "Valve"
valve_games = list(db["games"].find({"developer": "Valve"}))
save_to_json(folder_selection, "selection_valve_games.json", valve_games)

# Найти игры с отрицательными отзывами больше 5000
high_negative_reviews = list(db["games"].find({"negative_ratings": {"$gte": 5000}}))
save_to_json(folder_selection, "selection_high_neg_reviews.json", high_negative_reviews)

# Найти все игры, у которых рейтинг выше 90
high_rated_games = list(db["games"].find({"rating": {"$gte": "90.0"}}))
save_to_json(folder_selection, "selection_high_rated_games.json", high_rated_games)

# Агрегация 
folder_aggregation = "Выборка с агрегацией"

# Группировка по издателю и подсчёт количества игр
publisher_count = list(db["games"].aggregate([{"$group": {"_id": "$publisher", "game_count": {"$sum": 1}}}]))
save_to_json(folder_aggregation, "aggregation_publisher_count.json", publisher_count)

# Средний рейтинг игр по разработчикам
avg_rating_by_dev = list(db["games"].aggregate([
    {"$group": {"_id": "$developer", "avg_rating": {"$avg": {"$toDouble": "$rating"}}}}]))
save_to_json(folder_aggregation, "aggregation_avg_rating_by_dev.json", avg_rating_by_dev)

# Максимальный и минимальный рейтинг игр
rating_stats = list(db["games"].aggregate([
    {"$group": {"_id": None, "max_rating": {"$max": "$positive_ratings"}, "min_rating": {"$min": "$positive_ratings"}}}]))
save_to_json(folder_aggregation, "aggregation_rating_stats.json", rating_stats)

# Подсчёт игр по жанрам
genre_count = list(db["games"].aggregate([{"$group": {"_id": "$primary_genre", "count": {"$sum": 1}}}]))
save_to_json(folder_aggregation, "aggregation_genre_count.json", genre_count)

# Сумма положительных отзывов по издателям
total_positive_by_publisher = list(db["games"].aggregate([
    {"$group": {"_id": "$publisher", "total_positive": {"$sum": "$positive_ratings"}}}]))
save_to_json(folder_aggregation, "aggregation_positive_by_publisher.json", total_positive_by_publisher)

# Обновление и удаление 
folder_update_delete = "Обновление-удаление данных"

# Увеличить положительные отзывы на 10% для игр "Valve"
db["games"].update_many({"developer": "Valve"}, {"$mul": {"positive_ratings": 1.1}})
updated_valve = list(db["games"].find({"developer": "Valve"}))
save_to_json(folder_update_delete, "update_valve_positive.json", updated_valve)

# Удалить игры с отрицательными отзывами более 10000
db["games"].delete_many({"negative_ratings": {"$gte": 10000}})
remaining_games = list(db["games"].find())
save_to_json(folder_update_delete, "delete_high_neg_reviews.json", remaining_games)

# Обновить жанр на "Retro" для игр до 2005 года
db["games"].update_many({"release_date": {"$lt": "2005-01-01"}}, {"$set": {"genres": "Retro"}})
retro_games = list(db["games"].find({"genres": "Retro"}))
save_to_json(folder_update_delete, "update_retro_games.json", retro_games)

# Удалить игры с ценой выше 10 долларов
db["games"].delete_many({"price": {"$gt": 10}})
affordable_games = list(db["games"].find())
save_to_json(folder_update_delete, "delete_high_price.json", affordable_games)

# Обновить издателя на "Unknown" для пустых значений
db["games"].update_many({"publisher": ""}, {"$set": {"publisher": "Unknown"}})
updated_unknown = list(db["games"].find({"publisher": "Unknown"}))
save_to_json(folder_update_delete, "update_unknown_publisher.json", updated_unknown)

print("Обработал+сохранил")
