import sqlite3
import csv
import json
import os

# БД
DB_NAME = 'games_database.db'
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Таблицы
def create_tables():
    # CSV
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games_csv (
            appid INTEGER PRIMARY KEY,
            name TEXT,
            release_date TEXT,
            developer TEXT,
            positive_ratings INTEGER,
            negative_ratings INTEGER,
            price REAL
        )
    ''')
    # JSON
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games_json (
            id INTEGER PRIMARY KEY,
            game TEXT,
            release_date TEXT,
            peak_players INTEGER,
            total_reviews INTEGER,
            rating REAL,
            publisher TEXT
        )
    ''')
    # TXT
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS steamcharts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month_year TEXT,
            avg_players REAL,
            peak_players INTEGER,
            game_name TEXT
        )
    ''')
    conn.commit()

# CSV
def load_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('''
                INSERT OR IGNORE INTO games_csv 
                (appid, name, release_date, developer, positive_ratings, negative_ratings, price) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['appid'],
                row['name'],
                row['release_date'],
                row['developer'],
                int(row['positive_ratings']),
                int(row['negative_ratings']),
                float(row['price'])
            ))
    conn.commit()

# JSON
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for idx, game in enumerate(data):
            cursor.execute('''
                INSERT OR IGNORE INTO games_json
                (id, game, release_date, peak_players, total_reviews, rating, publisher)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                idx,
                game['game'],
                game['release'],
                int(game['peak_players'].replace(",", "")),
                int(game['total_reviews']),
                float(game['rating']),
                game['publisher']
            ))
    conn.commit()

# TXT
def load_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        next(file)  # Пропускаем заголовок
        for line in file:
            parts = line.strip().split(" | ")
            cursor.execute('''
                INSERT INTO steamcharts (month_year, avg_players, peak_players, game_name) 
                VALUES (?, ?, ?, ?)
            ''', (
                parts[0],
                float(parts[1]),
                int(parts[4]),
                parts[-1]
            ))
    conn.commit()

# Запросы
def run_queries(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # output1. Простая выборка с условием + сортировка + ограничение
    cursor.execute('''
        SELECT name, positive_ratings, price 
        FROM games_csv 
        WHERE positive_ratings > 1000
        ORDER BY positive_ratings DESC 
        LIMIT 5
    ''')
    result = [{"name": row[0], "positive_ratings": row[1], "price": row[2]} for row in cursor.fetchall()]
    with open(os.path.join(output_dir, 'query1.json'), 'w') as file:
        json.dump(result, file, indent=4)

    # output2. Подсчет игр с положительными отзывами > 5000
    cursor.execute('''
        SELECT COUNT(*) 
        FROM games_csv 
        WHERE positive_ratings > 5000
    ''')
    result = cursor.fetchone()
    with open(os.path.join(output_dir, 'query2.json'), 'w') as file:
        json.dump({"count_positive_ratings_5000": result[0]}, file, indent=4)

    # output3. Средний рейтинг по играм из JSON
    cursor.execute('''
        SELECT AVG(rating) 
        FROM games_json
    ''')
    result = cursor.fetchone()
    with open(os.path.join(output_dir, 'query3.json'), 'w') as file:
        json.dump({"average_rating_json": result[0]}, file, indent=4)

    # output4. Группировка по месяцам из TXT и подсчет среднего количества игроков
    cursor.execute('''
        SELECT month_year, AVG(avg_players)
        FROM steamcharts
        GROUP BY month_year
    ''')
    result = [{"month_year": row[0], "average_players": row[1]} for row in cursor.fetchall()]
    with open(os.path.join(output_dir, 'query4.json'), 'w') as file:
        json.dump(result, file, indent=4)

    # output5. Обновление данных (например, удваиваем количество отзывов)
    cursor.execute('''
        UPDATE games_csv 
        SET positive_ratings = positive_ratings * 2 
        WHERE positive_ratings > 10000
    ''')
    conn.commit()

    cursor.execute('SELECT name, positive_ratings FROM games_csv WHERE positive_ratings > 20000')
    result = [{"name": row[0], "updated_positive_ratings": row[1]} for row in cursor.fetchall()]
    with open(os.path.join(output_dir, 'query5.json'), 'w') as file:
        json.dump(result, file, indent=4)

# Главная функция
def main():
    create_tables()
    load_csv('games.csv')
    load_json('games.json')
    load_txt('steamcharts.txt')
    run_queries('Вывод запросов')

    print("Результаты запросов созранены в отдельной папке 'Вывод запросов'")

if __name__ == '__main__':
    main()
