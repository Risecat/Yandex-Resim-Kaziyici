# -*- coding: utf-8 -*-
"""
GERÇEK ZAMANLI VERSİYON - Bul → Hemen İndir
Link bulunduğu anda indirilir, gerçek ilerleme gösterilir
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import requests
import io
from PIL import Image
import re
from urllib.parse import unquote, urlparse, parse_qs

class YandexImageScraper():
    def __init__(self, webdriver_path, image_path, search_key="cat", number_of_images=1, 
                 headless=True, min_resolution=(0, 0), max_resolution=(1920, 1080), 
                 max_missed=10, enable_pagination=False, max_scrolls=3000, 
                 no_image_threshold=10, allowed_formats=None):
        
        safe_folder_name = search_key.replace(":", " ").replace("/", " ").replace("\\", " ").strip()
        safe_folder_name = " ".join(safe_folder_name.split())
        self.base_image_path = os.path.join(image_path, safe_folder_name)

        if not os.path.exists(self.base_image_path):
            print(f"[INFO] Klasör oluşturuluyor: {self.base_image_path}")
            os.makedirs(self.base_image_path)
            
        if not os.path.isfile(webdriver_path):
            exit("[ERR] ChromeDriver bulunamadı!")

        try:
            options = Options()
            if headless:
                options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            driver = webdriver.Chrome(webdriver_path, options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
        except Exception as e:
            print(f"[ERR] ChromeDriver hatası: {e}")
            exit("[ERR] ChromeDriver başlatılamadı!")

        self.driver = driver
        self.search_key = search_key
        self.number_of_images = number_of_images
        self.base_url = f"https://yandex.com.tr/gorsel/search?from=tabbar&text={search_key}"
        self.headless = headless
        self.min_resolution = min_resolution
        self.max_resolution = max_resolution
        self.enable_pagination = enable_pagination
        self.current_page = 1
        self.max_scrolls = max_scrolls
        self.no_image_threshold = no_image_threshold
        self.allowed_formats = allowed_formats if allowed_formats else ['.jpg', '.jpeg', '.webp']
        self.allowed_formats = [fmt.lower() if fmt.startswith('.') else f'.{fmt.lower()}' for fmt in self.allowed_formats]
        
        # Zaten kullanılan URL'leri takip et
        self.tried_urls = set()

    def extract_real_url(self, yandex_url):
        try:
            if 'img_url=' in yandex_url:
                parsed = urlparse(yandex_url)
                params = parse_qs(parsed.query)
                if 'img_url' in params:
                    return unquote(params['img_url'][0])
            return None
        except:
            return None

    def try_click_load_more_button(self):
        try:
            load_more_selectors = [
                "button.FetchListButton-Button",
                "button.Button_view_action",
                "button[class*='FetchListButton']",
                "button[class*='LoadButton']",
                "button[class*='Button2_view_action']",
                ".FetchListButton",
                ".Button2_view_action"
            ]
            
            for selector in load_more_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in buttons:
                        try:
                            button_text = button.text.strip().lower()
                            if any(kw in button_text for kw in ['daha fazla', 'показать', 'show more', 'загрузить', 'more', 'load']):
                                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                                time.sleep(0.5)
                                try:
                                    button.click()
                                except:
                                    self.driver.execute_script("arguments[0].click();", button)
                                time.sleep(1)
                                return True
                        except:
                            continue
                except:
                    continue
            return False
        except:
            return False

    def find_image_urls(self):
        """🚀 GERÇEK ZAMANLI: Link bulunduğu anda indir"""
        saved_count = 0
        failed_count = 0
        format_rejected = 0
        scroll_count = 0
        no_new_url_count = 0
        
        # Sayfa klasörü
        page_folder = os.path.join(self.base_image_path, f"Page_{self.current_page}")
        if not os.path.exists(page_folder):
            os.makedirs(page_folder)
        
        # İlk sayfayı yükle
        self._load_page(self.current_page)
        
        print(f"\n{'='*60}")
        print(f"[INFO] HEDEF: {self.number_of_images} resim")
        print(f"[INFO] Yeni sürüm gerçek zamanlı mod")
        print(f"{'='*60}\n")
        
        while saved_count < self.number_of_images and scroll_count < self.max_scrolls:
            
            # Yeni URL'leri topla
            new_urls = self._extract_urls_from_page()
            
            # Yeni URL var mı?
            if len(new_urls) == 0:
                no_new_url_count += 1
                
                if no_new_url_count >= self.no_image_threshold:
                    print(f"\n[WARNING] {self.no_image_threshold} kez yeni URL bulunamadı")
                    
                    if self.enable_pagination:
                        print(f"[PAGINATION] Sayfa {self.current_page + 1}'e geçiliyor...")
                        self.current_page += 1
                        self.tried_urls.clear()
                        
                        # Yeni sayfa klasörü
                        page_folder = os.path.join(self.base_image_path, f"Page_{self.current_page}")
                        if not os.path.exists(page_folder):
                            os.makedirs(page_folder)
                        
                        self._load_page(self.current_page)
                        no_new_url_count = 0
                        scroll_count = 0
                        continue
                    else:
                        print("[INFO] Pagination kapalı, sonlandırılıyor.")
                        break
                
                # Scroll devam
                self._smart_scroll(scroll_count)
                scroll_count += 1
                
                # Butona tıkla
                if scroll_count % 3 == 0:
                    self.try_click_load_more_button()
                
                continue
            
            # Yeni URL'leri hemen indir
            no_new_url_count = 0
            
            for url in new_urls:
                if saved_count >= self.number_of_images:
                    break
                
                result = self._download_single_image(url, page_folder, saved_count)
                
                if result == "success":
                    saved_count += 1
                    print(f"✓ [{saved_count}/{self.number_of_images}] Kaydedildi!")
                elif result == "format_rejected":
                    format_rejected += 1
                    print(f"!  Format hatası (toplam: {format_rejected})")
                else:
                    failed_count += 1
                    print(f"✕ Başarısız (toplam: {failed_count})")
                
                # Hedef tamamlandı mı?
                if saved_count >= self.number_of_images:
                    print(f"\n{'='*60}")
                    print(f"➤ HEDEF TAMAMLANDI!")
                    print(f"✓ Kaydedilen: {saved_count}")
                    print(f"✕ Başarısız: {failed_count}")
                    print(f"!  Format hatası: {format_rejected}")
                    print(f"Sayfa: {self.current_page}")
                    print(f"{'='*60}\n")
                    self.driver.quit()
                    return []
            
            # Scroll devam
            self._smart_scroll(scroll_count)
            scroll_count += 1
            
            # Butona tıkla
            if scroll_count % 3 == 0:
                self.try_click_load_more_button()
        
        # Döngü bitti ama hedef tamamlanmadı
        print(f"\n{'='*60}")
        print(f"!  UYARI: Hedef tamamlanamadı")
        print(f"✓ Kaydedilen: {saved_count}/{self.number_of_images}")
        print(f"✕ Başarısız: {failed_count}")
        print(f"!  Format hatası: {format_rejected}")
        print(f"Sayfa: {self.current_page}")
        print(f"{'='*60}\n")
        
        self.driver.quit()
        return []

    def _load_page(self, page_number):
        """Belirtilen sayfayı yükle"""
        if page_number > 1:
            url = f"{self.base_url}&p={page_number}"
        else:
            url = self.base_url
        
        print(f"[INFO] Yükleniyor: {url}")
        self.driver.get(url)
        time.sleep(3)

    def _extract_urls_from_page(self):
        """Sayfadan henüz denenmemiş URL'leri çıkar"""
        new_urls = []
        
        try:
            # METHOD 1: Link elementleri
            links = self.driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute('href')
                if href and 'img_url=' in href:
                    real_url = self.extract_real_url(href)
                    if real_url and len(real_url) > 50 and real_url not in self.tried_urls:
                        new_urls.append(real_url)
                        self.tried_urls.add(real_url)
            
            # METHOD 2: Sayfa kaynağı regex
            page_source = self.driver.page_source
            pattern = r'img_url=([^&"\']+)'
            matches = re.findall(pattern, page_source)
            for match in matches:
                real_url = unquote(match).split('&')[0]
                if len(real_url) > 50 and real_url not in self.tried_urls:
                    new_urls.append(real_url)
                    self.tried_urls.add(real_url)
            
            # METHOD 3: JSON format
            json_pattern = r'"url":"(https?://[^"]*?\.(?:jpg|jpeg|png|webp|gif|bmp)[^"]*?)"'
            json_matches = re.findall(json_pattern, page_source, re.IGNORECASE)
            for match in json_matches:
                url_clean = match.replace('\\/', '/')
                if len(url_clean) > 50 and url_clean not in self.tried_urls:
                    new_urls.append(url_clean)
                    self.tried_urls.add(url_clean)
        
        except Exception as e:
            print(f"[ERROR] URL çıkarma hatası: {e}")
        
        return new_urls

    def _download_single_image(self, image_url, save_path, saved_count):
        """Tek bir resmi indir ve sonucu döndür"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Referer': 'https://yandex.com.tr/'
            }
            
            response = requests.get(image_url, timeout=10, headers=headers, allow_redirects=True)
            
            if response.status_code == 200:
                image_from_web = Image.open(io.BytesIO(response.content))
                
                # Format kontrolü
                image_format = image_from_web.format.lower() if image_from_web.format else 'unknown'
                allowed_format_names = [fmt.replace('.', '').lower() for fmt in self.allowed_formats]
                
                if image_format == 'jpeg':
                    image_format = 'jpg'
                
                if image_format not in allowed_format_names:
                    image_from_web.close()
                    return "format_rejected"
                
                # Çözünürlük kontrolü
                width, height = image_from_web.size
                if not (width >= self.min_resolution[0] and 
                        height >= self.min_resolution[1] and
                        width <= self.max_resolution[0] and 
                        height <= self.max_resolution[1]):
                    image_from_web.close()
                    return "resolution_rejected"
                
                # Dosya adı
                search_string = ''.join(e for e in self.search_key if e.isalnum())
                filename = f"{search_string}_{saved_count:04d}.{image_format}"
                image_path = os.path.join(save_path, filename)
                
                # Kaydet
                if image_from_web.mode == 'RGBA':
                    rgb_im = image_from_web.convert('RGB')
                    rgb_im.save(image_path)
                else:
                    image_from_web.save(image_path)
                
                image_from_web.close()
                return "success"
            else:
                return "http_error"
                
        except Exception as e:
            return "download_error"

    def _smart_scroll(self, scroll_count):
        """Akıllı scroll stratejisi"""
        try:
            if scroll_count % 10 == 0:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            elif scroll_count % 5 == 0:
                self.driver.execute_script("window.scrollBy(0, 2000);")
                time.sleep(1)
            else:
                self.driver.execute_script("window.scrollBy(0, 800);")
                time.sleep(0.5)
        except:
            pass