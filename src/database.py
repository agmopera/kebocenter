import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_NAME = os.path.join(BASE_DIR, "siparis.db")


def connect_database():
    print("DB =", os.path.abspath(DB_NAME))
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
        cursor.execute("""ALTER TABLE subeler ADD COLUMN limit_tutari REAL DEFAULT 0""")
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
        cursor.execute("""ALTER TABLE urunler ADD COLUMN fiyat REAL DEFAULT 0""")
        print("✔ fiyat sütunu eklendi")
    except Exception as e:
        print("❌ fiyat:", e)


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

       # ======================================
    # MERKEZ STOK TABLOSU
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS merkez_stok(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            urun_id INTEGER UNIQUE,

            miktar REAL DEFAULT 0,

            FOREIGN KEY(urun_id)
            REFERENCES urunler(id)

        )
    """)


    # ======================================
    # ŞUBE STOK TABLOSU
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sube_stok(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            sube_id INTEGER,

            urun_id INTEGER,

            miktar REAL DEFAULT 0,

            UNIQUE(sube_id, urun_id),

            FOREIGN KEY(sube_id)
            REFERENCES subeler(id),

            FOREIGN KEY(urun_id)
            REFERENCES urunler(id)

        )
    """)


    # ======================================
    # STOK HAREKETLERİ
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stok_hareketleri(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            urun_id INTEGER,

            miktar REAL,

            hareket_tipi TEXT,

            kaynak TEXT,

            hedef TEXT,

            siparis_id INTEGER,

            tarih TEXT,

            aciklama TEXT,

            FOREIGN KEY(urun_id)
            REFERENCES urunler(id),

            FOREIGN KEY(siparis_id)
            REFERENCES siparisler(id)

        )
    """)
    # ======================================
# SEVKİYAT PROGRAMI
# ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sevkiyat_programi(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        hafta INTEGER,

        tarih TEXT,

        firma TEXT,

        sube_id INTEGER,

        donuk REAL DEFAULT 0,

        soguk REAL DEFAULT 0,

        donuk_doluluk REAL DEFAULT 0,

        soguk_doluluk REAL DEFAULT 0,

        atb_cikis TEXT,

        sube_teslim TEXT,

        palet_fiyat REAL DEFAULT 0,

        toplam_maliyet REAL DEFAULT 0,

        kayip_maliyeti REAL DEFAULT 0,

        durum TEXT DEFAULT 'PLANLANDI',

        FOREIGN KEY(sube_id)
        REFERENCES subeler(id)

    )
""")


    # ======================================
    # VERİTABANI KAYDET
    # ======================================

    conn.commit()


    # ======================================
    # VERİTABANI BAĞLANTISINI KAPAT
    # ======================================

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
            durum=?,
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

    # ==================================================
# SİPARİŞİN ŞUBE ID'SİNİ GETİR
# ==================================================

def get_siparis_sube_id(siparis_id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sube_id
        FROM siparisler
        WHERE id=?
    """, (
        siparis_id,
    ))

    sonuc = cursor.fetchone()

    conn.close()

    if sonuc:
        return sonuc[0]

    return None

  # ==================================================
# SİPARİŞ DETAYLARI + ÜRÜN TİPİ + PALET KAPASİTESİ
# ==================================================

def get_siparis_detaylari_sevkiyat(siparis_id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            d.urun_id,
            u.urun_adi,
            u.urun_tipi,
            u.palet_kapasitesi,
            d.miktar

        FROM siparis_detay d

        INNER JOIN urunler u
            ON d.urun_id = u.id

        WHERE d.siparis_id = ?

        ORDER BY u.urun_adi
    """, (
        siparis_id,
    ))

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
            palet_kapasitesi,
            fiyat,
            urun_tipi
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

# ==================================================
# FİNANS
# ==================================================

def get_finans_urunleri():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            urun_adi,
            birim,
            fiyat
        FROM urunler
        ORDER BY urun_adi
    """)

    sonuc = cursor.fetchall()

    conn.close()

    return sonuc


def fiyat_guncelle(id, fiyat):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE urunler
        SET fiyat=?
        WHERE id=?
    """, (
        fiyat,
        id
    ))

    conn.commit()
    conn.close()


def get_finans_subeleri():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            sube_adi,
            limit_tutari
        FROM subeler
        ORDER BY sube_adi
    """)

    sonuc = cursor.fetchall()

    conn.close()

    return sonuc


def limit_guncelle(id, limit_tutari):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE subeler
        SET limit_tutari=?
        WHERE id=?
    """, (
        limit_tutari,
        id
    ))

    conn.commit()
    conn.close()

def get_sube_limit(sube_id):

    conn = connect_database()

    cursor = conn.cursor()


    cursor.execute("""
        SELECT limit_tutari
        FROM subeler
        WHERE id=?
    """, (sube_id,))


    sonuc = cursor.fetchone()


    conn.close()


    if sonuc and sonuc[0]:

        return sonuc[0]


    return 0

    # ======================================
# ŞUBE SEVKİYAT BİLGİLERİ
# ======================================

def get_sube_sevkiyat_bilgileri(sube_id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            sevkiyat_gunu,
            sevkiyat_saati,
            teslim_suresi
        FROM subeler
        WHERE id=?
    """, (
        sube_id,
    ))

    sonuc = cursor.fetchone()

    conn.close()

    return sonuc
    

def aktif_siparis_var_mi(sube_id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM siparisler
        WHERE sube_id=?
        AND durum IN (
            'Hazırlandı',
            'Onaylandı',
            'Sevkiyatta'
        )
    """, (sube_id,))

    sonuc = cursor.fetchone()[0]

    conn.close()

    return sonuc > 0
        
# ==================================================
# STOKLAR
# ==================================================

def get_merkez_stok():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            u.id,
            u.urun_adi,
            u.birim,
            COALESCE(ms.miktar, 0)
        FROM urunler u
        LEFT JOIN merkez_stok ms
            ON u.id = ms.urun_id
        WHERE u.durum='Aktif'
        ORDER BY u.urun_adi
    """)

    sonuc = cursor.fetchall()

    conn.close()

    return sonuc


def merkez_stok_giris(urun_id, miktar):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO merkez_stok
        (
            urun_id,
            miktar
        )
        VALUES (?, ?)

        ON CONFLICT(urun_id)
        DO UPDATE SET
            miktar = miktar + excluded.miktar
    """, (
        urun_id,
        miktar
    ))

    conn.commit()
    conn.close()


def stok_hareketi_ekle(
    urun_id,
    miktar,
    hareket_tipi,
    kaynak,
    hedef,
    siparis_id=None,
    aciklama=""
):

    conn = connect_database()
    cursor = conn.cursor()

    from datetime import datetime

    tarih = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO stok_hareketleri
        (
            urun_id,
            miktar,
            hareket_tipi,
            kaynak,
            hedef,
            siparis_id,
            tarih,
            aciklama
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        urun_id,
        miktar,
        hareket_tipi,
        kaynak,
        hedef,
        siparis_id,
        tarih,
        aciklama
    ))

    conn.commit()
    conn.close()

# ==================================================
# STOK HAREKETLERİ LİSTESİ
# ==================================================
# ======================================
# STOK HAREKETLERİNİ GETİR
# FİLTRELİ
# ======================================

def get_stok_hareketleri(
    baslangic=None,
    bitis=None,
    sube_id=None,
    urun_id=None,
    hareket_tipi=None,
    arama=None
):

    conn = connect_database()
    cursor = conn.cursor()

    sorgu = """
        SELECT

            sh.id,

            sh.tarih,

            u.urun_adi,

            u.birim,

            sh.miktar,

            sh.hareket_tipi,

            sh.kaynak,

            sh.hedef,

            sh.siparis_id,

            sh.aciklama,

            sb.sube_adi

        FROM stok_hareketleri sh

        INNER JOIN urunler u
            ON sh.urun_id = u.id

        LEFT JOIN siparisler s
            ON sh.siparis_id = s.id

        LEFT JOIN subeler sb
            ON s.sube_id = sb.id

        WHERE 1=1
    """

    parametreler = []


    # ======================================
    # BAŞLANGIÇ TARİHİ
    # ======================================

    if baslangic:

        sorgu += """
            AND date(sh.tarih) >= date(?)
        """

        parametreler.append(
            baslangic
        )


    # ======================================
    # BİTİŞ TARİHİ
    # ======================================

    if bitis:

        sorgu += """
            AND date(sh.tarih) <= date(?)
        """

        parametreler.append(
            bitis
        )


    # ======================================
    # ŞUBE
    # ======================================

    if sube_id:

        sorgu += """
            AND (
                s.sube_id = ?
                OR sh.kaynak = (
                    SELECT sube_adi
                    FROM subeler
                    WHERE id=?
                )
            )
        """

        parametreler.append(
            sube_id
        )

        parametreler.append(
            sube_id
        )


    # ======================================
    # ÜRÜN
    # ======================================

    if urun_id:

        sorgu += """
            AND sh.urun_id = ?
        """

        parametreler.append(
            urun_id
        )


    # ======================================
    # HAREKET TİPİ
    # ======================================

    if hareket_tipi:

        sorgu += """
            AND sh.hareket_tipi = ?
        """

        parametreler.append(
            hareket_tipi
        )


    # ======================================
    # GENEL ARAMA
    # ======================================

    if arama:

        sorgu += """
            AND (
                u.urun_adi LIKE ?
                OR sh.kaynak LIKE ?
                OR sh.hedef LIKE ?
                OR sh.aciklama LIKE ?
            )
        """

        arama_degeri = "%" + arama + "%"

        parametreler.extend([
            arama_degeri,
            arama_degeri,
            arama_degeri,
            arama_degeri
        ])


    # ======================================
    # SIRALAMA
    # ======================================

    sorgu += """
        ORDER BY sh.id DESC
    """


    cursor.execute(
        sorgu,
        parametreler
    )

    sonuc = cursor.fetchall()

    conn.close()

    return sonuc

    # ======================================
# ŞUBE STOKLARINI GETİR
# ======================================

def get_sube_stoklari(sube_id=None):

    conn = connect_database()
    cursor = conn.cursor()

    if sube_id:
        cursor.execute("""
            SELECT
                ss.sube_id,
                sb.sube_adi,
                ss.urun_id,
                u.urun_adi,
                u.birim,
                ss.miktar

            FROM sube_stok ss

            INNER JOIN subeler sb
                ON ss.sube_id = sb.id

            INNER JOIN urunler u
                ON ss.urun_id = u.id

            WHERE ss.sube_id = ?

            ORDER BY
                u.urun_adi
        """, (
            sube_id,
        ))

    else:
        cursor.execute("""
            SELECT
                ss.sube_id,
                sb.sube_adi,
                ss.urun_id,
                u.urun_adi,
                u.birim,
                ss.miktar

            FROM sube_stok ss

            INNER JOIN subeler sb
                ON ss.sube_id = sb.id

            INNER JOIN urunler u
                ON ss.urun_id = u.id

            ORDER BY
                sb.sube_adi,
                u.urun_adi
        """)

    sonuc = cursor.fetchall()

    conn.close()

    return sonuc

# ======================================
# STOK HAREKETLERİNİ GETİR
# ======================================


            # ==================================================
# ŞUBE STOK GÜNCELLE
# ==================================================

def sube_stok_guncelle(
    sube_id,
    urun_id,
    miktar
):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sube_stok
        (
            sube_id,
            urun_id,
            miktar
        )
        VALUES (?, ?, ?)

        ON CONFLICT(sube_id, urun_id)
        DO UPDATE SET
            miktar = miktar + excluded.miktar
    """, (
        sube_id,
        urun_id,
        miktar
    ))

    conn.commit()
    conn.close()


# ==================================================
# MERKEZ STOK AZALT
# ==================================================

def merkez_stok_azalt(
    urun_id,
    miktar
):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO merkez_stok
        (
            urun_id,
            miktar
        )
        VALUES (?, ?)

        ON CONFLICT(urun_id)
        DO UPDATE SET
            miktar = miktar - ?
    """, (
        urun_id,
        0,
        miktar
    ))

    conn.commit()
    conn.close()


# ==================================================
# SİPARİŞ STOKLARINI AKTAR
# ==================================================

def siparis_stoklarini_aktar(
    siparis_id
):

    conn = connect_database()
    cursor = conn.cursor()

    # ======================================
    # SİPARİŞİN ŞUBESİNİ BUL
    # ======================================

    cursor.execute("""
        SELECT
            sube_id
        FROM siparisler
        WHERE id=?
    """, (
        siparis_id,
    ))

    siparis = cursor.fetchone()

    if not siparis:

        conn.close()
        return

    sube_id = siparis[0]


    # ======================================
    # SİPARİŞ ÜRÜNLERİNİ AL
    # ======================================

    cursor.execute("""
        SELECT
            urun_id,
            miktar
        FROM siparis_detay
        WHERE siparis_id=?
    """, (
        siparis_id,
    ))

    detaylar = cursor.fetchall()


    # ======================================
    # ÜRÜNLERİ AKTAR
    # ======================================

    for detay in detaylar:

        urun_id = detay[0]
        miktar = detay[1]


        # ==================================
        # MERKEZ STOKTAN DÜŞ
        # ==================================

        cursor.execute("""
            INSERT INTO merkez_stok
            (
                urun_id,
                miktar
            )
            VALUES (?, ?)

            ON CONFLICT(urun_id)
            DO UPDATE SET
                miktar = miktar - ?
        """, (
            urun_id,
            -miktar,
            miktar
        ))


        # ==================================
        # ŞUBE STOKUNA EKLE
        # ==================================

        cursor.execute("""
            INSERT INTO sube_stok
            (
                sube_id,
                urun_id,
                miktar
            )
            VALUES (?, ?, ?)

            ON CONFLICT(sube_id, urun_id)
            DO UPDATE SET
                miktar = miktar + excluded.miktar
        """, (
            sube_id,
            urun_id,
            miktar
        ))


        # ==================================
        # STOK HAREKETİ
        # ==================================

        from datetime import datetime

        tarih = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute("""
            INSERT INTO stok_hareketleri
            (
                urun_id,
                miktar,
                hareket_tipi,
                kaynak,
                hedef,
                siparis_id,
                tarih,
                aciklama
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            urun_id,
            miktar,
            "Sipariş Sevki",
            "Merkez Depo",
            str(sube_id),
            siparis_id,
            tarih,
            "Sipariş onaylandı ve stok transferi yapıldı"
        ))


    conn.commit()
    conn.close()

    # ==================================================
# ŞUBE SATIŞ STOK İŞLEMLERİ
# ==================================================
def sube_stok_azalt(
    sube_id,
    urun_id,
    miktar
):

    conn = connect_database()
    cursor = conn.cursor()

    # ======================================
    # ŞUBE BİLGİSİNİ AL
    # ======================================

    cursor.execute("""
        SELECT
            sube_adi
        FROM subeler
        WHERE id=?
    """, (
        sube_id,
    ))

    sube = cursor.fetchone()

    if not sube:
        conn.close()
        return False

    sube_adi = sube[0]


    # ======================================
    # ÜRÜN BİLGİSİNİ AL
    # ======================================

    cursor.execute("""
        SELECT
            urun_adi,
            birim
        FROM urunler
        WHERE id=?
    """, (
        urun_id,
    ))

    urun = cursor.fetchone()

    if not urun:
        conn.close()
        return False

    urun_adi = urun[0]
    birim = urun[1]


   # ======================================
    # ŞUBE STOKTAN SATIŞI DÜŞ
    # ======================================

    cursor.execute("""
        SELECT miktar
        FROM sube_stok
        WHERE sube_id=?
        AND urun_id=?
    """, (
        sube_id,
        urun_id
    ))

    mevcut = cursor.fetchone()


    if mevcut:

        cursor.execute("""
            UPDATE sube_stok
            SET miktar = miktar - ?
            WHERE sube_id=?
            AND urun_id=?
        """, (
            miktar,
            sube_id,
            urun_id
        ))

    else:

        cursor.execute("""
            INSERT INTO sube_stok
            (
                sube_id,
                urun_id,
                miktar
            )
            VALUES (?, ?, ?)
        """, (
            sube_id,
            urun_id,
            -miktar
        ))


    # ======================================
    # STOK HAREKETİ
    # ======================================

    from datetime import datetime

    tarih = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    cursor.execute("""
        INSERT INTO stok_hareketleri
        (
            urun_id,
            miktar,
            hareket_tipi,
            kaynak,
            hedef,
            siparis_id,
            tarih,
            aciklama
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        urun_id,
        -miktar,
        "Satış",
        sube_adi,
        "Müşteri",
        None,
        tarih,
        "Excel satış verisi aktarımı"
    ))


    conn.commit()
    conn.close()

    return True
    

def get_sube_urun_id(
    sube_adi,
    urun_adi
):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.id,
            u.id

        FROM subeler s

        CROSS JOIN urunler u

        WHERE
            UPPER(TRIM(s.sube_adi))
            =
            UPPER(TRIM(?))

            AND

            UPPER(TRIM(u.urun_adi))
            =
            UPPER(TRIM(?))
    """, (
        sube_adi,
        urun_adi
    ))

    sonuc = cursor.fetchone()

    conn.close()

    return sonuc

    # ==================================================
# SEVKİYAT PROGRAMINA KAYIT EKLE
# ==================================================

def sevkiyat_programi_ekle(
    hafta,
    tarih,
    firma,
    sube_id,
    donuk,
    soguk,
    donuk_doluluk,
    soguk_doluluk,
    atb_cikis,
    sube_teslim,
    palet_fiyat,
    toplam_maliyet,
    kayip_maliyeti,
    durum="PLANLANDI"
):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sevkiyat_programi
        (
            hafta,
            tarih,
            firma,
            sube_id,
            donuk,
            soguk,
            donuk_doluluk,
            soguk_doluluk,
            atb_cikis,
            sube_teslim,
            palet_fiyat,
            toplam_maliyet,
            kayip_maliyeti,
            durum
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        hafta,
        tarih,
        firma,
        sube_id,
        donuk,
        soguk,
        donuk_doluluk,
        soguk_doluluk,
        atb_cikis,
        sube_teslim,
        palet_fiyat,
        toplam_maliyet,
        kayip_maliyeti,
        durum
    ))

    sevkiyat_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return sevkiyat_id

# ==================================================
# SEVKİYAT PROGRAMINI GETİR
# ==================================================

def get_sevkiyat_programi(
    baslangic=None,
    bitis=None,
    sube_id=None,
    firma=None
):

    conn = connect_database()
    cursor = conn.cursor()

    sorgu = """
        SELECT
            s.id,
            s.hafta,
            s.tarih,
            s.firma,
            sb.id,
            sb.sube_adi,
            s.donuk,
            s.soguk,
            s.donuk_doluluk,
            s.soguk_doluluk,
            s.atb_cikis,
            s.sube_teslim,
            s.palet_fiyat,
            s.toplam_maliyet,
            s.kayip_maliyeti,
            s.durum

        FROM sevkiyat_programi s

        INNER JOIN subeler sb
            ON s.sube_id = sb.id

        WHERE 1=1
    """

    parametreler = []

    # ======================================
    # BAŞLANGIÇ TARİHİ
    # ======================================

    if baslangic:

        sorgu += """
            AND date(s.tarih) >= date(?)
        """

        parametreler.append(baslangic)

    # ======================================
    # BİTİŞ TARİHİ
    # ======================================

    if bitis:

        sorgu += """
            AND date(s.tarih) <= date(?)
        """

        parametreler.append(bitis)

    # ======================================
    # ŞUBE FİLTRESİ
    # ======================================

    if sube_id:

        sorgu += """
            AND s.sube_id = ?
        """

        parametreler.append(sube_id)

    # ======================================
    # FİRMA FİLTRESİ
    # ======================================

    if firma:

        sorgu += """
            AND s.firma = ?
        """

        parametreler.append(firma)

    # ======================================
    # SIRALAMA
    # ======================================

    sorgu += """
        ORDER BY
            date(s.tarih),
            sb.sube_adi
    """

    cursor.execute(
        sorgu,
        parametreler
    )

    sonuc = cursor.fetchall()

    conn.close()

    return sonuc
