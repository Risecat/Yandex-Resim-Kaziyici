# Yandex Image Scraper - Sınırsız Scroll

Yandex Görseller'den sınırsız scroll ile görsel toplama aracı.<br>
Google Chrome WebDriver kullanarak Yandex arama motorunda işlem yapar.<br>
Orijinal depo: https://github.com/ohyicong/Google-Image-Scraper

## Yandex'in Avantajı

Yandex Görseller'de scroll limiti yoktur. Google'dan farklı olarak istediğiniz kadar aşağı inebilir ve binlerce görsel toplayabilirsiniz!

## Gereksinimler

1. Google Chrome
2. Python 3
3. Windows OS

## Kurulum

### 1. Projeyi İndirin

```bash
git https://github.com/Risecat/Yandex-Resim-Kaziyici
cd Yandex-Resim-Kaziyici
```

### 2. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 3. Web Driver'ı İndirin

**Önemli:** Web Driver sürümü, bilgisayarınızdaki Chrome tarayıcı sürümü ile aynı olmalıdır.

1. Chrome'da arama çubuğuna `chrome://version/` yazın
2. Sürüm numarasını not edin (örn: `142.0.7444.176`)
3. Aşağıdaki linki kendi sürümünüzle değiştirerek tarayıcınıza yapıştırın:
   ```
   https://storage.googleapis.com/chrome-for-testing-public/{SÜRÜMÜNÜZ}/win64/chromedriver-win64.zip
   ```
   **Örnek:**
   ```
   https://storage.googleapis.com/chrome-for-testing-public/142.0.7444.176/win64/chromedriver-win64.zip
   ```
4. İndirilen ZIP dosyasını açın
5. İçindeki `chromedriver.exe` dosyasını projenin `webdriver/` klasörüne kopyalayın

### 4. Arama Ayarlarını Düzenleyin

`main.py` dosyasını açın ve aşağıdaki ayarları düzenleyin:

### Arama Ayarları

```python
# Aramak istediğin kelimeler/nesneler
search_keys = [
    "galata kulesi",
    "kız kulesi",
    "kamondo merdivenleri"
]
```

### Parametreler

```python
number_of_images = 1200            # İstenilen resim miktarı
headless = False                   # True = Arka planda çalışır (Robot musunuz sorusu için False önerilir)
min_resolution = (320, 320)        # Minimum çözünürlük
max_resolution = (9999, 9999)      # Maximum çözünürlük
allowed_formats = ['.jpg', '.jpeg', '.webp']  # İzin verilen dosya formatları
max_missed = 750                   # Maksimum başarısız deneme sayısı
number_of_workers = 1              # Thread sayısı
keep_filenames = False             # Orijinal dosya isimlerini koru

# Sayfalandırma Ayarları
enable_pagination = True           # Sayfa geçişi aktif/pasif (&p=2, &p=3...)
max_scrolls = 1000                 # Her sayfada maksimum kaç kez scroll yapılacak
no_image_threshold = 10            # Kaç kez resim bulunamazsa sonraki sayfaya geç
```

#### Sayfalandırma Nedir?

- **`enable_pagination = True`**: Hedef sayıya ulaşana kadar sayfalar arası geçiş yapar. Her sayfa ayrı klasöre kaydedilir (`Page_1/`, `Page_2/`, `Page_3/`...)
- **`enable_pagination = False`**: Sadece ilk sayfadan resim toplar

#### İzin Verilen Formatlar

`allowed_formats` parametresi ile hangi dosya formatlarının indirileceğini belirleyebilirsiniz:

```python
allowed_formats = ['.jpg', '.jpeg', '.webp']  # Sadece bu formatlar indirilir
allowed_formats = ['.jpg', '.png', '.webp', '.gif']  # Daha fazla format
```

## Kullanım

1. Terminali (PowerShell veya CMD) açın
2. Proje klasörüne gidin:
   ```bash
   cd Yandex-Image-Scraper
   ```
3. Programı çalıştırın:
   ```bash
   python main.py
   ```

## Özellikler

- **Sınırsız Scroll**: Yandex'te scroll limiti olmadığı için istediğiniz kadar görsel toplayabilirsiniz
- **Sayfalandırma**: Her sayfa için ayrı klasörlerde organizasyon (`Page_1/`, `Page_2/`...)
- **Otomatik Klasörleme**: Her arama için ayrı klasör oluşturur (örn: `galata kulesi/`)
- **Chrome WebDriver**: Güvenilir Google Chrome tarayıcısını kullanır
- **Akıllı Filtreleme**: Çözünürlük ve format filtresi ile istenmeyen görselleri otomatik filtreler
- **Format Kontrolü**: İndirmeden önce dosya formatını kontrol eder

## Nasıl Çalışır?

1. Chrome tarayıcı açılır
2. Yandex Görseller'e gidilir (`https://yandex.com/images/`)
3. Arama yapılır
4. Sayfa sürekli aşağı kaydırılır
5. Her scroll'da yeni görseller toplanır
6. `no_image_threshold` kez resim bulunamazsa sonraki sayfaya geçilir (pagination aktifse)
7. İstenen sayıya ulaşılana kadar devam edilir

## Sorun Giderme

### Web Driver Hatası

Eğer "Web Driver version mismatch" hatası alırsanız:

1. Chrome sürümünüzü kontrol edin (`chrome://version/`)
2. Tam olarak aynı sürümdeki Web Driver'ı indirin
3. `webdriver/` klasörüne doğru şekilde yerleştirin

### Görsel Bulunamıyor

- `headless = False` yaparak Chrome penceresini görebilirsiniz
- `number_of_images` değerini düşürmeyi deneyin
- `enable_pagination = True` yapın
- İnternet bağlantınızı kontrol edin

### "Robot musunuz?" Sorusu

- **Önemli:** `headless = False` olarak ayarlayın
- Manuel olarak captcha'yı çözün
- Program otomatik devam edecektir

## Not

- Program komut satırından çalıştırılmalıdır
- İndirilen görseller `photos/` klasörüne kategorize edilir
- Web Driver sürümü Chrome tarayıcı sürümü ile uyumlu olmalıdır
- Sayfalandırma aktifse her sayfa ayrı klasöre kaydedilir
- `allowed_formats` ile sadece istediğiniz formatlardaki görseller indirilir
