from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

DB_URL = "postgresql://postgres.qpvovfxrzktgofdbazld:12052014Kepen.@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"

def get_db_connection():
    conn = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS yemek_menusu (
            id SERIAL PRIMARY KEY,
            date TEXT,
            soup TEXT,
            mainCourse TEXT,
            sideDish TEXT,
            dessert TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS duyurular (
            id SERIAL PRIMARY KEY,
            title SERIAL PRIMARY KEY,
            title TEXT,
            description TEXT,
            timeAgo TEXT,
            isUrgent INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.get("/api/menu")
def get_menu():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM yemek_menusu")
    rows = cursor.fetchall()
    conn.close()
    
    # --- NULL TEMİZLEME FİLTRESİ ---
    result = []
    for row in rows:
        d = dict(row)
        for key, value in d.items():
            if value is None:
                d[key] = "" # Android ekranda null görmesin diye boş string yapıyoruz
        result.append(d)
    return result

@app.get("/api/announcements")
def get_announcements():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM duyurular")
    rows = cursor.fetchall()
    conn.close()
    
    # --- NULL TEMİZLEME FİLTRESİ ---
    result = []
    for row in rows:
        d = dict(row)
        for key, value in d.items():
            if value is None:
                d[key] = ""
        d["isUrgent"] = bool(d.get("isUrgent", 0))
        result.append(d)
    return result

@app.get("/")
def read_root():
    return {"message": "Fabrika API Merkezi Bulut Veritabanı (PostgreSQL) ile aktif ve sorunsuz çalışıyor!"}