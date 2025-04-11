# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sv_7 import*
import time
class Coupang_web:

  def __init__(self):
    self.options = webdriver.ChromeOptions()
    # self.options.add_argument("--headless")  # 헤드리스 모드 실행
    # self.options.add_argument('--window-size=1920x1080')
    # self.options.add_argument("--disable-gpu")
    # 혹은 options.add_argument("--disable-gpu")
    # UserAgent값을 바꿔줍시다! - headless인 것을 속이기!
    self.options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    self.options.add_argument("lang=ko_KR") # 한국어!
    self.options.add_argument("--disable-blink-features=AutomationControlled")

    self.driver = webdriver.Chrome(
      service=Service(ChromeDriverManager().install()),
      options=self.options
    )
    self.driver.implicitly_wait(3)
    self.driver.get('about:blank')
    self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
    self.pages = []
    self.html = ''
    self.soup = ''
    self.title = 'li > a > dl > dd > div > div.name'
    self.price = 'li > a > dl > dd > div > div.price-area > div > div.price > em > strong'
    self.price_100 = 'li > a > dl > dd > div > div.price-area > div > div.price > span.unit-price > em:nth-child(2)'
    self.a_link = 'li > a'
    self.one = '#productList'

  def click_next(self):
    self.driver.find_element(By.XPATH, '//*[@id="searchOptionForm"]/div[2]/div[2]/div[6]/span[2]/a[2]').click()
    time.sleep(60)

  def store_pages(self):
    for i in range(1, 28):
      self.pages.append(mainpage + str(i))

  def connect(self, page):    
    self.driver.get(page)
    try:
      element = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.ID, 'productList'))
        )
    finally:
      print('계속')

  def grab(self):

    self.html = self.driver.page_source
    self.soup = BeautifulSoup(self.html, 'html.parser')
    self.one = self.soup.select_one(self.one)      
    self.title = self.one.select(self.title)
    self.price = self.one.select(self.price)
    self.price_100 = self.one.select(self.price_100)      
    self.a_link = self.one.select(self.a_link)
    print(len(self.title), len(self.price), len(self.price_100), len(self.a_link))
    print(self.title)
    # print(self.price)
    # print(self.price_100)
    # print(self.a_link)
    time.sleep(60)
    
