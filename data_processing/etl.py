import os
import pandas as pd
import sqlite3
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(PROJECT_ROOT, "project_costs.db")
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, ".raw_data")

ELEC_KEYWORDS = ['전선', '케이블', '전등', '스위치', '배전반', '분전반', '차단기', '트레이', '접지', '전기', '등기구']
FIRE_KEYWORDS = ['소화', '스프링클러', '감지기', '유도등', '발신기', '경종', '피난', '소방', '헤드', '완강기', '시각경보', '화재']

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def clean_val(val):
    if pd.isna(val) or val == '' or str(val).strip() == '': return ''
    return str(val).strip()

def clean_num(val):
    if pd.isna(val) or val == '' or str(val).strip() == '': return 0.0
    try: return float(str(val).replace(',', '').strip())
    except: return 0.0

def generate_code(idx):
    return f"인천_{str(idx).zfill(5)}"

global_idx = 1

def extract_building(how2, how4):
    text = str(how2) + " " + str(how4)
    if '본관동' in text: return '본관동'
    if '소방훈련관' in text: return '소방훈련관'
    if '소방종합훈련탑' in text or '훈련탑' in text: return '소방종합훈련탑'
    if '관사동' in text: return '관사동'
    return '기타시설'

def build_row(how1, how2, how4, how5, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, source):
    global global_idx
    code = generate_code(global_idx)
    global_idx += 1
    
    where2 = extract_building(how2, how4)
    
    # 20 columns: code, WHERE1_프로젝트, WHERE2_동, WHERE3_층, HOW1_공사, HOW2_대공종, HOW3_작업명, HOW4_품명, HOW5_규격, HOW6_세부작업명, R1_단위, R2_수량, R3_재료비_단가, R4_노무비_단가, R5_경비_단가, R6_합계_단가, R7_재료비_금액, R8_노무비_금액, R9_경비_금액, R10_합계_금액
    return (
        code, "인천소방학교", where2, "", how1, how2, "", how4, how5, "", 
        r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, source
    )

def process_arch():
    file_path = os.path.join(RAW_DATA_DIR, "건축내역서_인천소방학교.xlsx")
    if not os.path.exists(file_path): return []
    df = pd.read_excel(file_path, header=None, skiprows=2)
    data = []
    current_how2 = "건축일반"
    for _, row in df.iterrows():
        how4 = clean_val(row[0])
        if not how4: continue
        
        how5 = clean_val(row[1])
        r1 = clean_val(row[2])
        r2 = clean_num(row[3])
        r3 = clean_num(row[4])
        r7 = clean_num(row[5])
        r4 = clean_num(row[6])
        r8 = clean_num(row[7])
        r5 = clean_num(row[8])
        r9 = clean_num(row[9])
        r6 = clean_num(row[10])
        r10 = clean_num(row[11])
        
        if r2 == 0 and r10 == 0: 
            if r1 == '': current_how2 = how4
            continue
            
        data.append(build_row("건축 공사", current_how2, how4, how5, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, '건축내역서_인천소방학교.xlsx'))
    return data

def process_landscaping():
    file_path = os.path.join(RAW_DATA_DIR, "조경내역서_인천소방학교.xlsx")
    if not os.path.exists(file_path): return []
    df = pd.read_excel(file_path, header=None, skiprows=2)
    data = []
    current_how2 = "조경일반"
    for _, row in df.iterrows():
        how4 = clean_val(row[0])
        if not how4: continue
        
        how5 = clean_val(row[1])
        r2 = clean_num(row[2])
        r1 = clean_val(row[3])
        r3 = clean_num(row[4])
        r7 = clean_num(row[5])
        r4 = clean_num(row[6])
        r8 = clean_num(row[7])
        r5 = clean_num(row[8])
        r9 = clean_num(row[9])
        r6 = clean_num(row[10])
        r10 = clean_num(row[11])
        
        if r2 == 0 and r10 == 0:
            if r1 == '': current_how2 = how4
            continue
            
        data.append(build_row("조경 공사", current_how2, how4, how5, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, '조경내역서_인천소방학교.xlsx'))
    return data

def get_mech_how1(name, spec):
    text = name + " " + spec
    if any(k in text for k in FIRE_KEYWORDS): return "소방 공사"
    if any(k in text for k in ELEC_KEYWORDS): return "전기 공사"
    return "기계설비 공사"

def process_mechanical():
    file_path = os.path.join(RAW_DATA_DIR, "기계내역서_인천소방학교.xlsx")
    if not os.path.exists(file_path): return []
    df = pd.read_excel(file_path, header=None, skiprows=8)
    data = []
    current_how2 = "기계일반"
    for _, row in df.iterrows():
        how4 = clean_val(row[2])
        if not how4: continue
        
        how5 = clean_val(row[3])
        r1 = clean_val(row[4])
        r2 = clean_num(row[5])
        r6 = clean_num(row[6]) # 단가
        r10 = clean_num(row[7]) # 합계금액
        
        # Mechanical usually doesn't detail material/labor in this exact column format, so we assign to total
        r3 = r4 = r5 = r7 = r8 = r9 = 0.0
        
        if r2 == 0 and r10 == 0:
            if r1 == '': current_how2 = how4
            continue
            
        how1 = get_mech_how1(how4, how5)
        
        data.append(build_row(how1, current_how2, how4, how5, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, '기계내역서_인천소방학교.xlsx'))
    return data

def process_civil():
    file_path = os.path.join(RAW_DATA_DIR, "토목내역서_인천소방학교.xlsx")
    if not os.path.exists(file_path): return []
    df = pd.read_excel(file_path, header=None, skiprows=18)
    data = []
    current_how2 = "토목일반"
    for _, row in df.iterrows():
        how4 = clean_val(row[0])
        if not how4: continue
        
        how5 = clean_val(row[1])
        r2 = clean_num(row[2])
        r1 = clean_val(row[3])
        
        r3 = clean_num(row[4])
        r7 = clean_num(row[5])
        r4 = clean_num(row[6])
        r8 = clean_num(row[7])
        r5 = clean_num(row[8])
        r9 = clean_num(row[9])
        r6 = clean_num(row[10])
        r10 = clean_num(row[11])
        
        if r10 == 0:
            r10 = r7 + r8 + r9
        if r6 == 0 and r2 > 0:
            r6 = r10 / r2

        if r2 == 0 and r10 == 0:
            if r1 == '': current_how2 = how4
            continue
            
        data.append(build_row("토목 공사", current_how2, how4, how5, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, '토목내역서_인천소방학교.xlsx'))
    return data

def main():
    print("Extracting and processing standard classification data...")
    all_data = []
    all_data.extend(process_arch())
    all_data.extend(process_landscaping())
    all_data.extend(process_mechanical())
    all_data.extend(process_civil())
    
    print(f"Total items extracted: {len(all_data)}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.executemany("""
        INSERT INTO cost_items (
            code, WHERE1_프로젝트, WHERE2_동, WHERE3_층, HOW1_공사, HOW2_대공종, HOW3_작업명, HOW4_품명, HOW5_규격, HOW6_세부작업명, 
            R1_단위, R2_수량, R3_재료비_단가, R4_노무비_단가, R5_경비_단가, R6_합계_단가, R7_재료비_금액, R8_노무비_금액, R9_경비_금액, R10_합계_금액, source_file
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, all_data)
    
    conn.commit()
    conn.close()
    print("Data successfully loaded.")

if __name__ == "__main__":
    main()
