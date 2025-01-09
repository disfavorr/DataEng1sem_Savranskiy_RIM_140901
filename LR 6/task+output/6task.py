import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Загрузка данных и анализ памяти
chunk_size = 100000  # Используем чанки из-за большого размера файла
columns_to_load = [
    "Job Id", "Experience", "Qualifications", "Salary Range",
    "location", "Country", "Work Type", "Company Size",
    "Job Title", "skills"
]

# Выгружаем данные из файла
chunks = pd.read_csv("job_descriptions.csv", chunksize=chunk_size)
data = pd.concat(chunks, ignore_index=True)

# Сохраняем статистику до оптимизации
memory_stats = data.memory_usage(deep=True)
memory_stats_df = pd.DataFrame(memory_stats, columns=["Memory_Bytes"]).reset_index()
memory_stats_df.columns = ["Column", "Memory_Bytes"]
memory_stats_df.sort_values(by="Memory_Bytes", ascending=False, inplace=True)
memory_stats_df.to_json("memory_stats_unoptimized.json", orient="records", indent=4)

# 2. Оптимизация колонок с типом `object`
for col in data.select_dtypes(include=["object"]).columns:
    if data[col].nunique() / len(data) < 0.5:
        data[col] = data[col].astype("category")

# 3. Понижающее преобразование типов `int`
for col in data.select_dtypes(include=["int"]).columns:
    data[col] = pd.to_numeric(data[col], downcast="integer")

# 4. Понижающее преобразование типов `float`
for col in data.select_dtypes(include=["float"]).columns:
    data[col] = pd.to_numeric(data[col], downcast="float")

# 5. Сохраняем статистику после оптимизации
optimized_memory_stats = data.memory_usage(deep=True)
optimized_memory_stats_df = pd.DataFrame(optimized_memory_stats, columns=["Memory_Bytes"]).reset_index()
optimized_memory_stats_df.columns = ["Column", "Memory_Bytes"]
optimized_memory_stats_df.sort_values(by="Memory_Bytes", ascending=False, inplace=True)
optimized_memory_stats_df.to_json("memory_stats_optimized.json", orient="records", indent=4)

# 6. Сохранение поднабора данных
optimized_subset = data[columns_to_load]
optimized_subset.to_csv("optimized_subset.csv", index=False)

# 7. Построение графиков
# График распределения зарплат
plt.figure(figsize=(10, 6))
sns.histplot(data["Salary Range"].dropna(), kde=True)
plt.title("Salary Range Distribution")
plt.xlabel("Salary Range")
plt.ylabel("Frequency")
plt.savefig("salary_distribution.png")
plt.show()

# Корреляционная матрица
plt.figure(figsize=(10, 8))
correlation_matrix = data.corr(numeric_only=True)
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.savefig("correlation_matrix.png")
plt.show()

# Распределение опыта работы
experience_counts = data["Experience"].value_counts()
plt.figure(figsize=(12, 6))
experience_counts.plot(kind="bar", color="skyblue")
plt.title("Experience Levels in Job Descriptions")
plt.xlabel("Experience")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=45)
plt.savefig("experience_distribution.png")
plt.show()

# Круговая диаграмма по типу работы
work_type_counts = data["Work Type"].value_counts()
plt.figure(figsize=(8, 8))
work_type_counts.plot(kind="pie", autopct='%1.1f%%', colors=sns.color_palette("pastel"))
plt.title("Work Type Distribution")
plt.ylabel("")
plt.savefig("work_type_distribution.png")
plt.show()
