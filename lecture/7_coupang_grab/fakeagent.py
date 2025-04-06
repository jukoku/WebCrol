import time
import random
import requests
from bs4 import BeautifulSoup

from fake_useragent import UserAgent

def set_header() -> dict[str, str]:
    return {
        "User-Agent": UserAgent().random,
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

def crawling_waiting_time() -> None:
    return time.sleep(random.randint(1, 3))

def check_last_page(self, category_id):
    response = requests.get(construct_url(category_id, 1), headers=set_header())
    response.raise_for_status()
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        page = soup.find('div', class_='product-list-paging')
        return int(page['data-total'])
    return 1

