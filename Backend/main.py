import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Ayarlar
st.set_page_config(page_title="Fabrika Yönetim Paneli", layout="wide")

def get_db_connection():
    conn = sqlite3.connect("fabrika.db")
    conn.row_factory = sqlite3.Row
    return conn

# Yardımcı fonksiyonlar
def bugunun_tarihini_al():
    aylar = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    bugun = datetime.now()
    return f"{bugun.day} {aylar[bugun.month]} {gunler[bugun.weekday()]}"

st.title("🏭 Fabrika Uygulaması Yönetim Merkezi")

tab1, tab2 = st.tabs(["📋 Yemek Menüsü", "📢 Duyurular"])

with tab1:
    st.header("Günün Menüsünü Belirle")
    otomatik_tarih = bugunun_tarihini_al()
    st.info(f"📅 Bugün: **{otomatik_tarih}**")
    
    col1, col2 = st.columns(2)
    with col1:
        corba = st.text_input("🍜 Çorba")
        ana_yemek = st.text_input("🍛 Ana Yemek")
    with col2:
        yan_lezzet = st.text_input("🍚 Yan Lezzet")
        tatli = st.text_input("🍮 Tatlı")
    
    if st.button("Kaydet"):
        if corba and ana_yemek:
            conn = get_db_connection()
            # Önce aynı gün kaydı var mı bak
            conn.execute("INSERT OR REPLACE INTO yemek_menusu (date, soup, mainCourse, sideDish, dessert) VALUES (?, ?, ?, ?, ?)",
                         (otomatik_tarih, corba, ana_yemek, yan_lezzet, tatli))
            conn.commit()
            conn.close()
            st.success("Menü güncellendi!")
            st.rerun()

with tab2:
    st.header("Yeni Duyuru")
    d_baslik = st.text_input("Başlık")
    d_icerik = st.text_area("İçerik")
    d_acil = st.checkbox("🚨 Acil Durum")
    
    if st.button("Yayınla"):
        conn = get_db_connection()
        conn.execute("INSERT INTO duyurular (title, description, timeAgo, isUrgent) VALUES (?, ?, ?, ?)",
                     (d_baslik, d_icerik, datetime.now().strftime("%H:%M"), 1 if d_acil else 0))
        conn.commit()
        conn.close()
        st.success("Duyuru yayınlandı!")
        st.rerun()