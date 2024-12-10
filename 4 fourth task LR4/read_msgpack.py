import msgpack

# Функция для чтения данных из .msgpack
def read_msgpack_file(file_path):
    with open(file_path, 'rb') as file:
        data = msgpack.load(file, raw=False)  # raw=False позволит автоматически декодировать строки как utf-8
    return data

# Пример использования
file_path = '_product_data.msgpack'
data = read_msgpack_file(file_path)

# Вывод данных для проверки
print(data)
