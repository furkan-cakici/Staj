import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from datetime import datetime

# --- AYARLAR ---
st.set_page_config(page_title="Fabrika Yönetim Paneli", layout="wide", page_icon="🏭")

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
            title TEXT,
            description TEXT,
            timeAgo TEXT,
            isUrgent INTEGER
        )
    """)
    conn.commit()
    conn.close()

try:
    init_db()
except Exception as e:
    st.error(f"Veritabanı bağlantı hatası: {e}")

def bugunun_tarihini_al():
    aylar = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    bugun = datetime.now()
    return f"{bugun.day} {aylar[bugun.month]} {gunler[bugun.weekday()]}"

st.title("🏭 Fabrika Uygulaması Yönetim Merkezi")
st.markdown("Yemek menülerini ve duyuruları buradan anlık olarak yönetebilirsiniz.")

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
    
    if st.button("Menüyü Kaydet / Güncelle", type="primary"):
        if corba and ana_yemek:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM yemek_menusu WHERE date = %s", (otomatik_tarih,))
                kayit = cursor.fetchone()
                
                if kayit:
                    cursor.execute("""
                        UPDATE yemek_menusu 
                        SET soup = %s, maincourse = %s, sidedish = %s, dessert = %s
                        WHERE date = %s
                    """, (corba, ana_yemek, yan_lezzet, tatli, otomatik_tarih))
                else:
                    cursor.execute("""
                        INSERT INTO yemek_menusu (date, soup, mainCourse, sideDish, dessert) 
                        VALUES (%s, %s, %s, %s, %s)
                    """, (otomatik_tarih, corba, ana_yemek, yan_lezzet, tatli))
                
                conn.commit()
                st.success("Menü başarıyla kaydedildi!")
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
            finally:
                conn.close()
            st.rerun()
        else:
            st.warning("Lütfen en azından Çorba ve Ana Yemek alanlarını doldurun.")

    st.divider()
    st.subheader("Sistemdeki Kayıtlı Menüler")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # ID KALDIRILDI
        cursor.execute('SELECT date, soup, maincourse AS "mainCourse", sidedish AS "sideDish", dessert FROM yemek_menusu')
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            df_menu = pd.DataFrame(rows)
            df_menu = df_menu.fillna("") 
            st.dataframe(df_menu, use_container_width=True, hide_index=True)
        else:
            st.info("Henüz kayıtlı bir menü bulunmuyor.")
    except Exception as e:
        st.error(f"Kayıtlar okunamadı: {e}")

with tab2:
    st.header("Yeni Duyuru Yayınla")
    d_baslik = st.text_input("Başlık")
    d_icerik = st.text_area("İçerik")
    d_acil = st.checkbox("🚨 Acil Durum (Kırmızı Etiket)")
    
    if st.button("Duyuruyu Yayınla", type="primary"):
        if d_baslik and d_icerik:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                saat = datetime.now().strftime("%H:%M")
                
                cursor.execute("""
                    INSERT INTO duyurular (title, description, timeAgo, isUrgent) 
                    VALUES (%s, %s, %s, %s)
                """, (d_baslik, d_icerik, saat, 1 if d_acil else 0))
                
                conn.commit()
                st.success("Duyuru başarıyla yayınlandı!")
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
            finally:
                conn.close()
            st.rerun()
        else:
            st.warning("Lütfen başlık ve içerik alanlarını boş bırakmayın.")

    st.divider()
    
    col_sil, col_sifirla = st.columns(2)
    
    with col_sil:
        st.subheader("🗑️ İstediğin Duyuruyu Sil")
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, timeago AS "timeAgo" FROM duyurular')
            mevcut_duyurular = cursor.fetchall()
            
            if mevcut_duyurular:
                duyuru_secenekleri = {f"{d['id']} - {d['title']} ({d['timeAgo']})": d['id'] for d in mevcut_duyurular}
                secilen_duyuru = st.selectbox("Silmek istediğiniz duyuruyu seçin:", list(duyuru_secenekleri.keys()))
                
                if st.button("Seçili Duyuruyu Sil"):
                    silinecek_id = duyuru_secenekleri[secilen_duyuru]
                    cursor.execute("DELETE FROM duyurular WHERE id = %s", (silinecek_id,))
                    conn.commit()
                    st.success("Duyuru başarıyla silindi!")
                    st.rerun()
            else:
                st.info("Sistemde silinecek bir duyuru bulunmuyor.")
        except Exception as e:
            st.error(f"Duyurular yüklenirken hata oluştu: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

    # --- SIFIRLAMA BÖLÜMÜ (YENİ) ---
    with col_sifirla:
        st.subheader("🧹 Gün Sonu: Tüm Duyuruları Sıfırla")
        st.info("Bu buton dünün tüm duyurularını kalıcı olarak siler ve ID sayacını yeni gün için tekrar 1'e döndürür.")
        if st.button("Sistemi Sıfırla (Tam Temizlik)", type="primary"):
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                # TRUNCATE komutu tabloyu komple siler, RESTART IDENTITY ise sayacı 1'e döndürür.
                cursor.execute("TRUNCATE TABLE duyurular RESTART IDENTITY")
                conn.commit()
                st.success("Tüm duyurular temizlendi, ID sayacı 1'den başlatıldı!")
                st.rerun()
            except Exception as e:
                st.error(f"Sıfırlama hatası: {e}")
            finally:
                conn.close()

    st.divider()
    st.subheader("Aktif Duyurular")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, description, timeago AS "timeAgo", isurgent AS "isUrgent" FROM duyurular')
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            df_duyuru = pd.DataFrame(rows)
            # Veritabanındaki ID'yi gizleyip, görsel olarak 1, 2, 3 diye satır numarası atıyoruz
            df_duyuru = df_duyuru.drop(columns=['id']) 
            df_duyuru.index = df_duyuru.index + 1
            
            df_duyuru = df_duyuru.fillna("")
            df_duyuru['isUrgent'] = df_duyuru['isUrgent'].apply(lambda x: "Evet 🚨" if x == 1 else "Hayır")
            # hide_index=False yaptık ki atadığımız 1, 2, 3 numaraları ekranda görünsün
            st.dataframe(df_duyuru, use_container_width=True, hide_index=False)
        else:
            st.info("Sistemde aktif duyuru bulunmuyor.")
    except Exception as e:
        st.error(f"Kayıtlar okunamadı: {e}")