import pandas as pd
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

files = glob.glob('.raw_data/*.xlsx')
for f in files:
    print(f"=== {os.path.basename(f)} ===")
    try:
        # Read the first sheet, first 20 rows
        df = pd.read_excel(f, nrows=20)
        
        # Let's find the first row that has many non-null values, likely the header
        header_idx = df.notna().sum(axis=1).idxmax()
        print(f"Probable header at row: {header_idx}")
        
        # Read again with the proper header
        df = pd.read_excel(f, header=header_idx, nrows=5)
        print("Columns:", df.columns.tolist())
        print(df.head(2).to_dict(orient='records'))
    except Exception as e:
        print("Error:", e)
    print("\n")
