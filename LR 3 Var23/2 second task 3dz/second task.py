import json
import os
from bs4 import BeautifulSoup

# Функция для парсинга HTML-файла
def parse_html(file_path):
    products = []
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        product_items = soup.find_all("div", class_="product-item")
        
        for item in product_items:
            product = {}
            product['name'] = item.find("span").text.strip() if item.find("span") else None
            price_tag = item.find("price")
            product['price'] = float(price_tag.text.strip().replace(' ₽', '').replace(' ', '')) if price_tag else None
            # Извлекаем другие характеристики товара
            product['processor'] = item.find("li", {"type": "processor"}).text.strip() if item.find("li", {"type": "processor"}) else None
            product['ram'] = item.find("li", {"type": "ram"}).text.strip() if item.find("li", {"type": "ram"}) else None
            product['matrix'] = item.find("li", {"type": "matrix"}).text.strip() if item.find("li", {"type": "matrix"}) else None
            product['resolution'] = item.find("li", {"type": "resolution"}).text.strip() if item.find("li", {"type": "resolution"}) else None
            product['camera'] = item.find("li", {"type": "camera"}).text.strip() if item.find("li", {"type": "camera"}) else None
            # Добавляем объект в список
            products.append(product)
    return products

# Функция для записи данных в JSON файл
def save_to_json(data, file_name):
    with open(file_name, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# Функции для статистики и фильтрации
def get_numerical_statistics(data, field):
    values = [item[field] for item in data if item[field] is not None]
    if not values:
        return {}
    statistics = {
        'sum': sum(values),
        'min': min(values),
        'max': max(values),
        'average': sum(values) / len(values)
    }
    return statistics
#Вместо processor любой класс
def filter_by_category(data, category):
    return [item for item in data if item.get('processor') == category]

def sort_by_field(data, field):
    return sorted(data, key=lambda x: x.get(field, float('inf')))


def main():
    # Путь к папке с файлами HTML
    folder_path = "D:/PyhonLearnPath/DataEngeneering/dz3var23/2/"
    all_products = []

    # Парсинг .HTML
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            file_path = os.path.join(folder_path, filename)
            products = parse_html(file_path)
            all_products.extend(products)

    # Сохранение всех данных в output.json
    save_to_json(all_products, "output.json")

    # Сортировка по цене
    sorted_by_price = sort_by_field(all_products, 'price')
    save_to_json(sorted_by_price, "sorted_by_price.json")

    # Фильтрация по категории
    filtered_by_category = filter_by_category(all_products, '4x4.4 ГГц') #4x4.4ГГц можно менять на любой существующий в файлах (связан с 45 строкой)
    save_to_json(filtered_by_category, "4x4.4Ghz_Proc_filt.json")

    # Статистика для поля "price"
    price_statistics = get_numerical_statistics(all_products, "price")
    save_to_json(price_statistics, "price_statistics.json")

    # Частота категорий
    category_frequency = {}
    for product in all_products:
        category = product.get("ram") #ram можно менять
        if category:
            category_frequency[category] = category_frequency.get(category, 0) + 1
    save_to_json(category_frequency, "category_frequency.json")

if __name__ == "__main__":
    main()
