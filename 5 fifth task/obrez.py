import pandas as pd

file_path = "cds.csv"  
data = pd.read_csv(file_path)

new_date = data[:100000]

new_date.to_csv("cds.csv", index=False)
