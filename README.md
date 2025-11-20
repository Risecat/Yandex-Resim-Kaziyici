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

### 1. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 2. Web Driver'ı İndirin

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

### 3. Arama Ayarlarını Düzenleyin

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

### Diğer Parametreler

```python
number_of_images = 300          # Yandex'ten indirilecek görsel sayısı
headless = False                # True = Arka planda çalışır (Chrome GUI yok)
min_resolution = (0, 0)         # Minimum çözünürlük
max_resolution = (9999, 9999)   # Maximum çözünürlük
max_missed = 300                # Maksimum başarısız deneme sayısı
number_of_workers = 1           # Thread sayısı
keep_filenames = False          # Orijinal dosya isimlerini koru
```

## Kullanım

1. Terminali (PowerShell veya CMD) açın
2. Proje klasörüne gidin:
   ```bash
   cd C:\Users\KULLANICI_ADINIZ\OneDrive\Masaüstü\Yandex-Image-Scraper
   ```
3. Programı çalıştırın:
   ```bash
   python main.py
   ```

## Özellikler

- **Sınırsız Scroll**: Yandex'te scroll limiti olmadığı için istediğiniz kadar görsel toplayabilirsiniz
- **Otomatik Klasörleme**: Her arama için ayrı klasör oluşturur (örn: `galata kulesi/`)
- **Chrome WebDriver**: Güvenilir Google Chrome tarayıcısını kullanır
- **Akıllı Filtreleme**: Thumbnail'leri ve küçük görselleri otomatik filtreler

## Nasıl Çalışır?

1. Chrome tarayıcı açılır
2. Yandex Görseller'e gidilir (`https://yandex.com.tr/gorsel/`)
3. Arama yapılır
4. Sayfa sürekli aşağı kaydırılır
5. Her scroll'da yeni görseller toplanır
6. İstenen sayıya ulaşılana kadar devam edilir

## Sorun Giderme

### Web Driver Hatası

Eğer "Web Driver version mismatch" hatası alırsanız:

1. Chrome sürümünüzü kontrol edin (`chrome://version/`)
2. Tam olarak aynı sürümdeki Web Driver'ı indirin
3. `webdriver/` klasörüne doğru şekilde yerleştirin

### Görsel Bulunamıyor

- `headless = False` yaparak Chrome penceresini görebilirsiniz
- `number_of_images` değerini düşürmeyi deneyin
- İnternet bağlantınızı kontrol edin

## Not

- Program komut satırından çalıştırılmalıdır
- İndirilen görseller `photos/` klasörüne site bazlı kategorize edilir
- Web Driver sürümü Chrome tarayıcı sürümü ile uyumlu olmalıdır
