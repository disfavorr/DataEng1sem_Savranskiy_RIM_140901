import sqlite3
import msgpack
import json

# Чтения .msgpack файла
def read_msgpack_file(file_path):
    with open(file_path, 'rb') as f:
        return msgpack.load(f, raw=False)

# Чтения .json файла
def read_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Создание таблицы
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            price REAL,
            quantity INTEGER,
            category TEXT,
            update_count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()

# Вставка данных о товарах
def insert_products(conn, products):
    cursor = conn.cursor()
    for product in products:
        cursor.execute('''
            INSERT OR IGNORE INTO products (name, price, quantity, category)
            VALUES (?, ?, ?, ?)
        ''', (
            product['name'], 
            product['price'], 
            product['quantity'], 
            product.get('category', 'unknown')
        ))
    conn.commit()

# Обновление данных о товарах
def apply_updates(conn, updates):
    cursor = conn.cursor()
    for update in updates:
        with conn: 
            if update['method'] == 'price_abs':
                cursor.execute('''
                    UPDATE products
                    SET price = price + ?, update_count = update_count + 1
                    WHERE name = ? AND price + ? >= 0
                ''', (update['param'], update['name'], update['param']))
            elif update['method'] == 'quantity_add':
                cursor.execute('''
                    UPDATE products
                    SET quantity = quantity + ?, update_count = update_count + 1
                    WHERE name = ? AND quantity + ? >= 0
                ''', (update['param'], update['name'], update['param']))
            elif update['method'] == 'quantity_sub':
                cursor.execute('''
                    UPDATE products
                    SET quantity = quantity - ?, update_count = update_count + 1
                    WHERE name = ? AND quantity - ? >= 0
                ''', (update['param'], update['name'], update['param']))
            elif update['method'] == 'remove':
                cursor.execute('DELETE FROM products WHERE name = ?', (update['name'],))
            
# Сохранение
def save_to_file(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Топ-10 самых обновляемых товаров
def top_updated_products(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, update_count
        FROM products
        ORDER BY update_count DESC
        LIMIT 10
    ''')
    results = cursor.fetchall()
    return [{"товар": row[0], "количество обновлений": row[1]} for row in results]

# Анализ цен товаров
def analyze_prices(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT category,
               COUNT(*) AS count,
               SUM(price) AS total,
               MIN(price) AS min_price,
               MAX(price) AS max_price,
               AVG(price) AS avg_price
        FROM products
        GROUP BY category
    ''')
    results = cursor.fetchall()
    return [
        {
            "категория": row[0],
            "количество товаров": row[1],
            "общая стоимость": row[2],
            "минимальная цена": row[3],
            "максимальная цена": row[4],
            "средняя цена": row[5]
        }
        for row in results
    ]

# Анализ остатков товаров
def analyze_quantities(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT category,
               COUNT(*) AS count,
               SUM(quantity) AS total,
               MIN(quantity) AS min_quantity,
               MAX(quantity) AS max_quantity,
               AVG(quantity) AS avg_quantity
        FROM products
        GROUP BY category
    ''')
    results = cursor.fetchall()
    return [
        {
            "категория": row[0],
            "количество товаров": row[1],
            "общий остаток": row[2],
            "минимальный остаток": row[3],
            "максимальный остаток": row[4],
            "средний остаток": row[5]
        }
        for row in results
    ]

# Товары с остатком больше среднего
def custom_query(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, quantity, category
        FROM products
        WHERE quantity > (SELECT AVG(quantity) FROM products)
    ''')
    results = cursor.fetchall()
    return [{"товар": row[0], "остаток": row[1], "категория": row[2]} for row in results]





def main():
    conn = sqlite3.connect('products.db')
    create_table(conn)

    # Загрузка данных
    products = read_msgpack_file('_product_data.msgpack')
    updates = read_json_file('_update_data.json')

    # Вставка данных и применение изменений
    insert_products(conn, products)
    apply_updates(conn, updates)

    # Запросы
    top_updates = top_updated_products(conn)
    save_to_file(top_updates, 'top_updated_products.json')

    price_analysis = analyze_prices(conn)
    save_to_file(price_analysis, 'price_analysis.json')

    quantity_analysis = analyze_quantities(conn)
    save_to_file(quantity_analysis, 'quantity_analysis.json')

    custom_results = custom_query(conn)
    save_to_file(custom_results, 'custom_query_results.json')

    conn.close()

if __name__ == '__main__':
    main()
