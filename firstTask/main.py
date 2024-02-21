import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, parse_qs
import time
def download_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None
def create_index_file(pages_info):
    with open('index.txt', 'w', encoding='utf-8') as f:
        for page_info in pages_info:
            f.write(f'{page_info[0]} - {page_info[1]} - {page_info[2]}\n')
def save_page(page_content, page_num, url, saved_pages):
    filename = f'page_{page_num}.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(page_content)
    saved_pages.append((page_num, filename, url))

start_url = 'http://www.world-war.ru/'
max_pages = 100

if not os.path.exists('downloaded_pages'):
    os.makedirs('downloaded_pages')

os.chdir('downloaded_pages')

saved_pages = []

crawl_queue = [start_url]
visited_urls = set()

while crawl_queue and len(saved_pages) < max_pages:
    url = crawl_queue.pop(0)
    parsed_url = urlparse(url)
    if parsed_url.netloc == urlparse(start_url).netloc and url not in visited_urls:
        print(f'Crawling: {url}')
        page_content = download_page(url)
        if page_content:
            soup = BeautifulSoup(page_content, 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            page_num = len(saved_pages) + 1
            save_page(str(soup), page_num, url, saved_pages)
            links = [link.get('href') for link in soup.find_all('a', href=True)]
            for link in links:
                parsed_link = urlparse(link)
                if parsed_link.netloc == parsed_url.netloc and parsed_link.path.count('/') == 2 and not parsed_link.query:
                    crawl_queue.append(link)
            visited_urls.add(url)
        time.sleep(1)

create_index_file(saved_pages)

print("Finish!")
