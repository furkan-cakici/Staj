import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- AYARLAR ---
st.set_page_config(page_title="Fabrika Yönetim Paneli", layout="wide", page_icon="🏭")

def get_db_connection():
    # Streamlit'te thread çakışmalarını önlemek için check_same_thread=False eklendi
    conn = sqlite3.connect("fabrika.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# --- YARDIMCI FONKSİYONLAR ---
def bugunun_tarihini_al():
    aylar = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    bugun = datetime.now()
    return f"{bugun.day} {aylar[bugun.month]} {gunler[bugun.weekday()]}"

# --- ARAYÜZ ---
st.title("🏭 Fabrika Uygulaması Yönetim Merkezi")
st.markdown("Yemek menülerini ve duyuruları buradan anlık olarak yönetebilirsiniz.")

tab1, tab2 = st.tabs(["📋 Yemek Menüsü", "📢 Duyurular"])

# ==========================================
# 1. SEKME: YEMEK MENÜSÜ YÖNETİMİ
# ==========================================
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
    
    if st.button("Menüyü Kaydet / Güncelle", type="primary"):
        if corba and ana_yemek:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                
                # Önce bugünün tarihiyle kayıt var mı kontrol et
                cursor.execute("SELECT id FROM yemek_menusu WHERE date = ?", (otomatik_tarih,))
                kayit = cursor.fetchone()
                
                if kayit:
                    # Varsa güncelle
                    cursor.execute("""
                        UPDATE yemek_menusu 
                        SET soup = ?, mainCourse = ?, sideDish = ?, dessert = ?
                        WHERE date = ?
                    """, (corba, ana_yemek, yan_lezzet, tatli, otomatik_tarih))
                else:
                    # Yoksa yeni ekle
                    cursor.execute("""
                        INSERT INTO yemek_menusu (date, soup, mainCourse, sideDish, dessert) 
                        VALUES (?, ?, ?, ?, ?)
                    """, (otomatik_tarih, corba, ana_yemek, yan_lezzet, tatli))
                
                conn.commit()
                st.success("Menü başarıyla kaydedildi!")
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
            finally:
                conn.close()
        else:
            st.warning("Lütfen en azından Çorba ve Ana Yemek alanlarını doldurun.")

    st.divider()
    st.subheader("Sistemdeki Kayıtlı Menüler")
    try:
        conn = get_db_connection()
        df_menu = pd.read_sql_query("SELECT * FROM yemek_menusu", conn)
        conn.close()
        if not df_menu.empty:
            st.dataframe(df_menu, use_container_width=True, hide_index=True)
        else:
            st.info("Henüz kayıtlı bir menü bulunmuyor.")
    except Exception:
        st.error("Veritabanından menüler okunamadı. Tablo henüz oluşturulmamış olabilir.")


# ==========================================
# 2. SEKME: DUYURU YÖNETİMİ
# ==========================================
with tab2:
    st.header("Yeni Duyuru Yayınla")
    d_baslik = st.text_input("Başlık")
    d_icerik = st.text_area("İçerik")
    d_acil = st.checkbox("🚨 Acil Durum (Kırmızı Etiket)")
    
    if st.button("Duyuruyu Yayınla", type="primary"):
        if d_baslik and d_icerik:
            try:
                conn = get_db_connection()
                saat = datetime.now().strftime("%H:%M")
                conn.execute("""
                    INSERT INTO duyurular (title, description, timeAgo, isUrgent) 
                    VALUES (?, ?, ?, ?)
                """, (d_baslik, d_icerik, saat, 1 if d_acil else 0))
                conn.commit()
                st.success("Duyuru başarıyla yayınlandı!")
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
            finally:
                conn.close()
        else:
            st.warning("Lütfen başlık ve içerik alanlarını boş bırakmayın.")

    st.divider()
    st.subheader("Aktif Duyurular")
    try:
        conn = get_db_connection()
        df_duyuru = pd.read_sql_query("SELECT id, title, description, timeAgo, isUrgent FROM duyurular", conn)
        conn.close()
        
        if not df_duyuru.empty:
            # 1 ve 0 değerlerini kullanıcı dostu metinlere çeviriyoruz
            df_duyuru['isUrgent'] = df_duyuru['isUrgent'].apply(lambda x: "Evet 🚨" if x == 1 else "Hayır")
            st.dataframe(df_duyuru, use_container_width=True, hide_index=True)
        else:
            st.info("Sistemde aktif duyuru bulunmuyor.")
    except Exception:
        st.error("Veritabanından duyurular okunamadı. Tablo henüz oluşturulmamış olabilir.")