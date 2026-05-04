import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "project_costs.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Drop existing table to migrate to the new schema
    cursor.execute("DROP TABLE IF EXISTS cost_items")
    
    cursor.execute("""
        CREATE TABLE cost_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT,
            WHERE1_프로젝트 TEXT,
            WHERE2_동 TEXT,
            WHERE3_층 TEXT,
            HOW1_공사 TEXT,
            HOW2_대공종 TEXT,
            HOW3_작업명 TEXT,
            HOW4_품명 TEXT,
            HOW5_규격 TEXT,
            HOW6_세부작업명 TEXT,
            R1_단위 TEXT,
            R2_수량 REAL,
            R3_재료비_단가 REAL,
            R4_노무비_단가 REAL,
            R5_경비_단가 REAL,
            R6_합계_단가 REAL,
            R7_재료비_금액 REAL,
            R8_노무비_금액 REAL,
            R9_경비_금액 REAL,
            R10_합계_금액 REAL,
            source_file TEXT
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized with standard classification schema.")
