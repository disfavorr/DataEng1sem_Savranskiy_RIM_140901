import sqlite3
import csv
import json

def main():
    db_name = 'books.db'
    file_name = 'item.csv'

    # БД и таблица
    def create_table():
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                genre TEXT,
                pages INTEGER,
                published_year INTEGER,
                isbn TEXT,
                rating REAL,
                views INTEGER
            );
        ''')
        connection.commit()
        connection.close()

    # Загрузка из файла
    def load_data():
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        with open(file_name, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            for row in csv_reader:
                cursor.execute('''
                    INSERT INTO books (title, author, genre, pages, published_year, isbn, rating, views)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                ''', (row['title'], row['author'], row['genre'], int(row['pages']),
                      int(row['published_year']), row['isbn'], float(row['rating']), int(row['views'])))
        connection.commit()
        connection.close()

    # Запросы к бд
    def export_sorted_to_json(output_file):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM books ORDER BY views DESC LIMIT 33;')
        rows = cursor.fetchall()
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump([dict(zip([column[0] for column in cursor.description], row)) for row in rows], file, ensure_ascii=False, indent=4)
        connection.close()

    def export_statistics_to_json(output_file):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute('SELECT SUM(views), MIN(views), MAX(views), AVG(views) FROM books;')
        stats = cursor.fetchone()
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump({'sum': stats[0], 'min': stats[1], 'max': stats[2], 'avg': stats[3]}, file, ensure_ascii=False, indent=4)
        connection.close()

    def export_genre_frequency_to_json(output_file):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute('SELECT genre, COUNT(*) FROM books GROUP BY genre ORDER BY COUNT(*) DESC;')
        genres = cursor.fetchall()
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump({genre: count for genre, count in genres}, file, ensure_ascii=False, indent=4)
        connection.close()

    def export_filtered_to_json(output_file):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM books WHERE rating > 4.0 ORDER BY views DESC LIMIT 33;')
        rows = cursor.fetchall()
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump([dict(zip([column[0] for column in cursor.description], row)) for row in rows], file, ensure_ascii=False, indent=4)
        connection.close()

    create_table()
    load_data()
    export_sorted_to_json('top_33_sorted.json')
    export_statistics_to_json('statistics.json')
    export_genre_frequency_to_json('genre_frequency.json')
    export_filtered_to_json('filtered_33_rating_more_4.json')

if __name__ == "__main__":
    main()
