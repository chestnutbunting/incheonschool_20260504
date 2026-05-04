import pandas as pd
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
file_path = '.raw_data/기계내역서_인천소방학교.xlsx'
df = pd.read_excel(file_path, header=None, skiprows=8)

# Just print out a random sample of item names to see how they differ
items = df[2].dropna().unique()

print(f"Total unique items: {len(items)}")
# Try to find keywords for 전기(Electrical) and 소방(Firefighting)
elec_keywords = ['전선', '케이블', '전등', '스위치', '배전반', '분전반', '차단기', '트레이', '접지', '전기']
fire_keywords = ['소화', '스프링클러', '감지기', '유도등', '발신기', '경종', '피난', '소방', '헤드', '완강기']

elec_items = [i for i in items if any(k in str(i) for k in elec_keywords)]
fire_items = [i for i in items if any(k in str(i) for k in fire_keywords)]

print(f"Potential Electrical items: {len(elec_items)}")
print("Sample Elec:", elec_items[:5])

print(f"Potential Firefighting items: {len(fire_items)}")
print("Sample Fire:", fire_items[:5])
