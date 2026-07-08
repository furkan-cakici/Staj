import streamlit as st
import sqlite3
import os
import pandas as pd
from datetime import datetime

# Türkçe tarih oluşturma
def bugunun_tarihini_al():
    aylar = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    
    bugun = datetime.now()
    gun_adi = gunler[bugun.weekday()]
    ay_adi = aylar[bugun.month]
    
    return f"{bugun.day} {ay_adi} {gun_adi}"

st.set_page_config(page_title="Fabrika Yönetim Paneli", layout="wide")

st.title("🏭 Fabrika Uygulaması Yönetim Merkezi")
st.write("Yemek menülerini ve duyuruları buradan anlık olarak güncelleyebilirsiniz.")


def get_db_connection():
    # Veritabanı dosyasına doğrudan erişim yerine URI yöntemiyle (daha güvenli) bağlan
    db_path = "file:fabrika.db?mode=rw" 
    conn = sqlite3.connect(db_path, uri=True)
    conn.row_factory = sqlite3.Row
    return conn

st.title("🏭 Fabrika Yönetim Paneli")

tab1, tab2 = st.tabs(["🥘 Yemek Menüsü", "📢 Duyurular"])

# --- YEMEK MENÜSÜ SEKMESİ ---
with tab1:
    st.header("Günün Menüsünü Belirle")
    
    otomatik_tarih = bugunun_tarihini_al()
    st.info(f"📅 Bugünün Tarihi: **{otomatik_tarih}** (Sistemden otomatik çekildi)")
    
    col1, col2 = st.columns(2)
    with col1:
        corba = st.text_input("🍜 Çorba")
        ana_yemek = st.text_input("🍛 Ana Yemek")
    with col2:
        yan_lezzet = st.text_input("🍚 Yan Lezzet")
        tatli = st.text_input("🍮 Tatlı")
    
    if st.button("Bugünün Menüsünü Kaydet ve Eskileri Temizle"):
        if corba and ana_yemek:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM yemek_menusu WHERE date != ?", (otomatik_tarih,))
            
            cursor.execute("SELECT id FROM yemek_menusu WHERE date = ?", (otomatik_tarih,))
            mevcut_menu = cursor.fetchone()
            
            if mevcut_menu:
                cursor.execute("""
                    UPDATE yemek_menusu 
                    SET soup = ?, mainCourse = ?, sideDish = ?, dessert = ?
                    WHERE date = ?
                """, (corba, ana_yemek, yan_lezzet, tatli, otomatik_tarih))
                st.success("Bugünün menüsü güncellendi!")
            else:
                cursor.execute("""
                    INSERT INTO yemek_menusu (date, soup, mainCourse, sideDish, dessert)
                    VALUES (?, ?, ?, ?, ?)
                """, (otomatik_tarih, corba, ana_yemek, yan_lezzet, tatli))
                st.success("Bugünün menüsü başarıyla eklendi ve eski günler silindi!")
                
            conn.commit()
            conn.close()
        else:
            st.error("Lütfen en azından Çorba ve Ana Yemek alanlarını doldurun.")

    st.markdown("---")
    st.subheader("Sistemde Kayıtlı Güncel Menü")
    
    conn = get_db_connection()
    menuler_df = pd.read_sql_query("SELECT date, soup, mainCourse, sideDish, dessert FROM yemek_menusu", conn)
    conn.close()
    
    if not menuler_df.empty:
        st.dataframe(menuler_df, use_container_width=True)
    else:
        st.warning("Veritabanında henüz kayıtlı menü bulunmuyor.")

# --- DUYURU SEKMESİ ---
with tab2:
    st.header("Yeni Duyuru Yayınla")
    
    d_baslik = st.text_input("📢 Duyuru Başlığı")
    d_icerik = st.text_area("📝 Duyuru İçeriği")
    # ZAMAN INPUTUNU TAMAMEN KALDIRDIK
    d_acil = st.checkbox("🚨 Bu acil/kritik bir duyurudur (Kart kırmızı görünsün)")
    
    if st.button("Duyuruyu Yayınla"):
        if d_baslik and d_icerik:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Yayınla butonuna basıldığı anın saatini ve tarihini yakalıyoruz
            su_an = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute("""
                INSERT INTO duyurular (title, description, timeAgo, isUrgent)
                VALUES (?, ?, ?, ?)
            """, (d_baslik, d_icerik, su_an, 1 if d_acil else 0)) # su_an değişkenini kaydettik
            
            conn.commit()
            conn.close()
            st.success("Duyuru panoda başarıyla canlıya alındı!")
            st.rerun()
        else:
            st.error("Lütfen Başlık ve İçerik alanlarını boş bırakmayın.")
                
    st.markdown("---")
    
    # --- TEKLİ DUYURU SİLME ALANI ---
    st.subheader("🗑️ İstediğin Duyuruyu Sil")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    # Veritabanından duyuruların ID'sini ve başlığını çekiyoruz
    cursor.execute("SELECT id, title, timeAgo FROM duyurular")
    mevcut_duyurular = cursor.fetchall()
    
    if mevcut_duyurular:
        # Açılır menüde düzgün görünmesi için bir sözlük (dictionary) oluşturuyoruz
        # Format: "1 - Yemekhane Kapalı (Dün)"
        duyuru_secenekleri = {f"{d['id']} - {d['title']} ({d['timeAgo']})": d['id'] for d in mevcut_duyurular}
        
        col_secim, col_buton = st.columns([4, 1])
        with col_secim:
            secilen_duyuru = st.selectbox("Silmek istediğiniz duyuruyu seçin:", list(duyuru_secenekleri.keys()))
        
        with col_buton:
            # Butonu biraz aşağı hizalamak için boşluk bırakıyoruz
            st.write("") 
            st.write("")
            if st.button("Seçili Duyuruyu Sil", type="primary"):
                silinecek_id = duyuru_secenekleri[secilen_duyuru]
                cursor.execute("DELETE FROM duyurular WHERE id = ?", (silinecek_id,))
                conn.commit()
                st.success("Duyuru başarıyla silindi!")
                st.rerun() # Sayfayı yenileyip tablonun temiz halini gösterir
    else:
        st.info("Sistemde silinecek bir duyuru bulunmuyor.")
    conn.close()

    st.markdown("---")
    st.subheader("Aktif Duyurular")
    
    conn = get_db_connection()
    duyurular_df = pd.read_sql_query("SELECT id, title, description, timeAgo, isUrgent FROM duyurular", conn)
    conn.close()
    
    if not duyurular_df.empty:
        duyurular_df["isUrgent"] = duyurular_df["isUrgent"].map({1: "🔴 Acil", 0: "⚪ Standart"})
        # Tabloda ID'yi index olarak ayarlayalım ki daha şık dursun
        st.dataframe(duyurular_df.set_index('id'), use_container_width=True)
    else:
        st.info("Şu an aktif bir duyuru bulunmuyor.")
        