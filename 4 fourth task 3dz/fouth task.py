import os
import json
import xml.etree.ElementTree as ET
from collections import Counter

# Папка с файлами
folder_path = 'D:/PyhonLearnPath/DataEngeneering/dz3var23/4' 

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    items = []

    for clothing in root.findall('clothing'):
        item = {}
        for elem in clothing:
            item[elem.tag] = elem.text.strip() if elem.text else None
        items.append(item)
    
    return items

# Чтение всех XML-файлов
all_items = []
for filename in os.listdir(folder_path):
    if filename.endswith('.xml'):
        file_path = os.path.join(folder_path, filename)
        all_items.extend(parse_xml(file_path))

# Вывод всех данных в JSON
with open('vse-v-output.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_items, json_file, ensure_ascii=False, indent=4)

# Сортировка по price
sorted_items = sorted(all_items, key=lambda x: float(x.get('price', 0)))

# Фильтрация по категории
filtered_items = [item for item in all_items if item.get('category') == 'Hat'] #Вместо hat(шляпа) можно любую другую

# Ценовая стат-ка
prices = [float(item['price']) for item in all_items if item.get('price')]
price_sum = sum(prices)
price_min = min(prices)
price_max = max(prices)
price_avg = price_sum / len(prices) if prices else 0

# Частотный анализ по категории
categories = [item['category'] for item in all_items if item.get('category')]
category_counts = dict(Counter(categories))

# Запись статистики в JSON-файлы
with open('price_stats.json', 'w', encoding='utf-8') as price_stats_file:
    json.dump({
        'sum': price_sum,
        'min': price_min,
        'max': price_max,
        'avg': price_avg
    }, price_stats_file, ensure_ascii=False, indent=4)

# Вывод частотного анализа из 47 строки
with open('category_counts.json', 'w', encoding='utf-8') as category_counts_file:
    json.dump(category_counts, category_counts_file, ensure_ascii=False, indent=4)

# Вывод данных отфильтрованных в 37 строке
with open('filtered_shlyapa.json', 'w', encoding='utf-8') as filtered_file:
    json.dump(filtered_items, filtered_file, ensure_ascii=False, indent=4)