from fastapi import FastAPI
import sqlite3

app = FastAPI()

def get_db_connection():
    # check_same_thread=False ile aynı anda hem senin panelden hem telefondan istek gelirse kilitlenmeyi önlüyoruz
    conn = sqlite3.connect("fabrika.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Sunucu ilk kalktığında tablolar yoksa oluşturmasını garantiye alıyoruz
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS yemek_menusu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            soup TEXT,
            mainCourse TEXT,
            sideDish TEXT,
            dessert TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS duyurular (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    return [dict(row) for row in rows]

@app.get("/api/announcements")
def get_announcements():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM duyurular")
    rows = cursor.fetchall()
    conn.close()
    
    # SQLite'ta boolean olmadığı için 1/0 kontrolünü True/False yapıyoruz
    result = []
    for row in rows:
        d = dict(row)
        d["isUrgent"] = bool(d["isUrgent"])
        result.append(d)
    return result

@app.get("/")
def read_root():
    return {"message": "Fabrika API aktif ve sorunsuz çalışıyor!"}