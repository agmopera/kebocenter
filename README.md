# Sipariş Yönetim Sistemi

Bu proje, profesyonel bir sipariş yönetim sisteminin temeli oluşturmayı amaçlamaktadır.

## Kurulum ve Çalıştırma

1. Projeyi clonlayın veya indirin.
2. Ana klasörünüzde terminalden aşağıdaki komutları kullanarak gereken paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Uygulamayı çalıştırmak için `app.py` dosyasını çalıştırın:
   ```bash
   python app.py
   ```

## Klasör Yapısı

- **SiparisSistemi/**: Ana proje klasörü.
  - **app.py**: Flask uygulaması başlangıcı.
  - **database/**: Veritabanı modülleri.
    - **\_\_init\_\_.py**: Veritabanı konfigürasyonu.
  - **static/**: Statik dosyalar (CSS, JS).
    - **css/**: CSS dosyaları.
      - **style.css**: Genel stili tanımlayan minimal bir CSS.
    - **js/**: JavaScript dosyaları.
      - **script.js**: Önceden boş bırakılmış.
  - **images/**: Görüntüler.
  - **templates/**: HTML şablonları.
    - **login.html**: Giriş sayfası.
    - **dashboard.html**: Ana panel sayfası.
  - **requirements.txt**: Gereken paketlerin listesi.
  - **README.md**: Projenin genel yapısı ve kurulum bilgileri.

Bu dosyalar, uygulamanın temeli oluşturur. Sipariş yönetim özelliklerinin eklenmesi için bu yapıyı kullanabilirsiniz.