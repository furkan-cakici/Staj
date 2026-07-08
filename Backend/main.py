from fastapi import FastAPI
import sqlite3

app = FastAPI()

def init_db():
    conn = sqlite3.connect("fabrika.db")
    cursor = conn.cursor()
    
    # Yemek Menüsü Tablosu
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
    
    # Duyurular Tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS duyurular (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            timeAgo TEXT,
            isUrgent INTEGER
        )
    """)
    
    # Örnek test verileri (Eğer tablolar boşsa eklenir)
    cursor.execute("SELECT COUNT(*) FROM yemek_menusu")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO yemek_menusu (date, soup, mainCourse, sideDish, dessert) VALUES (?, ?, ?, ?, ?)",
                       ("15 Nisan Salı", "Mercimek Çorbası", "Karnıyarık", "Pirinç Pilavı", "Sütlaç"))
        cursor.execute("INSERT INTO duyurular (title, description, timeAgo, isUrgent) VALUES (?, ?, ?, ?)",
                       ("Bakım Çalışması", "Yarın saat 10:00'da atölye A'da altyapı çalışması olacaktır.", "1 Saat Önce", 1))
        conn.commit()
    conn.close()

init_db()

@app.get("/api/menu")
def get_menu():
    conn = sqlite3.connect("fabrika.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM yemek_menusu")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/api/announcements")
def get_announcements():
    conn = sqlite3.connect("fabrika.db")
    conn.row_factory = sqlite3.Row
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