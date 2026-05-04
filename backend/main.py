from fastapi import FastAPI, Query, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import sqlite3
import os
import io
import csv

app = FastAPI(title="인천소방학교 내역서 API (표준분류체계)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "project_costs.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/items")
def search_items(
    q: Optional[str] = None,
    category: Optional[str] = None,
    building: Optional[str] = None,
    page: int = 1,
    limit: int = 50
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM cost_items WHERE 1=1"
    params = []
    
    if q:
        query += " AND (HOW4_품명 LIKE ? OR HOW5_규격 LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])
    if category:
        query += " AND HOW1_공사 = ?"
        params.append(category)
    if building:
        query += " AND WHERE2_동 = ?"
        params.append(building)
        
    # Count total
    count_query = query.replace("SELECT *", "SELECT COUNT(*)")
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    # Pagination
    offset = (page - 1) * limit
    query += " ORDER BY id LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": [dict(row) for row in rows]
    }

@app.get("/api/summary")
def get_summary(
    q: Optional[str] = None,
    category: Optional[str] = None,
    building: Optional[str] = None
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT HOW1_공사 as category, SUM(R10_합계_금액) as total FROM cost_items WHERE 1=1"
    params = []
    
    if q:
        query += " AND (HOW4_품명 LIKE ? OR HOW5_규격 LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])
    if category:
        query += " AND HOW1_공사 = ?"
        params.append(category)
    if building:
        query += " AND WHERE2_동 = ?"
        params.append(building)
        
    query += " GROUP BY HOW1_공사"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

@app.get("/api/export")
def export_csv(
    q: Optional[str] = None,
    category: Optional[str] = None,
    building: Optional[str] = None
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM cost_items WHERE 1=1"
    params = []
    
    if q:
        query += " AND (HOW4_품명 LIKE ? OR HOW5_규격 LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])
    if category:
        query += " AND HOW1_공사 = ?"
        params.append(category)
    if building:
        query += " AND WHERE2_동 = ?"
        params.append(building)
    
    query += " ORDER BY id"
    cursor.execute(query, params)
    
    output = io.StringIO()
    # Add BOM for Excel compatibility in Korean
    output.write('\ufeff')
    writer = csv.writer(output)
    
    # Headers
    headers = [
        "ID", "코드", "프로젝트", "동", "층", "공사", "대공종", "작업명", "품명", "규격",
        "세부작업명", "단위", "수량", "재료비_단가", "노무비_단가", "경비_단가", "합계_단가",
        "재료비_금액", "노무비_금액", "경비_금액", "합계_금액", "출처파일"
    ]
    writer.writerow(headers)
    
    for row in cursor:
        writer.writerow(row)
    
    conn.close()
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=incheon_school_cost.csv"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
