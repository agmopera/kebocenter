import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_NAME = os.path.join(BASE_DIR, "siparis.db")


def connect_database():
    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = connect_database()
    cursor = conn.cursor()

    

    # ======================================
    # ŞUBELER TABLOSU
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subeler(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    sube_adi TEXT,
    kullanici_adi TEXT,
    sifre TEXT,
    yetkili TEXT,
    telefon TEXT,
    eposta TEXT,
    il TEXT,
    ilce TEXT,
    adres TEXT,

    durum TEXT,

    uretim_gunu TEXT,
    sevkiyat_gunu TEXT,
    sevkiyat_saati TEXT,
    teslim_suresi TEXT

)
    """)
# BURAYA GELECEK
    try:
        cursor.execute("ALTER TABLE subeler ADD COLUMN uretim_gunu TEXT")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE subeler ADD COLUMN sevkiyat_gunu TEXT")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE subeler ADD COLUMN sevkiyat_saati TEXT")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE subeler ADD COLUMN teslim_suresi TEXT")
    except:
        pass
        
    
    # ======================================
    # ÜRÜNLER TABLOSU
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urunler(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            urun_kodu TEXT NOT NULL UNIQUE,

            urun_adi TEXT NOT NULL,

            kategori TEXT,

            birim TEXT,

            durum TEXT

        )
    """)

    # Yeni alanlar (eski veritabanı için)
    try:
        cursor.execute("""
            ALTER TABLE urunler
            ADD COLUMN palet_kapasitesi INTEGER DEFAULT 0
        """)
    except:
        pass

    try:
        cursor.execute("""
            ALTER TABLE urunler
            ADD COLUMN urun_tipi TEXT DEFAULT 'Donuk'
        """)
    except:
        pass

    try:
        cursor.execute("""
            ALTER TABLE urunler
            ADD COLUMN koli_agirligi REAL DEFAULT 0
        """)
    except:
        pass

    # ======================================
    # SİPARİŞLER TABLOSU
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS siparisler(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            siparis_no TEXT UNIQUE,

            sube_id INTEGER,

            tarih TEXT,

            durum TEXT,

            FOREIGN KEY(sube_id) REFERENCES subeler(id)

        )
    """)


    # ======================================
    # SİPARİŞ DETAY TABLOSU
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS siparis_detay(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            siparis_id INTEGER,

            urun_id INTEGER,

            miktar REAL,

            FOREIGN KEY(siparis_id) REFERENCES siparisler(id),

            FOREIGN KEY(urun_id) REFERENCES urunler(id)

        )
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS siparis_gecmisi(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    siparis_id INTEGER,

    tarih TEXT,

    kullanici TEXT,

    eski_durum TEXT,

    yeni_durum TEXT

)
""")

    conn.commit()
    conn.close()



# ==================================================
# ŞUBELER
# ==================================================

def add_sube(
    sube_adi,
    kullanici_adi,
    sifre,
    yetkili,
    telefon,
    eposta,
    il,
    ilce,
    adres,
    durum,
    uretim_gunu,
    sevkiyat_gunu,
    sevkiyat_saati,
    teslim_suresi
):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO subeler
        (
            sube_adi,
            kullanici_adi,
            sifre,
            yetkili,
            telefon,
            eposta,
            il,
            ilce,
            adres,
            durum,
            uretim_gunu,
            sevkiyat_gunu,
            sevkiyat_saati,
            teslim_suresi
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        sube_adi,
        kullanici_adi,
        sifre,
        yetkili,
        telefon,
        eposta,
        il,
        ilce,
        adres,
        durum,
        uretim_gunu,
        sevkiyat_gunu,
        sevkiyat_saati,
        teslim_suresi
    ))

    conn.commit()
    conn.close()


def get_subeler():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            sube_adi,
            kullanici_adi,
            sifre,
            yetkili,
            telefon,
            eposta,
            il,
            ilce,
            adres,
            durum,
            uretim_gunu,
            sevkiyat_gunu,
            sevkiyat_saati,
            teslim_suresi
        FROM subeler
        ORDER BY sube_adi
    """)

    sonuc = cursor.fetchall()

    conn.close()

    return sonuc



def get_sube(id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            sube_adi,
            kullanici_adi,
            sifre,
            yetkili,
            telefon,
            eposta,
            il,
            ilce,
            adres,
            durum,
            uretim_gunu,
            sevkiyat_gunu,
            sevkiyat_saati,
            teslim_suresi
        FROM subeler
        WHERE id=?
    """, (id,))

    sonuc = cursor.fetchone()

    conn.close()

    return sonuc



def update_sube(
    id,
    sube_adi,
    kullanici_adi,
    sifre,
    yetkili,
    telefon,
    eposta,
    il,
    ilce,
    adres,
    durum,
    uretim_gunu,
    sevkiyat_gunu,
    sevkiyat_saati,
    teslim_suresi
):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE subeler
        SET
            sube_adi=?,
            kullanici_adi=?,
            sifre=?,
            yetkili=?,
            telefon=?,
            eposta=?,
            il=?,
            ilce=?,
            adres=?,
            durum=?,
            uretim_gunu=?,
            sevkiyat_gunu=?,
            sevkiyat_saati=?,
            teslim_suresi=?
        WHERE id=?
    """, (
        sube_adi,
        kullanici_adi,
        sifre,
        yetkili,
        telefon,
        eposta,
        il,
        ilce,
        adres,
        durum,
        uretim_gunu,
        sevkiyat_gunu,
        sevkiyat_saati,
        teslim_suresi,
        id
    ))

    conn.commit()
    conn.close()

def delete_sube(id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM subeler
        WHERE id=?
    """, (id,))

    conn.commit()
    conn.close()

# ==================================================
# SİPARİŞLER
# ==================================================

def add_siparis(siparis_no, sube_id, tarih, durum):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO siparisler
        (siparis_no, sube_id, tarih, durum)
        VALUES (?, ?, ?, ?)
    """, (
        siparis_no,
        sube_id,
        tarih,
        durum
    ))

    siparis_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return siparis_id


def add_siparis_detay(siparis_id, urun_id, miktar):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO siparis_detay
        (siparis_id, urun_id, miktar)
        VALUES (?, ?, ?)
    """, (
        siparis_id,
        urun_id,
        miktar
    ))

    conn.commit()
    conn.close()


def get_siparisler():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            s.id,
            s.siparis_no,
            sb.sube_adi,
            s.tarih,
            s.durum

        FROM siparisler s

        INNER JOIN subeler sb

        ON s.sube_id = sb.id

        ORDER BY s.id DESC
    """)

    sonuc = cursor.fetchall()

    conn.close()

    return sonuc


    conn.commit()
    conn.close()

def get_onay_bekleyen_siparisler():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            s.id,
            s.siparis_no,
            sb.sube_adi,
            s.tarih,
            s.durum

        FROM siparisler s

        INNER JOIN subeler sb

        ON s.sube_id = sb.id

        WHERE s.durum='Hazırlandı'

        ORDER BY s.id DESC

    """)

    sonuc = cursor.fetchall()

    conn.close()

    return sonuc


def get_sube_siparisleri(sube_id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            siparisler.id,
            siparisler.siparis_no,
            subeler.sube_adi,
            siparisler.tarih,
            siparisler.durum
        FROM siparisler
        INNER JOIN subeler
            ON siparisler.sube_id = subeler.id
        WHERE siparisler.sube_id = ?
        ORDER BY siparisler.id DESC
    """, (sube_id,))

    sonuc = cursor.fetchall()

    conn.close()

    return sonuc


# ==================================================
# ÜRÜNLER
# ==================================================

def add_urun(
    urun_kodu,
    urun_adi,
    kategori,
    birim,
    durum,
    palet_kapasitesi,
    urun_tipi,
    koli_agirligi
):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
       INSERT INTO urunler
(
    urun_kodu,
    urun_adi,
    kategori,
    birim,
    durum,
    palet_kapasitesi,
    urun_tipi,
    koli_agirligi
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
    urun_kodu,
    urun_adi,
    kategori,
    birim,
    durum,
    palet_kapasitesi,
    urun_tipi,
    koli_agirligi
))

    conn.commit()
    conn.close()


def get_urunler():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            urun_kodu,
            urun_adi,
            kategori,
            birim,
            durum,
            palet_kapasitesi,
            urun_tipi,
            koli_agirligi
        FROM urunler
        ORDER BY urun_adi
    """)

    sonuc = cursor.fetchall()

    conn.close()

    return sonuc


def get_urun(id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM urunler
        WHERE id=?
    """, (id,))

    sonuc = cursor.fetchone()

    conn.close()

    return sonuc


def update_urun(id, urun_kodu, urun_adi, kategori, birim,palet_kapasitesi,urun_tipi,koli_agirligi, durum):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE urunler
        SET
            urun_kodu=?,
            urun_adi=?,
            kategori=?,
            birim=?,
            durum=?
            palet_kapasitesi=?,
            urun_tipi=?,
            koli_agirligi=?,
        WHERE id=?
    """, (
        urun_kodu,
        urun_adi,
        kategori,
        birim,
        durum,
        id
    ))

    conn.commit()
    conn.close()


def delete_urun(id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM urunler
        WHERE id=?
    """, (id,))

    conn.commit()
    conn.close()

# ==================================================
# SİPARİŞ DETAY
# ==================================================

def get_siparis(id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            s.id,
            s.siparis_no,
            sb.sube_adi,
            s.tarih,
            s.durum

        FROM siparisler s

        INNER JOIN subeler sb
            ON s.sube_id = sb.id

        WHERE s.id=?

    """, (id,))

    sonuc = cursor.fetchone()

    conn.close()

    return sonuc


def get_siparis_detaylari(siparis_id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            d.id,
            d.urun_id,
            u.urun_adi,
            d.miktar

        FROM siparis_detay d

        INNER JOIN urunler u
            ON d.urun_id = u.id

        WHERE d.siparis_id = ?

        ORDER BY u.urun_adi

    """, (siparis_id,))

    sonuc = cursor.fetchall()

    conn.close()

    return sonuc
    
def delete_siparis(id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM siparis_detay
        WHERE siparis_id=?
    """, (id,))

    cursor.execute("""
        DELETE FROM siparisler
        WHERE id=?
    """, (id,))

    conn.commit()
    conn.close()

def update_siparis(id, sube_id, tarih, durum):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE siparisler
        SET
            sube_id=?,
            tarih=?,
            durum=?
        WHERE id=?
    """, (
        sube_id,
        tarih,
        durum,
        id
    ))

    conn.commit()
    conn.close()


def update_siparis_detay(id, miktar):

    conn = connect_database()
    cursor = conn.cursor()


    cursor.execute("""
        UPDATE siparis_detay

        SET miktar=?

        WHERE id=?

    """,(
        miktar,
        id
    ))


    conn.commit()

    conn.close()

def siparis_durum_guncelle(id, durum):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE siparisler
        SET durum=?
        WHERE id=?
    """,(
        durum,
        id
    ))

    conn.commit()
    conn.close()



def delete_siparis_detay(id):

    conn = connect_database()
    cursor = conn.cursor()


    cursor.execute("""
        DELETE FROM siparis_detay

        WHERE id=?

    """,(id,))
    
    conn.commit()
    conn.close()

def sipariste_urun_var_mi(siparis_id, urun_id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM siparis_detay
        WHERE siparis_id=? AND urun_id=?
    """, (
        siparis_id,
        urun_id
    ))

    sonuc = cursor.fetchone()

    conn.close()

    return sonuc is not None


def siparise_urun_ekle(siparis_id, urun_id, miktar):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO siparis_detay
        (siparis_id, urun_id, miktar)
        VALUES (?, ?, ?)
    """, (
        siparis_id,
        urun_id,
        miktar
    ))

    conn.commit()
    conn.close()


def toplam_koli(siparis_id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            IFNULL(SUM(miktar),0)
        FROM siparis_detay
        WHERE siparis_id=?
    """, (siparis_id,))

    toplam = cursor.fetchone()[0]

    conn.close()

    return toplam

    conn.commit()

    conn.close()

# ==================================================
# GİRİŞ KONTROL
# ==================================================
# ==================================================
# GİRİŞ KONTROL
# ==================================================

def login_kontrol(kullanici_adi, sifre):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM subeler
        WHERE kullanici_adi=?
        AND sifre=?
        AND durum='Aktif'
    """, (
        kullanici_adi,
        sifre
    ))

    kullanici = cursor.fetchone()

    conn.close()

    return kullanici

  
def tum_subeleri_goster():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, sube_adi, kullanici_adi, sifre, durum
        FROM subeler
    """)

    sonuc = cursor.fetchall()

    conn.close()

    return sonuc

# ==================================================
# DASHBOARD VERİLERİ
# ==================================================


def toplam_sube_sayisi():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM subeler
    """)

    sonuc = cursor.fetchone()[0]

    conn.close()

    return sonuc



def toplam_urun_sayisi():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM urunler
    """)

    sonuc = cursor.fetchone()[0]

    conn.close()

    return sonuc



def toplam_siparis_sayisi():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM siparisler
    """)

    sonuc = cursor.fetchone()[0]

    conn.close()

    return sonuc

# ==========================
# SİPARİŞ GEÇMİŞİ
# ==========================

def siparis_gecmisi_ekle(
    siparis_id,
    tarih,
    kullanici,
    eski_durum,
    yeni_durum
):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO siparis_gecmisi
        (
            siparis_id,
            tarih,
            kullanici,
            eski_durum,
            yeni_durum
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        siparis_id,
        tarih,
        kullanici,
        eski_durum,
        yeni_durum
    ))

    conn.commit()
    conn.close()


def get_siparis_gecmisi(siparis_id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            tarih,
            kullanici,
            eski_durum,
            yeni_durum
        FROM siparis_gecmisi
        WHERE siparis_id=?
        ORDER BY id DESC
    """, (siparis_id,))

    sonuc = cursor.fetchall()

    conn.close()

    return sonuc

def get_tum_urunler():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            urun_adi,
            kategori,
            birim,
            palet_kapasitesi
        FROM urunler
        WHERE durum='Aktif'
        ORDER BY urun_adi
    """)

    sonuc = cursor.fetchall()

    conn.close()

    return sonuc


def get_tum_subeler():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            sube_adi
        FROM subeler
        WHERE durum='Aktif'
        ORDER BY sube_adi
    """)

    sonuc = cursor.fetchall()

    conn.close()

    return sonuc

def get_siparis_miktari(sube_id, urun_id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(sd.miktar),0)

        FROM siparis_detay sd

        INNER JOIN siparisler s
            ON s.id = sd.siparis_id

        WHERE
            s.sube_id=?
            AND sd.urun_id=?
    """, (
        sube_id,
        urun_id
    ))

    sonuc = cursor.fetchone()[0]

    conn.close()

    return sonuc
