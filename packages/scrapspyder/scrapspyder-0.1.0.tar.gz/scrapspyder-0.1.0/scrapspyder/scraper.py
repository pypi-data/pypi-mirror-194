import os
import sys
import requests
import re
import logging
from bs4 import BeautifulSoup
from urllib.parse  import urljoin, urlparse, unquote

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

class Scraper:

    def __init__(self, source, dest=None, headers=None, deep_scan=False, depth=0, patterns_to_trim=None, verbose=True):
        self.source_scheme, self.domain, self.path = self.analyze_source(source)
        self.source = self.source_scheme + "://" + self.domain + self.path
        self.dest = dest if dest else self.domain
        self.headers = headers if headers else HEADERS
        self.verbose = verbose
        self.depth = depth
        self.deep_scan = deep_scan
        self.patterns_to_trim = patterns_to_trim
        self.pages = []
        self.urls = []
        self.downloading_counter = 0

    
    def download(self):
        print(">>>>> Crawling")
        self.urls = self.crawl()

        print(">>>>> Downloading")
        for url in self.urls:
            self.download_file(url)

        print(">>>>> Finding Pages")
        self.pages = self.find_pages()
        
        print(">>>>> Downloading Assets")
        for page in self.pages:
            assets = self.find_assets(page)
            if self.deep_scan:
                assets = assets + self.find_deep_assets(page)
            
            for asset in assets:
                self.download_file(asset)
        self.print_to_screen()

    def analyze_source(self, source):
        if source.startswith("http"):
            parsed_source = urlparse(source)
            if parsed_source.netloc:
                return parsed_source.scheme, parsed_source.netloc, parsed_source.path
            else:
                sys.exit("Source does NOT seem valid")
        elif source.startswith("www"):
            parsed_source = urlparse("http://" + source)
            return "http", parsed_source.netloc, parsed_source.path
        else:
            sys.exit("Source does NOT seem valid")
            

    def crawl(self):
        pages = [self.source]
        if self.depth == 0:
            return pages
        indexed_url = []
        for i in range(self.depth):
            for page in pages:
                if page not in indexed_url:
                    indexed_url.append(page)
                    response = self.request_file(page)
                    if not response:
                        continue
                    soup = BeautifulSoup(response.content, "html.parser")
                    links = soup('a')  # finding all the sub_links
                    for link in links:
                        if 'href' in dict(link.attrs):
                            url = urljoin(page, link['href'])
                            if url.find("'") != -1:
                                continue
                            url = url.split('#')[0]
                            if url[0:4] == 'http':
                                indexed_url.append(url)
            pages = indexed_url
        return [*set(indexed_url)]


    def extract_url(self, url):
        path = urlparse(url).path
        if not os.path.splitext(path)[1] and not path.endswith("/"):
            path = path + "/"
        basename = os.path.basename(path)
        file_path = self.dest + os.path.dirname(path)
        file_name = basename if basename else "index.html"
        return file_path, file_name


    def download_file(self, url):
        file_path, file_name = self.extract_url(url)
        if not self.is_exist(file_path, file_name):
            response = self.request_file(url)
            if response and response.content:
                if self.store_file(file_path, file_name, response.content):
                    self.downloading_counter += 1
                    self.print_to_screen(f'Downloaded: {url}')
        else:
            self.print_to_screen(f'File exists: {url}')


    def request_file(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            else:
                self.print_to_screen(f"Requested with {response.status_code}: {url}")
                return
        except:
            self.print_to_screen(f"Request not reachable: {url}")            
            return


    def store_file(self, file_path, file_name, file_content):
        try:
            os.makedirs(file_path, exist_ok=True)
            with open(file_path + "/" + file_name, 'wb') as file:
                file.write(file_content)
            return True
        except Exception as e:
            if self.verbose:
                logging.error('Failed to store file: '+ str(e))
            return False
    

    def is_exist(self, file_path, file_name):
        return os.path.isfile(file_path + "/" + file_name)


    def find_pages(self):
        html_files = []
        for root, dirs, pages in os.walk(self.dest):
            for page in pages:
                if page.endswith(".html"):
                    path = (os.path.join(root, page)).replace("\\", "/")
                    html_files.append(path)
        return html_files


    def find_assets(self, source_file):
        source_text = self.read_local_file(source_file)
        soup = BeautifulSoup(source_text, 'html.parser')
        assets = []
        for tag in soup.find_all():
            if tag.name == 'img':
                src = tag.get('src')
                if src:
                    assets.append(src)
            elif tag.name == 'link':
                href = tag.get('href')
                if href and len(href) > 1:
                    assets.append(href)
            elif tag.name == 'script':
                src = tag.get('src')
                if src:
                    assets.append(src)
        return self.clean_assets(assets)


    def find_deep_assets(self, source_file):
        source_text = self.read_local_file(source_file)
        asset_extensions = ['html', 'css', 'js', 'jpg', 'jpeg', 'png', 'gif', 'svg', 'ico', 'webp', 'pdf', 'mp4', 'webm', 'mp3', 'wav', 'woff2', 'woff' 'ttf', 'otf', 'json', 'xml', 'csv', 'zip']
        assets = []
        for ext in asset_extensions:
            pattern = rf'[\/a-zA-Z0-9\_\.\:\\-]+\.{ext}\b'
            matches = re.findall(pattern, source_text, re.IGNORECASE)
            for match in matches:
                match = unquote(match).replace('%2F', '/')
                if not match in assets:
                    assets.append(match)
        return self.clean_assets(assets)


    def clean_assets(self, assets):
        cleaned = []
        for asset in assets:
            asset = asset.replace("%2F", "/")
            asset = asset.replace("%3A", ":")
            if self.patterns_to_trim:
                for pattern in self.patterns_to_trim:
                    asset = asset.replace(pattern, "")
            if asset.startswith("."):
                asset = asset.lstrip(".")
            if "?auto" in asset:
                idx = asset.index("?")
                asset = asset[:idx]
            if asset.startswith("//") and ".com" in asset:
                asset = "http:" + asset
            parsed_asset = urlparse(asset)
            if not parsed_asset.netloc:
                asset = self.source_scheme + "://" + self.domain + asset
            if not asset in cleaned:
                cleaned.append(asset)
        return cleaned

    
    def read_local_file(self, source_file):
        try:
            with open(source_file, 'r', encoding='utf-8') as file:
                source_text = file.read()
            return source_text
        except:
            self.print_to_screen(f'File could not read: {source_file}')

    
    def print_to_screen(self, message="Done!"):
        if self.verbose:
            print(f'Downloaded ({self.downloading_counter}) - ' + message)

