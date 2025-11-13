import pandas as pd

df = pd.read_csv("data/raw_data.csv", sep=None, engine="python")
print(df.head())
print(df.columns)
