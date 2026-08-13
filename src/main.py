from datetime import datetime, timedelta
import json
import random

from openpyxl import Workbook
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

from io import BytesIO

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    abort,
    flash,
    send_file,
    jsonify
)

from database import (
    create_tables,

    # ======================================
    # ŞUBELER
    # ======================================

    add_sube,
    get_subeler,
    get_sube,
    update_sube,
    delete_sube,

    # ======================================
    # ÜRÜNLER
    # ======================================

    add_urun,
    get_urunler,
    get_urun,
    update_urun,
    delete_urun,

    # ======================================
    # SİPARİŞLER
    # ======================================

    add_siparis,
    add_siparis_detay,
    get_siparisler,
    get_sube_siparisleri,
    get_onay_bekleyen_siparisler,
    get_siparis,
    get_siparis_detaylari,
    get_siparis_sube_id,
    get_siparis_detaylari_sevkiyat,

    get_tum_urunler,
    get_tum_subeler,
    get_siparis_miktari,
    delete_siparis,
    update_siparis,
    update_siparis_detay,
    delete_siparis_detay,
    siparis_durum_guncelle,
    siparis_gecmisi_ekle,
    get_siparis_gecmisi,

    # ======================================
    # FİNANS
    # ======================================

    get_finans_urunleri,
    get_finans_subeleri,
    fiyat_guncelle,
    limit_guncelle,
    aktif_siparis_var_mi,
    get_sube_limit,
    get_sube_sevkiyat_bilgileri,

    # ======================================
    # SİPARİŞ ÜRÜN İŞLEMLERİ
    # ======================================

    siparise_urun_ekle,
    siparis_stoklarini_aktar,
    sube_stok_azalt,
    get_sube_urun_id,
    get_sube_stoklari,
    get_stok_hareketleri,
    get_merkez_stok,
    sipariste_urun_var_mi,
    toplam_koli,
    merkez_stok_giris,
    stok_hareketi_ekle,

    # ======================================
    # SEVKİYAT
    # ======================================

    sevkiyat_programi_ekle,
    get_sevkiyat_programi,

    # ======================================
    # GİRİŞ
    # ======================================

    login_kontrol,

    # ======================================
    # DASHBOARD
    # ======================================

    toplam_sube_sayisi,
    toplam_urun_sayisi,
    toplam_siparis_sayisi
)


app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)


@app.before_request
def test():
    print(
        "METHOD:",
        request.method,
        "URL:",
        request.path
    )


app.secret_key = "siparis_sistemi_2026"

create_tables()


# ==========================
# SİPARİŞ DURUMLARI
# ==========================

SIPARIS_DURUMLARI = [
    "Hazırlandı",
    "Onaylandı",
    "Hazırlanıyor",
    "Sevk edildi",
    "Tamamlandı"
]


# ==========================
# YETKİ KONTROL
# ==========================

def admin_kontrol():

    if "giris" not in session:
        return redirect("/")

    if session.get("yetki") != "admin":
        abort(403)

    return None


# ==========================
# LOGIN
# ==========================

@app.route("/", methods=["GET", "POST"])
def login():

    print("LOGIN FONKSİYONU ÇALIŞTI")

    if request.method == "POST":

        kullanici_adi = request.form["kullanici"]
        sifre = request.form["sifre"]

        print("GELEN:", kullanici_adi, sifre)

        if kullanici_adi == "admin" and sifre == "admin123":

            session.clear()

            session["giris"] = True
            session["yetki"] = "admin"
            session["sube_id"] = 0
            session["sube_adi"] = "ADMIN"

            return redirect("/dashboard")

        kullanici = login_kontrol(
            kullanici_adi,
            sifre
        )

        if kullanici:

            session.clear()

            session["giris"] = True
            session["yetki"] = "sube"
            session["sube_id"] = kullanici[0]
            session["sube_adi"] = kullanici[1]

            return redirect("/dashboard")

        return """
        <h2>Kullanıcı adı veya şifre hatalı.</h2>
        <a href="/">Tekrar Dene</a>
        """

    return render_template("login.html")


# ==========================
# ÇIKIŞ
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    if "giris" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        yetki=session["yetki"],
        sube=session["sube_adi"],
        siparis_sayisi=toplam_siparis_sayisi(),
        sube_sayisi=toplam_sube_sayisi(),
        urun_sayisi=toplam_urun_sayisi()
    )


# ==========================
# ŞUBELER
# ==========================

@app.route("/subeler")
def subeler():

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    liste = get_subeler()

    return render_template(
        "subeler.html",
        subeler=liste
    )


@app.route("/yeni-sube", methods=["GET", "POST"])
def yeni_sube():

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    if request.method == "POST":

        add_sube(
            request.form["sube_adi"],
            request.form["kullanici_adi"],
            request.form["sifre"],
            request.form["yetkili"],
            request.form["telefon"],
            request.form["eposta"],
            request.form["il"],
            request.form["ilce"],
            request.form["adres"],
            request.form["durum"],
            request.form["uretim_gunu"],
            request.form["sevkiyat_gunu"],
            request.form["sevkiyat_saati"],
            request.form["teslim_suresi"]
        )

        return redirect("/subeler")

    return render_template(
        "yeni_sube.html"
    )


@app.route(
    "/sube-duzenle/<int:id>",
    methods=["GET", "POST"]
)
def sube_duzenle(id):

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    if request.method == "POST":

        update_sube(
            id,
            request.form["sube_adi"],
            request.form["kullanici_adi"],
            request.form["sifre"],
            request.form["yetkili"],
            request.form["telefon"],
            request.form["eposta"],
            request.form["il"],
            request.form["ilce"],
            request.form["adres"],
            request.form["durum"],
            request.form["uretim_gunu"],
            request.form["sevkiyat_gunu"],
            request.form["sevkiyat_saati"],
            request.form["teslim_suresi"]
        )

        return redirect("/subeler")

    sube = get_sube(id)

    return render_template(
        "sube_duzenle.html",
        sube=sube
    )


@app.route("/sube-sil/<int:id>")
def sube_sil(id):

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    delete_sube(id)

    return redirect("/subeler")


# ==========================
# ÜRÜNLER
# ==========================

@app.route("/urunler")
def urunler():

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    liste = get_urunler()

    return render_template(
        "urunler.html",
        urunler=liste
    )


# ==========================
# FİNANS
# ==========================

@app.route("/finans", methods=["GET", "POST"])
def finans():

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    if request.method == "POST":

        islem = request.form.get("islem")

        # ==========================
        # FİYATLARI KAYDET
        # ==========================

        if islem == "fiyatlar":

            urunler = get_finans_urunleri()

            for urun in urunler:

                fiyat = request.form.get(
                    f"fiyat_{urun[0]}",
                    "0"
                )

                try:
                    fiyat = float(fiyat)
                except:
                    fiyat = 0

                fiyat_guncelle(
                    urun[0],
                    fiyat
                )

        # ==========================
        # LİMİTLERİ KAYDET
        # ==========================

        elif islem == "limitler":

            subeler = get_finans_subeleri()

            for sube in subeler:

                limit = request.form.get(
                    f"limit_{sube[0]}",
                    "0"
                )

                try:
                    limit = float(limit)
                except:
                    limit = 0

                limit_guncelle(
                    sube[0],
                    limit
                )

        return redirect("/finans")

    urunler = get_finans_urunleri()
    subeler = get_finans_subeleri()

    return render_template(
        "finans.html",
        urunler=urunler,
        subeler=subeler
    )


# ==========================
# RAPORLAR
# ==========================

@app.route("/raporlar")
def raporlar():

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    return render_template("raporlar.html")


# ==========================
# AI
# ==========================

@app.route("/ai")
def ai():

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    return render_template("ai.html")


# ======================================
# MERKEZ STOK GİRİŞİ
# ======================================

@app.route(
    "/stok-giris",
    methods=["POST"]
)
def stok_giris():

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    urun_id = request.form["urun_id"]

    miktar = float(
        request.form["miktar"]
    )

    if miktar <= 0:
        return redirect("/stoklar")

    merkez_stok_giris(
        urun_id,
        miktar
    )

    stok_hareketi_ekle(
        urun_id,
        miktar,
        "Giriş",
        "Tedarikçi",
        "Merkez Depo",
        None,
        "Merkez stok girişi"
    )

    return redirect("/stoklar")


# ======================================
# YENİ ÜRÜN
# ======================================

@app.route(
    "/yeni-urun",
    methods=["GET", "POST"]
)
def yeni_urun():

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    if request.method == "POST":

        add_urun(
            request.form["urun_kodu"],
            request.form["urun_adi"],
            request.form["kategori"],
            request.form["birim"],
            request.form["durum"],
            request.form["palet_kapasitesi"],
            request.form["urun_tipi"],
            request.form.get("koli_agirligi", 0)
        )

        return redirect("/urunler")

    return render_template(
        "yeni_urun.html"
    )


@app.route(
    "/urun-duzenle/<int:id>",
    methods=["GET", "POST"]
)
def urun_duzenle(id):

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    if request.method == "POST":

        update_urun(
            id,
            request.form["urun_kodu"],
            request.form["urun_adi"],
            request.form["kategori"],
            request.form["birim"],
            request.form["palet_kapasitesi"],
            request.form["urun_tipi"],
            request.form.get("koli_agirligi", 0),
            request.form["durum"]
        )

        return redirect("/urunler")

    urun = get_urun(id)

    return render_template(
        "urun_duzenle.html",
        urun=urun
    )


@app.route("/urun-sil/<int:id>")
def urun_sil(id):

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    delete_urun(id)

    return redirect("/urunler")


# ==========================
# SİPARİŞLER
# ==========================

@app.route("/siparisler")
def siparisler():

    if "giris" not in session:
        return redirect("/")

    if session["yetki"] == "admin":

        liste = get_siparisler()

    else:

        liste = get_sube_siparisleri(
            session["sube_id"]
        )

    return render_template(
        "siparisler.html",
        siparisler=liste,
        yetki=session["yetki"]
    )


@app.route("/siparis-detay/<int:id>")
def siparis_detay(id):

    if "giris" not in session:
        return redirect("/")

    siparis = get_siparis(id)

    if not siparis:
        abort(404)

    # ==========================
    # ŞUBE YETKİ KONTROLÜ
    # ==========================

    if session["yetki"] == "sube":

        if siparis[2] != session["sube_adi"]:
            abort(403)

    detaylar = get_siparis_detaylari(id)

    gecmis = get_siparis_gecmisi(id)

    return render_template(
        "siparis_detay.html",
        siparis=siparis,
        detaylar=detaylar,
        gecmis=gecmis
    )


@app.route("/siparis-sil/<int:id>")
def siparis_sil(id):

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    delete_siparis(id)

    return redirect("/siparisler")


@app.route(
    "/siparis-durum/<int:id>",
    methods=["POST"]
)
def siparis_durum(id):

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    siparis = get_siparis(id)

    if not siparis:
        abort(404)

    eski_durum = siparis[4]

    yeni_durum = request.form["durum"]

    # Durum değişmemişse kayıt oluşturma
    if eski_durum == yeni_durum:
        return redirect("/siparisler")

    siparis_durum_guncelle(
        id,
        yeni_durum
    )

    siparis_gecmisi_ekle(
        siparis_id=id,
        tarih=datetime.now().strftime(
            "%d.%m.%Y %H:%M"
        ),
        kullanici=session["sube_adi"],
        eski_durum=eski_durum,
        yeni_durum=yeni_durum
    )

    return redirect("/siparisler")


# ======================================
# SEVKİYAT TARİH / SAAT HESABI
# ======================================

def sevkiyat_zamani_hesapla(
    siparis_tarihi,
    sevkiyat_gunu,
    sevkiyat_saati,
    teslim_suresi
):

    try:

        # ----------------------------------
        # SİPARİŞ TARİHİ
        # ----------------------------------

        tarih = datetime.strptime(
            siparis_tarihi,
            "%Y-%m-%d"
        )

        # ----------------------------------
        # SEVKİYAT GÜNLERİ
        # ----------------------------------

        gunler = {
            "Pazartesi": 0,
            "Salı": 1,
            "Çarşamba": 2,
            "Perşembe": 3,
            "Cuma": 4,
            "Cumartesi": 5,
            "Pazar": 6
        }

        hedef_gun = gunler.get(
            sevkiyat_gunu
        )

        if hedef_gun is None:
            return None, None, None

        # ----------------------------------
        # BİR SONRAKİ SEVKİYAT GÜNÜ
        # ----------------------------------

        mevcut_gun = tarih.weekday()

        fark = (
            hedef_gun - mevcut_gun
        ) % 7

        sevkiyat_tarihi = (
            tarih +
            timedelta(days=fark)
        )

        # ----------------------------------
        # SEVKİYAT SAATİ
        # ----------------------------------

        if not sevkiyat_saati:
            sevkiyat_saati = "18:00"

        saat = datetime.strptime(
            str(sevkiyat_saati),
            "%H:%M"
        ).time()

        atb_cikis = datetime.combine(
            sevkiyat_tarihi.date(),
            saat
        )

        # ----------------------------------
        # TESLİM SÜRESİ
        # ----------------------------------

        try:

            teslim_suresi = float(
                teslim_suresi or 0
            )

        except:

            teslim_suresi = 0

        # ----------------------------------
        # ŞUBE TESLİM
        # ----------------------------------

        sube_teslim = (
            atb_cikis +
            timedelta(hours=teslim_suresi)
        )

        return (
            sevkiyat_tarihi,
            atb_cikis,
            sube_teslim
        )

    except Exception as e:

        print(
            "Sevkiyat zamanı hesaplama hatası:",
            e
        )

        return None, None, None


# ======================================
# ADMIN SİPARİŞ ONAY
# ======================================

@app.route("/siparis-onayla/<int:id>")
def siparis_onayla(id):

    # ==================================
    # ADMIN KONTROLÜ
    # ==================================

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    # ==================================
    # SİPARİŞİ BUL
    # ==================================

    siparis = get_siparis(id)

    if not siparis:
        abort(404)

    # ==================================
    # SADECE HAZIRLANDI DURUMUNDA
    # ONAYLANABİLİR
    # ==================================

    if siparis[4] != "Hazırlandı":
        return redirect("/siparisler")

    # ==================================
    # ŞUBE ID
    # ==================================

    sube_id = get_siparis_sube_id(id)

    if not sube_id:
        return redirect("/siparisler")

    # ==================================
    # SİPARİŞ TARİHİ
    # ==================================

    siparis_tarihi = siparis[3]

    # ==================================
    # ŞUBE SEVKİYAT BİLGİLERİ
    # ==================================

    sube_bilgileri = get_sube_sevkiyat_bilgileri(
        sube_id
    )

    if not sube_bilgileri:
        return redirect("/siparisler")

    sevkiyat_gunu = sube_bilgileri[0]

    sevkiyat_saati = sube_bilgileri[1]

    teslim_suresi = sube_bilgileri[2]

    # ==================================
    # SİPARİŞ DETAYLARI
    # ==================================

    detaylar = get_siparis_detaylari_sevkiyat(id)

    # ==================================
    # PALET TOPLAMLARI
    # ==================================

    donuk = 0
    soguk = 0

    donuk_esdeger = 0
    soguk_esdeger = 0

    # ==================================
    # ÜRÜNLERİ TEK TEK İNCELE
    # ==================================

    for detay in detaylar:

        # ----------------------------------
        # detay:
        #
        # 0 = urun_id
        # 1 = urun_adi
        # 2 = urun_tipi
        # 3 = palet_kapasitesi
        # 4 = miktar
        # ----------------------------------

        urun_tipi = detay[2]

        palet_kapasitesi = float(
            detay[3] or 0
        )

        miktar = float(
            detay[4] or 0
        )

        # ----------------------------------
        # PALET KAPASİTESİ YOKSA GEÇ
        # ----------------------------------

        if palet_kapasitesi <= 0:
            continue

        # ==================================
        # PALET EŞDEĞERİ
        # ==================================

        palet_esdegeri = (
            miktar / palet_kapasitesi
        )

        # ==================================
        # EXCEL YUVARLAMA KURALI
        #
        # 0,00 - 0,11 → aşağı
        # 0,12 ve üstü → yukarı
        # ==================================

        tam_kisim = int(
            palet_esdegeri
        )

        ondalik_kisim = (
            palet_esdegeri
            - tam_kisim
        )

        if ondalik_kisim < 0.12:

            fiziksel_palet = tam_kisim

        else:

            fiziksel_palet = tam_kisim + 1

        # ==================================
        # MİKTAR VARSA EN AZ 1 PALET
        # ==================================

        if (
            miktar > 0
            and fiziksel_palet == 0
        ):

            fiziksel_palet = 1

        # ==================================
        # DONUK
        # ==================================

        if urun_tipi == "Donuk":

            donuk += fiziksel_palet

            # DOLULUK İÇİN PALET EŞDEĞERİ
            donuk_esdeger += palet_esdegeri

        # ==================================
        # SOĞUK
        # ==================================

        elif urun_tipi == "Soğuk":

            soguk += fiziksel_palet

            # DOLULUK İÇİN PALET EŞDEĞERİ
            soguk_esdeger += palet_esdegeri

    # ==================================
    # DOLULUK HESAPLARI
    # ==================================

    donuk_doluluk = 0
    soguk_doluluk = 0

    # ==================================
    # DONUK DOLULUK
    # ==================================

    if donuk > 0:

        donuk_doluluk = (
            donuk_esdeger / donuk
        ) * 100

    # ==================================
    # SOĞUK DOLULUK
    # ==================================

    if soguk > 0:

        soguk_doluluk = (
            soguk_esdeger / soguk
        ) * 100

    # ==================================
    # SEVKİYAT ZAMANI HESAPLA
    # ==================================

    (
        sevkiyat_tarihi,
        atb_cikis,
        sube_teslim
    ) = sevkiyat_zamani_hesapla(
        siparis_tarihi,
        sevkiyat_gunu,
        sevkiyat_saati,
        teslim_suresi
    )

    if not sevkiyat_tarihi:
        return redirect("/siparisler")

    hafta = sevkiyat_tarihi.isocalendar().week

    # ==================================
    # SEVKİYAT PROGRAMINA KAYIT
    # ==================================

    sevkiyat_programi_ekle(
        hafta=hafta,
        tarih=sevkiyat_tarihi,
        firma="Belirlenmedi",
        sube_id=sube_id,
        donuk=donuk,
        soguk=soguk,
        donuk_doluluk=donuk_doluluk,
        soguk_doluluk=soguk_doluluk,
        atb_cikis=atb_cikis.strftime(
            "%d.%m.%Y %H:%M"
        ),
        sube_teslim=sube_teslim.strftime(
            "%d.%m.%Y %H:%M"
        ),
        palet_fiyat=0,
        toplam_maliyet=0,
        kayip_maliyeti=0,
        durum="PLANLANDI"
    )

    # ==================================
    # STOKLARI AKTAR
    # ==================================

    siparis_stoklarini_aktar(id)

    # ==================================
    # SİPARİŞ DURUMU
    # ==================================

    siparis_durum_guncelle(
        id,
        "Onaylandı"
    )

    # ==================================
    # SİPARİŞ GEÇMİŞİ
    # ==================================

    siparis_gecmisi_ekle(
        siparis_id=id,
        tarih=datetime.now().strftime(
            "%d.%m.%Y %H:%M"
        ),
        kullanici=session.get(
            "sube_adi",
            "Admin"
        ),
        eski_durum="Hazırlandı",
        yeni_durum="Onaylandı"
    )

    # ==================================
    # GERİ DÖN
    # ==================================

    return redirect("/siparisler")


# ======================================
# SİPARİŞ DÜZENLE
# ======================================

@app.route(
    "/siparis-duzenle/<int:id>",
    methods=["GET", "POST"]
)
def siparis_duzenle(id):

    siparis = get_siparis(id)

    if not siparis:
        return "Sipariş bulunamadı"

    durum = siparis[4]

    # ŞUBE KONTROLÜ
    if session.get("yetki") == "sube":

        if durum != "Hazırlandı":

            return """
            <h3>
            Bu sipariş artık düzenlenemez.
            </h3>

            <a href="/siparisler">
            Siparişlere Dön
            </a>
            """

    if request.method == "POST":

        detaylar = get_siparis_detaylari(id)

        for detay in detaylar:

            yeni_miktar = request.form.get(
                f"miktar_{detay[0]}"
            )

            if yeni_miktar is not None:

                update_siparis_detay(
                    detay[0],
                    yeni_miktar
                )

        yeni_urun = request.form.get(
            "yeni_urun"
        )

        yeni_miktar = request.form.get(
            "yeni_miktar"
        )

        if yeni_urun and yeni_miktar:

            if not sipariste_urun_var_mi(
                id,
                yeni_urun
            ):

                siparise_urun_ekle(
                    id,
                    yeni_urun,
                    yeni_miktar
                )

        return redirect(
            f"/siparis-duzenle/{id}"
        )

    siparis = get_siparis(id)

    detaylar = get_siparis_detaylari(id)

    urunler = get_urunler()

    toplam = toplam_koli(id)

    return render_template(
        "siparis_duzenle.html",
        siparis=siparis,
        detaylar=detaylar,
        urunler=urunler,
        toplam=toplam
    )


@app.route(
    "/siparis-detay-sil/<int:detay_id>/<int:siparis_id>"
)
def siparis_detay_sil(
    detay_id,
    siparis_id
):

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    delete_siparis_detay(
        detay_id
    )

    return redirect(
        f"/siparis-duzenle/{siparis_id}"
    )


# ======================================
# YENİ SİPARİŞ
# ======================================

@app.route(
    "/yeni-siparis",
    methods=["GET", "POST"]
)
def yeni_siparis():

    if "giris" not in session:
        return redirect("/")

    if request.method == "POST":

        # ADMIN istediği şubeyi seçebilir
        if session["yetki"] == "admin":

            sube_id = request.form["sube_id"]

        # ŞUBE sadece kendi adına sipariş verir
        else:

            sube_id = session["sube_id"]

        tarih = datetime.now().strftime(
            "%Y-%m-%d"
        )

        urunler_json = request.form[
            "urunler_json"
        ]

        urun_listesi = json.loads(
            urunler_json
        )

        siparis_no = (
            "SP-"
            + datetime.now().strftime("%Y%m%d")
            + "-"
            + str(random.randint(1000, 9999))
        )

        siparis_id = add_siparis(
            siparis_no,
            sube_id,
            tarih,
            "Hazırlandı"
        )

        for urun in urun_listesi:

            add_siparis_detay(
                siparis_id,
                urun["id"],
                urun["miktar"]
            )

        return redirect("/siparisler")

    # ADMIN bütün şubeleri görür
    if session["yetki"] == "admin":

        subeler = get_subeler()

    else:

        # Aktif sipariş kontrolü
        if aktif_siparis_var_mi(
            session["sube_id"]
        ):

            return """
            <script>
                alert(
                    "Bu hafta zaten aktif bir siparişiniz bulunmaktadır."
                );
                window.location="/siparisler";
            </script>
            """

        subeler = [
            (
                session["sube_id"],
                session["sube_adi"]
            )
        ]

    urunler = get_tum_urunler()

    # ==============================
    # ŞUBE FİNANS LİMİTİ
    # ==============================

    if session["yetki"] == "admin":

        secili_sube = subeler[0][0]

    else:

        secili_sube = session["sube_id"]

    limit = get_sube_limit(
        secili_sube
    )

    return render_template(
        "yeni_siparis.html",
        subeler=subeler,
        urunler=urunler,
        limit=limit
    )


# ==================================
# ŞUBE LİMİT GETİRME (AJAX)
# ==================================

@app.route("/get-sube-limit/<int:sube_id>")
def get_sube_limit_ajax(sube_id):

    if "giris" not in session:
        return {
            "limit": 0
        }

    limit = get_sube_limit(
        sube_id
    )

    return {
        "limit": limit
    }


# ======================================
# STOKLAR
# ======================================

@app.route("/stoklar")
def stoklar():

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    # ==================================
    # FİLTRELER
    # ==================================

    baslangic = request.args.get(
        "baslangic",
        ""
    )

    bitis = request.args.get(
        "bitis",
        ""
    )

    sube_id = request.args.get(
        "sube_id",
        ""
    )

    urun_id = request.args.get(
        "urun_id",
        ""
    )

    hareket_tipi = request.args.get(
        "hareket_tipi",
        ""
    )

    arama = request.args.get(
        "arama",
        ""
    )

    # ==================================
    # BOŞ DEĞERLERİ NONE YAP
    # ==================================

    sube_id = (
        int(sube_id)
        if sube_id
        else None
    )

    urun_id = (
        int(urun_id)
        if urun_id
        else None
    )

    # ==================================
    # MERKEZ STOKLARI
    # ==================================

    merkez_stok = get_merkez_stok()

    # ==================================
    # ŞUBE STOKLARI
    # ==================================

    sube_stoklari = get_sube_stoklari()

    # ==================================
    # STOK HAREKETLERİ
    # ==================================

    stok_hareketleri = get_stok_hareketleri(
        baslangic or None,
        bitis or None,
        sube_id,
        urun_id,
        hareket_tipi or None,
        arama.strip() or None
    )

    # ==================================
    # FİLTRE SEÇENEKLERİ
    # ==================================

    filtre_subeler = get_tum_subeler()

    filtre_urunler = get_tum_urunler()

    return render_template(
        "stoklar.html",
        merkez_stok=merkez_stok,
        sube_stoklari=sube_stoklari,
        stok_hareketleri=stok_hareketleri,
        filtre_subeler=filtre_subeler,
        filtre_urunler=filtre_urunler,
        baslangic=baslangic,
        bitis=bitis,
        secili_sube=sube_id,
        secili_urun=urun_id,
        secili_hareket=hareket_tipi,
        arama=arama
    )


# ======================================
# SEVKİYAT PROGRAMI
# ======================================

@app.route("/sevkiyat")
def sevkiyat():

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    # ==================================
    # FİLTRELER
    # ==================================

    baslangic = request.args.get(
        "baslangic",
        ""
    )

    bitis = request.args.get(
        "bitis",
        ""
    )

    sube_id = request.args.get(
        "sube_id",
        ""
    )

    firma = request.args.get(
        "firma",
        ""
    )

    # ==================================
    # BOŞ DEĞERLERİ NONE YAP
    # ==================================

    sube_id = (
        int(sube_id)
        if sube_id
        else None
    )

    # ==================================
    # SEVKİYAT PROGRAMI
    # ==================================

    sevkiyatlar = get_sevkiyat_programi(
        baslangic=baslangic or None,
        bitis=bitis or None,
        sube_id=sube_id,
        firma=firma or None
    )

    # ==================================
    # FİLTRE SEÇENEKLERİ
    # ==================================

    filtre_subeler = get_tum_subeler()

    # ==================================
    # SAYFAYI GÖSTER
    # ==================================

    return render_template(
        "sevkiyat.html",
        sevkiyatlar=sevkiyatlar,
        filtre_subeler=filtre_subeler,
        baslangic=baslangic,
        bitis=bitis,
        secili_sube=sube_id,
        secili_firma=firma
    )


# ======================================
# ŞUBE SATIŞ EXCEL AKTARIMI
# ======================================

@app.route(
    "/sube-satis-aktar",
    methods=["POST"]
)
def sube_satis_aktar():

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    dosya = request.files.get("dosya")

    if not dosya or dosya.filename == "":

        return """
        <script>
            alert("Lütfen Excel dosyası seçin.");
            window.location="/stoklar";
        </script>
        """

    try:

        wb = openpyxl.load_workbook(
            dosya,
            data_only=True
        )

        ws = wb.active

        # ======================================
        # EXCEL BAŞLIKLARI
        # ======================================

        basliklar = []

        for hucre in ws[1]:

            if hucre.value is not None:

                basliklar.append(
                    str(hucre.value).strip()
                )

            else:

                basliklar.append("")

        # ======================================
        # GEREKLİ SÜTUN KONTROLÜ
        # ======================================

        gerekli_basliklar = [
            "Şube",
            "Ürün Adı",
            "Satış Miktarı"
        ]

        for baslik in gerekli_basliklar:

            if baslik not in basliklar:

                return f"""
                <script>

                    alert(
                        "Excel formatı hatalı.\\n\\n" +
                        "Eksik sütun: {baslik}\\n\\n" +
                        "Gerekli sütunlar:\\n" +
                        "Şube\\n" +
                        "Ürün Adı\\n" +
                        "Satış Miktarı"
                    );

                    window.location="/stoklar";

                </script>
                """

        # ======================================
        # SÜTUNLARIN YERLERİNİ BUL
        # ======================================

        sube_index = basliklar.index("Şube")

        urun_index = basliklar.index("Ürün Adı")

        miktar_index = basliklar.index(
            "Satış Miktarı"
        )

        # ======================================
        # SONUÇ SAYACI
        # ======================================

        basarili = 0
        hatali = 0

        # ======================================
        # EXCEL SATIRLARINI OKU
        # ======================================

        for satir in ws.iter_rows(
            min_row=2,
            values_only=True
        ):

            # Satır uzunluğu kontrolü

            if len(satir) <= max(
                sube_index,
                urun_index,
                miktar_index
            ):

                hatali += 1
                continue

            sube_adi = satir[sube_index]

            urun_adi = satir[urun_index]

            miktar = satir[miktar_index]

            # ==================================
            # BOŞ SATIRLARI GEÇ
            # ==================================

            if (
                sube_adi is None
                or urun_adi is None
                or miktar is None
            ):

                continue

            # ==================================
            # MİKTAR KONTROLÜ
            # ==================================

            try:

                miktar = float(miktar)

            except:

                hatali += 1
                continue

            if miktar <= 0:

                hatali += 1
                continue

            # ==================================
            # ŞUBE + ÜRÜN EŞLEŞTİR
            # ==================================

            eslesme = get_sube_urun_id(
                str(sube_adi).strip(),
                str(urun_adi).strip()
            )

            if not eslesme:

                hatali += 1
                continue

            sube_id = eslesme[0]

            urun_id = eslesme[1]

            # ==================================
            # ŞUBE STOKTAN SATIŞI DÜŞ
            # ==================================

            sube_stok_azalt(
                sube_id,
                urun_id,
                miktar
            )

            basarili += 1

        # ======================================
        # AKTARIM SONUCU
        # ======================================

        return f"""
        <script>

            alert(
                "Satış aktarımı tamamlandı.\\n\\n" +
                "Başarılı kayıt: {basarili}\\n" +
                "Hatalı kayıt: {hatali}"
            );

            window.location="/stoklar";

        </script>
        """

    except Exception as e:

        return f"""
        <script>

            alert(
                "Excel aktarılırken hata oluştu:\\n\\n{str(e)}"
            );

            window.location="/stoklar";

        </script>
        """


# ==========================
# EXCEL RAPOR
# ==========================

@app.route("/excel-rapor")
def excel_rapor():

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    wb = Workbook()

    ws = wb.active

    ws.title = "Şube Siparişleri"

    urunler = get_tum_urunler()

    subeler = get_tum_subeler()

    # ==================================
    # BAŞLIK
    # ==================================

    ws["A1"] = "Ürün"

    sutun = 2

    for sube in subeler:

        hucre = ws.cell(
            row=1,
            column=sutun
        )

        hucre.value = sube[1]

        hucre.font = Font(
            bold=True
        )

        hucre.fill = PatternFill(
            fill_type="solid",
            fgColor="D9EAD3"
        )

        hucre.alignment = Alignment(
            horizontal="center"
        )

        sutun += 1

    # ==================================
    # ÜRÜNLER
    # ==================================

    satir = 2

    for urun in urunler:

        ws.cell(
            row=satir,
            column=1
        ).value = urun[1]

        sutun = 2

        for sube in subeler:

            miktar = get_siparis_miktari(
                sube[0],
                urun[0]
            )

            ws.cell(
                row=satir,
                column=sutun
            ).value = miktar

            sutun += 1

        satir += 1

    # ==================================
    # EXCEL DOSYASI OLUŞTUR
    # ==================================

    dosya = BytesIO()

    wb.save(dosya)

    dosya.seek(0)

    return send_file(
        dosya,
        as_attachment=True,
        download_name="Siparis_Raporu.xlsx",
        mimetype=(
            "application/"
            "vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )


# ==========================
# UYGULAMA BAŞLAT
# ==========================

import os

print(
    "Login fonksiyonu =",
    login
)

print(
    "Endpoint =",
    app.view_functions["login"]
)

print("\n===== ROUTES =====")

for rule in app.url_map.iter_rules():

    print(
        rule,
        rule.methods
    )

print("==================\n")


# ======================================
# VERİTABANINI OLUŞTUR / GÜNCELLE
# ======================================

create_tables()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
    