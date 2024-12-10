import sqlite3
import json
import pickle

# Функция для чтения pickle файла
def read_pickle_file(file_path):
    with open(file_path, "rb") as file:
        return pickle.load(file)

# Чтение данных из pickle файла
pickle_file_path = "subitem.pkl"
data2 = read_pickle_file(pickle_file_path)

conn = sqlite3.connect("books.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS second_table (
    title TEXT,
    price INTEGER,
    place TEXT,
    date TEXT
)
""")

# Заполнение второй таблицы
for row in data2:
    cursor.execute("""
    INSERT INTO second_table (title, price, place, date) VALUES (?, ?, ?, ?)
    """, (row["title"], row["price"], row["place"], row["date"]))

conn.commit()

# Вывод всех книг, доступных только онлайн
zapros1 = cursor.execute("""
SELECT title, price, place, date FROM second_table WHERE place = 'online'
""").fetchall()

# Запрос 1 в JSON
zapros1_named = [
    {
        "title": row[0],
        "price": row[1],
        "place": row[2],
        "date": row[3],
    }
    for row in zapros1
]
with open("zapros1.json", "w", encoding="utf-8") as f:
    json.dump(zapros1_named, f, ensure_ascii=False, indent=4)

# Сумма, минимальная, максимальная, средняя цена книг
zapros2 = cursor.execute("""
SELECT SUM(price) AS total_price,
       MIN(price) AS min_price,
       MAX(price) AS max_price,
       AVG(price) AS avg_price
FROM second_table
""").fetchone()

# Запрос 2 в JSON
zapros2_named = {
    "total_price": zapros2[0],
    "min_price": zapros2[1],
    "max_price": zapros2[2],
    "avg_price": zapros2[3],
}
with open("zapros2.json", "w", encoding="utf-8") as f:
    json.dump(zapros2_named, f, ensure_ascii=False, indent=4)

# Книги с одинаковыми названиями
zapros3 = cursor.execute("""
SELECT books.title, books.author, books.genre, second_table.price, second_table.place, second_table.date
FROM books
JOIN second_table ON books.title = second_table.title
""").fetchall()

# Запрос 3 в JSON
zapros3_named = [
    {
        "title": row[0],
        "author": row[1],
        "genre": row[2],
        "price": row[3],
        "place": row[4],
        "date": row[5],
    }
    for row in zapros3
]
with open("zapros3.json", "w", encoding="utf-8") as f:
    json.dump(zapros3_named, f, ensure_ascii=False, indent=4)

conn.close()
