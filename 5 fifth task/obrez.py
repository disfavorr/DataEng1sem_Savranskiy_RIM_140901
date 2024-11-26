import pandas as pd

file_path = "cds.csv"  
data = pd.read_csv(file_path)

new_date = data[:500000]

selected_data.to_csv("selected_data.csv", index=False)