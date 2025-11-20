# -*- coding: utf-8 -*-
"""
Updated for 2025 - Yandex Images - Extract real image URLs
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import requests
import io
from PIL import Image
import re
from urllib.parse import unquote, urlparse, parse_qs

class YandexImageScraper():
    def __init__(self, webdriver_path, image_path, search_key="cat", number_of_images=1, headless=True, min_resolution=(0, 0), max_resolution=(1920, 1080), max_missed=10):
        
        safe_folder_name = search_key.replace(":", " ").replace("/", " ").replace("\\", " ").strip()
        safe_folder_name = " ".join(safe_folder_name.split())
        image_path = os.path.join(image_path, safe_folder_name)

        if (type(number_of_images)!=int):
            print("[Error] Number of images must be integer value.")
            return
        if not os.path.exists(image_path):
            print(f"[INFO] Image path not found. Creating a new folder: {image_path}")
            os.makedirs(image_path)
            
        if not os.path.isfile(webdriver_path):
            exit("[ERR] ChromeDriver not found!")

        try:
            options = Options()
            if(headless):
                options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            driver = webdriver.Chrome(webdriver_path, options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
        except Exception as e:
            print(f"[ERR] ChromeDriver error: {e}")
            exit("[ERR] ChromeDriver issue!")

        self.driver = driver
        self.search_key = search_key
        self.number_of_images = number_of_images
        self.image_path = image_path
        self.url = "https://yandex.com/images/search?text=%s"%(search_key)
        self.headless = headless
        self.min_resolution = min_resolution
        self.max_resolution = max_resolution

    def extract_real_url(self, yandex_url):
        """Yandex arama URL'sinden gerçek resim URL'sini çıkar"""
        try:
            # URL'den img_url parametresini çıkar
            if 'img_url=' in yandex_url:
                parsed = urlparse(yandex_url)
                params = parse_qs(parsed.query)
                
                if 'img_url' in params:
                    # URL decode et
                    real_url = unquote(params['img_url'][0])
                    return real_url
            
            return None
        except:
            return None

    def find_image_urls(self):
        print("[INFO] Gathering image links from Yandex")
        print(f"[INFO] Loading: {self.url}")
        
        self.driver.get(self.url)
        time.sleep(5)
        
        print(f"[DEBUG] Page title: {self.driver.title}")
        
        image_urls = set()
        scroll_count = 0
        max_scrolls = 50
        
        print("[INFO] Starting to collect images...")
        
        while len(image_urls) < self.number_of_images and scroll_count < max_scrolls:
            try:
                # METHOD 1: Link elementlerinden gerçek URL'leri çıkar
                links = self.driver.find_elements(By.TAG_NAME, "a")
                
                for link in links:
                    if len(image_urls) >= self.number_of_images:
                        break
                    
                    href = link.get_attribute('href')
                    if href and 'img_url=' in href:
                        # Gerçek resim URL'sini çıkar
                        real_url = self.extract_real_url(href)
                        
                        if real_url and len(real_url) > 50:
                            # Geçerli bir resim URL'si mi kontrol et
                            if any(ext in real_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                                if real_url not in image_urls:
                                    image_urls.add(real_url)
                                    print(f"[INFO] #{len(image_urls)}: {real_url[:90]}...")
                
                # METHOD 2: Sayfa kaynağından direkt img_url parametrelerini çıkar
                page_source = self.driver.page_source
                
                # img_url parametrelerini bul
                pattern = r'img_url=([^&"\']+)'
                matches = re.findall(pattern, page_source)
                
                for match in matches:
                    if len(image_urls) >= self.number_of_images:
                        break
                    
                    # URL decode et
                    real_url = unquote(match)
                    
                    if len(real_url) > 50 and real_url not in image_urls:
                        if any(ext in real_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                            # URL'yi temizle
                            real_url = real_url.split('&')[0]  # Sonraki parametreleri kaldır
                            
                            image_urls.add(real_url)
                            print(f"[INFO] #{len(image_urls)}: {real_url[:90]}...")
                
                # METHOD 3: JSON formatından URL'leri çıkar
                json_pattern = r'"url":"(https?://[^"]*?\.(?:jpg|jpeg|png|webp)[^"]*?)"'
                json_matches = re.findall(json_pattern, page_source, re.IGNORECASE)
                
                for match in json_matches:
                    if len(image_urls) >= self.number_of_images:
                        break
                    
                    url = match.replace('\\/', '/')
                    
                    if len(url) > 50 and url not in image_urls:
                        image_urls.add(url)
                        print(f"[INFO] #{len(image_urls)}: {url[:90]}...")
                
                # Scroll yap
                self.driver.execute_script("window.scrollBy(0, 800);")
                time.sleep(1.5)
                scroll_count += 1
                
                if scroll_count % 5 == 0:
                    print(f"[INFO] Scrolled {scroll_count} times, found {len(image_urls)} unique images")
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                
                if len(image_urls) >= self.number_of_images:
                    print(f"[SUCCESS] Collected {len(image_urls)} image URLs!")
                    break
                    
            except Exception as e:
                print(f"[ERROR] Loop error: {e}")
                scroll_count += 1
        
        print(f"\n[FINAL] Total unique URLs found: {len(image_urls)}")
        
        if len(image_urls) == 0:
            print("[WARNING] No images found!")
        
        self.driver.quit()
        return list(image_urls)[:self.number_of_images]

    def save_images(self, image_urls, keep_filenames):
        if len(image_urls) == 0:
            print("[WARNING] No URLs to download!")
            return
            
        print(f"\n[INFO] Starting download of {len(image_urls)} images...")
        saved_count = 0
        failed_count = 0
        
        for indx, image_url in enumerate(image_urls):
            try:
                print(f"[{indx+1}/{len(image_urls)}] Downloading: {image_url[:80]}...")
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                    'Referer': 'https://yandex.com/'
                }
                
                response = requests.get(image_url, timeout=15, headers=headers, allow_redirects=True)
                
                if response.status_code == 200:
                    try:
                        image_from_web = Image.open(io.BytesIO(response.content))
                        
                        # Dosya adı oluştur
                        search_string = ''.join(e for e in self.search_key if e.isalnum())
                        
                        if keep_filenames:
                            name = os.path.splitext(os.path.basename(urlparse(image_url).path))[0]
                            name = re.sub(r'[<>:"/\\|?*]', '', name)[:50]
                            filename = f"{name}.{image_from_web.format.lower()}"
                        else:
                            filename = f"{search_string}{indx:04d}.{image_from_web.format.lower()}"
                        
                        image_path = os.path.join(self.image_path, filename)
                        
                        # RGBA -> RGB dönüşümü
                        if image_from_web.mode == 'RGBA':
                            rgb_im = image_from_web.convert('RGB')
                            rgb_im.save(image_path)
                        else:
                            image_from_web.save(image_path)
                        
                        width, height = image_from_web.size
                        
                        # Çözünürlük kontrolü
                        if (width >= self.min_resolution[0] and 
                            height >= self.min_resolution[1] and
                            width <= self.max_resolution[0] and 
                            height <= self.max_resolution[1]):
                            print(f"[OK] Saved: {filename} ({width}x{height})")
                            saved_count += 1
                        else:
                            os.remove(image_path)
                            print(f"[SKIP] Resolution {width}x{height} outside bounds")
                            failed_count += 1
                        
                        image_from_web.close()
                        
                    except Exception as img_error:
                        print(f"[ERROR] Image processing failed: {str(img_error)[:50]}")
                        failed_count += 1
                else:
                    print(f"[ERROR] HTTP {response.status_code}")
                    failed_count += 1
                    
            except Exception as e:
                print(f"[ERROR] Download failed: {str(e)[:50]}")
                failed_count += 1
        
        print(f"\n{'='*60}")
        print(f"[COMPLETE] Successfully saved: {saved_count}/{len(image_urls)} images")
        print(f"[INFO] Failed/Skipped: {failed_count}")
        print(f"{'='*60}\n")