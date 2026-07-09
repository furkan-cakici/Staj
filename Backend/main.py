from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# DÜZELTİLDİ: Port 5432 yerine 6543 yapıldı.
DB_URL = "postgresql://postgres.qpvovfxrzktgofdbazld:12052014Kepen.@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"

def get_db_connection():
    # PostgreSQL bağlantısını RealDictCursor ile açıyoruz ki veriler doğrudan JSON formatına uygun gelsin
    conn = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
    return conn

def init_db():
    # Sunucu ilk kalktığında tablolar yoksa oluşturmasını garantiye alıyoruz
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQLite'taki AUTOINCREMENT yerine PostgreSQL'de SERIAL kullanılır
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
            title TEXT,
            description TEXT,
            timeAgo TEXT,
            isUrgent INTEGER
        )
    """)
    conn.commit()
    conn.close()

# Uygulama başlarken veritabanını bir kez kontrol et
init_db()

@app.get("/api/menu")
def get_menu():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM yemek_menusu")
    rows = cursor.fetchall()
    conn.close()
    return rows # RealDictCursor otomatik olarak dict formatında döndürür

@app.get("/api/announcements")
def get_announcements():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM duyurular")
    rows = cursor.fetchall()
    conn.close()
    
    # Veritabanındaki isUrgent (1/0) kontrolünü Android için True/False yapıyoruz
    result = []
    for row in rows:
        d = dict(row)
        d["isUrgent"] = bool(d["isUrgent"])
        result.append(d)
    return result

@app.get("/")
def read_root():
    # DÜZELTİLDİ: Git çakışma (merge conflict) işaretleri temizlendi
    return {"message": "Fabrika API Merkezi Bulut Veritabanı (PostgreSQL) ile aktif ve sorunsuz çalışıyor!"}