# -*- coding: utf-8 -*-
"""
Updated for Yandex Image Search with Pagination Support
"""
import os
import concurrent.futures
from GoogleImageScraper import YandexImageScraper

def worker_thread(search_key):
    image_scraper = YandexImageScraper(
        webdriver_path, 
        image_path, 
        search_key, 
        number_of_images, 
        headless, 
        min_resolution, 
        max_resolution, 
        max_missed,
        enable_pagination,  # Sayfalandırma
        max_scrolls,        # Maksimum scroll sayısı
        no_image_threshold, # Bulunamama eşiği
        allowed_formats)    # İzin verilen formatlar (YENİ)
    
    image_urls = image_scraper.find_image_urls()
    
    print(f"\n[DEBUG] '{search_key}' için toplam {len(image_urls)} URL bulundu")
    
    # find_image_urls artık hem toplama hem kaydetme işini yapıyor
    # Sayfalandırma aktifse her sayfa kendi klasörüne kaydediliyor

    del image_scraper

if __name__ == "__main__":
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', 'chromedriver.exe'))
    image_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))

    # ARAMA AYARLARI
    search_keys = [
        #"kız kulesi",
        "galata kulesi",
        #"kamondo merdivenleri",
    ]

    # Parameters
    number_of_images = 1200             # İstediğiniz toplam resim sayısı
    headless = False                   # Chrome'u görmek için False (Robot musunuz sorusu için False önerilir)
    min_resolution = (320, 320)        # Minimum çözünürlük
    allowed_formats = ['.jpg', '.jpeg', '.webp']  # İzin verilen formatlar
    max_resolution = (9999, 9999)
    max_missed = 750                   # Maksimum başarısız deneme sayısı
    number_of_workers = 1              # Tek seferde bir arama
    keep_filenames = False             # Orijinal dosya adlarını koru
    enable_pagination = True           # True ise, hedef sayıya ulaşana kadar sayfalar arasında gezinir her sayfa "Page_1","Page_2", "Page_3" vb. klasörlere kaydedilir
    
    # SCROLL VE BULUNAMAMA AYARLARI (YENİ)
    max_scrolls = 1000                 # Maksimum kaç kez scroll yapılacak
    no_image_threshold = 10            #Kaç kez üst üste resim bulunamazsa sonraki sayfaya geçilir (varsayılan: 10)

    print("=" * 60)
    print("YANDEX IMAGE SCRAPER - PAGINATION SUPPORT")
    print("=" * 60)
    print(f"Search queries: {search_keys}")
    print(f"Images per query: {number_of_images}")
    print(f"Headless mode: {headless}")
    print(f"Min resolution: {min_resolution}")
    print(f"Pagination enabled: {enable_pagination}")
    print(f"Max scrolls per page: {max_scrolls}")
    print(f"No image threshold: {no_image_threshold}")
    print(f"Allowed formats: {allowed_formats}")
    print("=" * 60)
    print()

    # Tek tek çalıştır (debug için daha iyi)
    for search_key in search_keys:
        print(f"\n{'='*60}")
        print(f"Processing: {search_key}")
        print(f"{'='*60}\n")
        worker_thread(search_key)
    
    print("\n" + "=" * 60)
    print("ALL DOWNLOADS COMPLETED!")
    print("=" * 60)