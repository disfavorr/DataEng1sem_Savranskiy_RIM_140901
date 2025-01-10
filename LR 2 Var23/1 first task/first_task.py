import numpy as np
import json

matrix = np.load('first_task.npy')

total_sum = np.sum(matrix)
total_avr = np.mean(matrix)

main_diag = np.diagonal(matrix)
sum_MD = np.sum(main_diag)
avr_MD = np.mean(main_diag)

side_diag = np.fliplr(matrix).diagonal()
sum_SD = np.sum(side_diag)
avr_SD = np.mean(side_diag)

max_value = np.max(matrix)
min_value = np.min(matrix)

result = {
    'sum': int(total_sum),
    'avr': float(total_avr),
    'sumMD': int(sum_MD), 
    'avrMD': float(avr_MD),
    'sumSD': int(sum_SD),  
    'avrSD': float(avr_SD),
    'max': int(max_value),
    'min': int(min_value)
}

with open('result.json', 'w') as json_file:
    json.dump(result, json_file, indent=4)

min_val = np.min(matrix)
max_val = np.max(matrix)

normalized_matrix = (matrix - min_val) / (max_val - min_val)

np.save('norm_matrix.npy', normalized_matrix)