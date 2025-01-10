import pandas as pd
import numpy as np
import msgpack
import json
import os

file_path = "cds.csv"  
data = pd.read_csv(file_path)

#Выбор столбцов
selected_columns = ["Date", "Ticker", "PX1", "PX2", "PX3", "PX4", "PX5", "PX6"]
selected_data = data[selected_columns]

#Обозначение с числовыми столбцами
numerical_columns = ["PX1", "PX2", "PX3", "PX4", "PX5", "PX6"]
statistics = {}

for column in numerical_columns:
    col_data = selected_data[column]
    statistics[column] = {
        "max": col_data.max(),
        "min": col_data.min(),
        "mean": col_data.mean(),
        "sum": col_data.sum(),
        "std": col_data.std()
    }

#Анализ текстовых данных
text_column = "Ticker"
text_frequency = selected_data[text_column].value_counts().to_dict()

#Анализ в JSON
analysis_results = {
    "numerical_analysis": statistics,
    "text_frequency": text_frequency
}

with open("analysis_results.json", "w", encoding="utf-8") as f:
    json.dump(analysis_results, f, ensure_ascii=False, indent=4)

selected_data.to_csv("selected_data.csv", index=False)
selected_data.to_json("selected_data.json", orient="records", indent=4)
selected_data.to_pickle("selected_data.pkl")
with open("selected_data.msgpack", "wb") as f:
    packed = msgpack.packb(selected_data.to_dict(orient="records"))
    f.write(packed)

#Сравнение
file_formats = ["selected_data.csv", "selected_data.json", "selected_data.pkl", "selected_data.msgpack"]
file_sizes = {file: os.path.getsize(file) for file in file_formats}

#Сохранение в отдельный файл
with open("file_size_comp.txt", "w", encoding="utf-8") as f:
    f.write("Размеры файлов в байтах:\n")
    for file, size in file_sizes.items():
        f.write(f"{file}: {size} байт\n")

print("Размеры файлов записаны в 'file_size_comp.txt'")