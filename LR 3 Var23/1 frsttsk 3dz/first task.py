from bs4 import BeautifulSoup
import os
import json
import pandas as pd
import numpy as np

data = []

# Обработка каждого файла
for file in os.listdir("D:/PyhonLearnPath/DataEngeneering/dz3var23/first task"):  # Замените "html_files" на вашу папку
    if file.endswith(".html"):
        with open(os.path.join("D:/PyhonLearnPath/DataEngeneering/dz3var23/first task", file), "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

            # Город
            city = soup.find("span").text.replace("Город:", "").strip()

            # Название строения
            building_title = soup.find("h1", class_="title").text.replace("Строение:", "").strip()

            # Адрес
            address_p = soup.find("p", class_="address-p").text.strip()
            street = address_p.split("Индекс:")[0].replace("Улица:", "").strip()
            postal_code = address_p.split("Индекс:")[1].strip()

            # Этажи
            floors = soup.find("span", class_="floors").text.replace("Этажи:", "").strip()

            # Год постройки
            year_built = soup.find("span", class_="year").text.replace("Построено в", "").strip()

            # Парковка
            parking = soup.find("div").find_all("span")[-1].text.replace("Парковка:", "").strip()

            # Рейтинг и просмотры
            rating_div = soup.find_all("div")[-1]
            rating = rating_div.find_all("span")[0].text.replace("Рейтинг:", "").strip()
            views = rating_div.find_all("span")[1].text.replace("Просмотры:", "").strip()

            # Сохранение в список
            data.append({
                "Город": city,
                "Название строения": building_title,
                "Улица": street,
                "Индекс": postal_code,
                "Этажи": int(floors),
                "Год постройки": int(year_built),
                "Парковка": parking,
                "Рейтинг": float(rating),
                "Просмотры": int(views),
            })

# Создание DataFrame
df = pd.DataFrame(data)

# Сохранение в JSON
df.to_json("parsed_data.json", orient="records", indent=4, force_ascii=False)

# Дополнительные задачи
# Сортировка по рейтингу
df_sorted = df.sort_values(by="Рейтинг", ascending=False)
df_sorted.to_json("sorted_by_rating.json", orient="records", indent=4, force_ascii=False)

# Фильтрация по парковке
df_parking = df[df["Парковка"] == "есть"]
df_parking.to_json("parking_filter.json", orient="records", indent=4, force_ascii=False)

# Статистика по просмотрам
views_stats = {
    "Сумма": df["Просмотры"].sum(),
    "Среднее": df["Просмотры"].mean(),
    "Минимум": df["Просмотры"].min(),
    "Максимум": df["Просмотры"].max(),
    "Стандартное отклонение": df["Просмотры"].std(),
}

# Частота меток для парковки
parking_frequency = df["Парковка"].value_counts().to_dict()

# Преобразование всех значений в stats в стандартные типы Python
stats = {
    "Статистика по просмотрам": {key: int(value) if isinstance(value, (np.integer, np.int64)) else float(value)
                                 for key, value in views_stats.items()},
    "Частота парковки": {key: int(value) for key, value in parking_frequency.items()},
}

# Сохранение статистики
with open("stats.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=4, ensure_ascii=False)

