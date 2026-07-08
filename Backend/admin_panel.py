import streamlit as st
import sqlite3
import os

def get_db_connection():
    # Streamlit Backend klasöründe çalıştığı için fabrika.db doğrudan bulunur
    db_path = "fabrika.db" 
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

st.title("🏭 Fabrika Yönetim Paneli")

tab1, tab2 = st.tabs(["🥘 Yemek Menüsü", "📢 Duyurular"])

with tab1:
    st.header("Yemek Ekle")
    tarih = st.text_input("Tarih")
    ana_yemek = st.text_input("Ana Yemek")
    if st.button("Kaydet", key="yemek"):
        conn = get_db_connection()
        conn.execute("INSERT INTO yemek_menusu (date, mainCourse) VALUES (?, ?)", (tarih, ana_yemek))
        conn.commit()
        conn.close()
        st.success("Yemek başarıyla eklendi!")

with tab2:
    st.header("Duyuru Ekle")
    baslik = st.text_input("Duyuru Başlığı")
    icerik = st.text_area("İçerik")
    if st.button("Duyuruyu Yayınla", key="duyuru"):
        conn = get_db_connection()
        conn.execute("INSERT INTO duyurular (title, description, timeAgo, isUrgent) VALUES (?, ?, 'Az önce', 0)", (baslik, icerik))
        conn.commit()
        conn.close()
        st.success("Duyuru paylaşıldı!")

        