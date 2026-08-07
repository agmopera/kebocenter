from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    abort,
    flash,
    send_file
)

print("MAIN DOSYASI ÇALIŞTI")

from datetime import datetime
import json
import random

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

from io import BytesIO


from database import (

    create_tables,

    add_sube,
    get_subeler,
    get_sube,
    update_sube,
    delete_sube,

    add_urun,
    get_urunler,
    get_urun,
    update_urun,
    delete_urun,

    add_siparis,
    add_siparis_detay,
    get_siparisler,
    get_sube_siparisleri,
    get_onay_bekleyen_siparisler,
    get_siparis,
    get_siparis_detaylari,
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
    get_finans_urunleri,
    get_finans_subeleri,
    fiyat_guncelle,
    limit_guncelle,
    aktif_siparis_var_mi,
    get_sube_limit,
    siparise_urun_ekle,
    sipariste_urun_var_mi,
    toplam_koli,

    login_kontrol,

    # Dashboard
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
    print("METHOD:", request.method, "URL:", request.path)

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
    methods=["GET","POST"]
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


@app.route("/raporlar")
def raporlar():

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    return render_template("raporlar.html")


@app.route("/ai")
def ai():

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    return render_template("ai.html")


@app.route("/stoklar")
def stoklar():

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc

    return render_template("stoklar.html")




@app.route("/yeni-urun", methods=["GET", "POST"])
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
    request.form.get("koli_agirligi",0)

)


        return redirect("/urunler")



    return render_template(
        "yeni_urun.html"
    )







@app.route(
    "/urun-duzenle/<int:id>",
    methods=["GET","POST"]
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

@app.route("/siparis-durum/<int:id>", methods=["POST"])
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
        tarih=datetime.now().strftime("%d.%m.%Y %H:%M"),
        kullanici=session["sube_adi"],
        eski_durum=eski_durum,
        yeni_durum=yeni_durum
    )

    return redirect("/siparisler")

# ==========================
# ADMIN SİPARİŞ ONAY
# ==========================

@app.route("/siparis-onayla/<int:id>")
def siparis_onayla(id):

    sonuc = admin_kontrol()

    if sonuc:
        return sonuc


    siparis_durum_guncelle(
        id,
        "Onaylandı"
    )


    return redirect("/siparisler")
    



@app.route("/siparis-duzenle/<int:id>", methods=["GET", "POST"])
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







@app.route(
    "/yeni-siparis",
    methods=["GET","POST"]
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



        tarih = datetime.now().strftime("%Y-%m-%d")


        urunler_json = request.form["urunler_json"]


        urun_listesi = json.loads(
            urunler_json
        )



        siparis_no = (
            "SP-"
            + datetime.now().strftime("%Y%m%d")
            + "-"
            + str(random.randint(1000,9999))
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
        if aktif_siparis_var_mi(session["sube_id"]):

            return """
    <script>
        alert("Bu hafta zaten aktif bir siparişiniz bulunmaktadır.");
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

    limit = get_sube_limit(secili_sube)

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
        return {"limit":0}


    limit = get_sube_limit(
        sube_id
    )


    return {
        "limit": limit
    }

# ==========================
# UYGULAMA BAŞLAT
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

    # Başlık
    ws["A1"] = "Ürün"

    sutun = 2

    for sube in subeler:

        hucre = ws.cell(row=1, column=sutun)

        hucre.value = sube[1]
        hucre.font = Font(bold=True)
        hucre.fill = PatternFill(
            fill_type="solid",
            fgColor="D9EAD3"
        )
        hucre.alignment = Alignment(horizontal="center")

        sutun += 1

    satir = 2

    for urun in urunler:

        ws.cell(row=satir, column=1).value = urun[1]

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

    dosya = BytesIO()

    wb.save(dosya)

    dosya.seek(0)



    return send_file(
        dosya,
        as_attachment=True,
        download_name="Siparis_Raporu.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


import os

print("Login fonksiyonu =", login)
print("Endpoint =", app.view_functions["login"])

print("\n===== ROUTES =====")

for rule in app.url_map.iter_rules():
    print(rule, rule.methods)

print("==================\n")

# Veritabanını oluştur / güncelle
create_tables()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

