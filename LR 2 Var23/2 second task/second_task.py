import numpy as np
import os

matrix = np.load('second_task.npy')

threshold = 523 

indices = np.where(matrix > threshold)

values = matrix[indices]

index_array = list(zip(indices[0], indices[1]))

np.savez('orig_second_task.npz', indices=index_array, values=values)
np.savez_compressed('compressed_second_task.npz', indices=index_array, values=values)

original_size = os.path.getsize('orig_second_task.npz')
compressed_size = os.path.getsize('compressed_second_task.npz')

print(f'Original size: {original_size / 1024:.2f} KB')
print(f'Compressed size: {compressed_size / 1024:.2f} KB')
