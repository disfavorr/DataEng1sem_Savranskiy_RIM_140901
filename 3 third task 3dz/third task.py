import json
import os
import xml.etree.ElementTree as ET

# Функция для парсинга XML-файла
def parse_xml(file_path):
    stars = []
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Извлечение данных из XML
    star = {}
    star['name'] = root.find('name').text.strip() if root.find('name') is not None else None
    star['constellation'] = root.find('constellation').text.strip() if root.find('constellation') is not None else None
    star['spectral_class'] = root.find('spectral-class').text.strip() if root.find('spectral-class') is not None else None
    star['radius'] = float(root.find('radius').text.strip()) if root.find('radius') is not None else None
    star['rotation'] = root.find('rotation').text.strip() if root.find('rotation') is not None else None
    star['age'] = root.find('age').text.strip() if root.find('age') is not None else None
    star['distance'] = root.find('distance').text.strip() if root.find('distance') is not None else None
    star['absolute_magnitude'] = root.find('absolute-magnitude').text.strip() if root.find('absolute-magnitude') is not None else None

    stars.append(star)
    return stars

# Запись данных в JSON файл
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

def filter_by_field(data, field, value):
    return [item for item in data if item.get(field) == value]

def sort_by_field(data, field):
    return sorted(data, key=lambda x: x.get(field, float('inf')))

def main():
    # Путь к папке с файлами XML
    folder_path = "D:/PyhonLearnPath/DataEngeneering/dz3var23/3/"
    all_stars = []

    # Парсинг всех .xml в папке
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            file_path = os.path.join(folder_path, filename)
            stars = parse_xml(file_path)
            all_stars.extend(stars)

    # Сохрание всех данных в output.json
    save_to_json(all_stars, "all-in-output.json")

    # Сортировка по радиусу
    sorted_by_radius = sort_by_field(all_stars, 'radius')
    save_to_json(sorted_by_radius, "sorted_by_radius.json")

    # Фильтрация по созвездию
    filtered_by_constellation = filter_by_field(all_stars, 'constellation', 'Лев') #Поле созвездие и 'Лев' заменимы
    save_to_json(filtered_by_constellation, "filtered_by_sozvezdie.json")

    # Статистика для поля "radius"
    radius_statistics = get_numerical_statistics(all_stars, "radius")
    save_to_json(radius_statistics, "radius_statistics.json")

    # Частота созвездий
    constellation_frequency = {}
    for star in all_stars:
        constellation = star.get("constellation")
        if constellation:
            constellation_frequency[constellation] = constellation_frequency.get(constellation, 0) + 1
    save_to_json(constellation_frequency, "constellation_frequency.json")

if __name__ == "__main__":
    main()
