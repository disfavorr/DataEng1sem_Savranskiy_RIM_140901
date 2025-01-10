import msgpack

def read_msgpack_file(file_path):
    with open(file_path, 'rb') as file:
        data = msgpack.load(file, raw=False)  # raw=False - декодирует строки как utf-8
    return data

file_path = 'task_3_item.msgpack'
data = read_msgpack_file(file_path)

print(data)