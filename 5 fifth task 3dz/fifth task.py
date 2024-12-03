import requests
from bs4 import BeautifulSoup
import json
from collections import Counter

# URL
url = 'https://www.classic-dent.ru/service/'

# Парсинг страницы с услугами
def parse_services_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Список для хранения услуг
    services = []

    # Поиск всех блоков с услугами
    price_categories = soup.find_all('div', class_='price-category-block')

    # Обработка каждой категории
    for category in price_categories:
        category_name = category.find('span').text.strip()  # Название категории

        # Все услуги в категории
        services_in_category = category.find_all('div', class_='price-item-block')

        for service in services_in_category:
            service_name = service.find('a').text.strip()  # Название услуги
            service_price = service.find('div', class_='price-item-price').text.strip()  # Цена услуги

            # Добавление услуги в список
            services.append({
                'category': category_name,
                'name': service_name,
                'price': service_price
            })
    
    return services

# Конвертация цены в числовое значение и диапазонов в среднее
def parse_price(price):
    # Минус пробелы и слово "от", если оно есть
    price = price.replace(' ', '').replace('от', '')
    
    # Если цена указана как диапазон, считаем по среднему
    if '-' in price:
        price_range = price.split('-')
        try:
            return (float(price_range[0]) + float(price_range[1])) / 2
        except ValueError:
            return None
    # Если цена фикс
    elif price.isdigit():
        return float(price)
    # Бесплатно = 0
    elif price.lower() == "бесплатно":
        return 0
    else:
        return None

services = parse_services_page(url)

# Сортировка по возрастанию цены
services_sorted_by_price = sorted(services, key=lambda x: parse_price(x['price']) if parse_price(x['price']) is not None else 0)

# Фильтрация по Исправление прикуса
filtered_services = [service for service in services if "Исправление прикуса" in service['category']]

# Статистика по цене
prices = [parse_price(service['price']) for service in services if parse_price(service['price']) is not None]

price_sum = sum(prices)
price_min = min(prices) if prices else 0
price_max = max(prices) if prices else 0
price_avg = price_sum / len(prices) if prices else 0

# Частотный анализ по категориям
category_counts = dict(Counter(service['category'] for service in services))

# Сортировка по цене
with open('services_sorted_by_price.json', 'w', encoding='utf-8') as f:
    json.dump(services_sorted_by_price, f, ensure_ascii=False, indent=4)

# Фильтрация по Исправление прикуса из 67 строки
with open('filtered_services_prikus.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_services, f, ensure_ascii=False, indent=4)

# Статистика по цене
statistics = {
    "price_sum": price_sum,
    "price_min": price_min,
    "price_max": price_max,
    "price_avg": price_avg
}

with open('price_statistics.json', 'w', encoding='utf-8') as f:
    json.dump(statistics, f, ensure_ascii=False, indent=4)

# Частотный анализ по категориям
with open('category_frequency.json', 'w', encoding='utf-8') as f:
    json.dump(category_counts, f, ensure_ascii=False, indent=4)
