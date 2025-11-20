# -*- coding: utf-8 -*-
"""
Updated for Yandex Image Search
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
        max_missed)
    image_urls = image_scraper.find_image_urls()
    
    print(f"\n[DEBUG] Found {len(image_urls)} URLs for '{search_key}'")
    
    if len(image_urls) > 0:
        image_scraper.save_images(image_urls, keep_filenames)
    else:
        print(f"[WARNING] No images found for '{search_key}', skipping download phase")

    del image_scraper

if __name__ == "__main__":
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', 'chromedriver.exe'))
    image_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))

    # ARAMA AYARLARI
    search_keys = [
        #"galata kulesi",
        #"kız kulesi",
        "kamondo merdivenleri"
    ]

    # Parameters
    number_of_images = 300           # İlk teste için düşük tutalım
    headless = False                # Chrome'u görmek için False
    min_resolution = (400, 400)     # Minimum çözünürlük
    max_resolution = (9999, 9999)
    max_missed = 300
    number_of_workers = 1           # Tek seferde bir arama
    keep_filenames = False

    print("=" * 60)
    print("YANDEX IMAGE SCRAPER")
    print("=" * 60)
    print(f"Search queries: {search_keys}")
    print(f"Images per query: {number_of_images}")
    print(f"Headless mode: {headless}")
    print(f"Min resolution: {min_resolution}")
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