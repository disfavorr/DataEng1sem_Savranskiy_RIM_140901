import pickle

def read_pickle_file(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

# Пример использования
file_path = 'subitem.pkl'  # Укажите путь к вашему файлу
data = read_pickle_file(file_path)
print(data)
