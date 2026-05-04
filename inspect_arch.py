import pandas as pd
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
f = '.raw_data/건축내역서_인천소방학교.xlsx'
print(f"=== {os.path.basename(f)} ===")
df = pd.read_excel(f, nrows=20)
header_idx = df.notna().sum(axis=1).idxmax()
print(f"Probable header at row: {header_idx}")
df = pd.read_excel(f, header=header_idx, nrows=5)
print("Columns:", df.columns.tolist())
print(df.head(2).to_dict(orient='records'))
