import sqlite3
import json
import csv

# text файл
def read_text_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip().split('=====')
        for record in content:
            record_data = {}
            for line in record.splitlines():
                # Пропуск строк, не содержащих '::'
                if '::' in line:
                    key, value = line.split('::')
                    record_data[key.strip()] = value.strip()
            if record_data:  # Только непустые записи
                data.append(record_data)
    return data


# csv файл
def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        return [row for row in csv_reader]

text_file_path = '_part_1.text'  
csv_file_path = '_part_2.csv'    

text_data = read_text_file(text_file_path)
csv_data = read_csv_file(csv_file_path)

# Создание/подключение к БД
conn = sqlite3.connect("super_music_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS music_data (
    artist TEXT,
    song TEXT,
    duration_ms INTEGER,
    year INTEGER,
    tempo REAL,
    genre TEXT,
    loudness REAL
)
""")

# text файл в таблицу
for row in text_data:
    cursor.execute("""
    INSERT INTO music_data (artist, song, duration_ms, year, tempo, genre, loudness)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (row['artist'], row['song'], int(row['duration_ms']), int(row['year']),
          float(row['tempo']), row['genre'], float(row['loudness'])))

# csv файл в таблицу
for row in csv_data:
    cursor.execute("""
    INSERT INTO music_data (artist, song, duration_ms, year, tempo, genre, loudness)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (row['artist'], row['song'], int(row['duration_ms']), int(row['year']),
          float(row['tempo']), row['genre'], float(row['loudness'])))

conn.commit()

# Вывод первых 33 строк, отсортированных по длительности (duration_ms)
zapros1 = cursor.execute("""
SELECT artist, song, duration_ms, year, tempo, genre, loudness FROM music_data
ORDER BY duration_ms DESC
LIMIT 33
""").fetchall()

# Запрос 1 в JSON
zapros1_named = [
    {
        "Артист": row[0],
        "Трек": row[1],
        "Длительность(мс)": row[2],
        "Год": row[3],
        "Темп(?)": row[4],
        "Жанр": row[5],
        "Громкость(?)": row[6],
    }
    for row in zapros1
]
with open("zapros1.json", "w", encoding="utf-8") as f:
    json.dump(zapros1_named, f, ensure_ascii=False, indent=4)

# Сумма, минимальное, максимальное и среднее значение для длительности (duration_ms)
zapros2 = cursor.execute("""
SELECT SUM(duration_ms) AS total_duration,
       MIN(duration_ms) AS min_duration,
       MAX(duration_ms) AS max_duration,
       AVG(duration_ms) AS avg_duration
FROM music_data
""").fetchone()

# Запрос 2 в JSON
zapros2_named = {
    "total_duration": zapros2[0],
    "min_duration": zapros2[1],
    "max_duration": zapros2[2],
    "avg_duration": zapros2[3],
}
with open("zapros2.json", "w", encoding="utf-8") as f:
    json.dump(zapros2_named, f, ensure_ascii=False, indent=4)

# Частота встречаемости для поля genre
zapros3 = cursor.execute("""
SELECT genre, COUNT(*) AS genre_count
FROM music_data
GROUP BY genre
ORDER BY genre_count DESC
""").fetchall()

# Запрос 3 в JSON
zapros3_named = [
    {
        "Жанр": row[0],
        "Треков в этом жанре": row[1],
    }
    for row in zapros3
]
with open("zapros3.json", "w", encoding="utf-8") as f:
    json.dump(zapros3_named, f, ensure_ascii=False, indent=4)

# 38 треков после 2010 года, отсортированных по duration_ms
zapros4 = cursor.execute("""
SELECT artist, song, duration_ms, year, tempo, genre, loudness
FROM music_data
WHERE year > 2010
ORDER BY duration_ms DESC
LIMIT 38
""").fetchall()

# Сохранение результата запроса 4 в файл JSON
zapros4_named = [
    {
        "Артист": row[0],
        "Трек": row[1],
        "Длительность(мс)": row[2],
        "Год": row[3],
        "Темп(?)": row[4],
        "Жанр": row[5],
        "Громкость(?)": row[6],
    }
    for row in zapros4
]
with open("zapros4.json", "w", encoding="utf-8") as f:
    json.dump(zapros4_named, f, ensure_ascii=False, indent=4)

# Закрытие соединения с базой данных
conn.close()

print("Задание выполнено успешно. Результаты сохранены в файлы zapros1.json, zapros2.json, zapros3.json и zapros4.json.")
