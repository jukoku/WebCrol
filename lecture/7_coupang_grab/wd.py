from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from sv_7 import*
class Coupang_web:

  def __init__(self):
    self.options = webdriver.ChromeOptions()
    self.options.add_argument("headless")  # 헤드리스 모드 실행
    self.options.add_argument('window-size=1920x1080')
    self.options.add_argument("disable-gpu")
    # 혹은 options.add_argument("--disable-gpu")
    # UserAgent값을 바꿔줍시다! - headless인 것을 속이기!
    self.options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    self.options.add_argument("lang=ko_KR") # 한국어!

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
    self.title = 'a > dl > dd > div > div.name'
    self.price = 'a > dl > dd > div > div.price-area > div > div.price > em > strong'
    self.price_100 = 'a > dl > dd > div > div.price-area > div > div.price > span.unit-price > em:nth-child(2)'
    self.a_link = 'a'

  def store_pages(self):
    for i in range(1, 28):
      self.pages.append(mainpage + str(i))
    print(self.pages)

  def grab(self):
    for page in self.pages:
      self.driver.get(page)

      self.html = self.driver.page_source
      self.soup = BeautifulSoup(self.html, 'html.parser')
      self.title = self.soup.select(self.title)
      self.price = self.soup.select(self.price)
      self.price_100 = self.soup.select(self.price_100)
      self.a_link = self.soup.select(self.a_link)
      print(len(self.title), len(self.price), len(self.price_100), len(self.a_link))
      print(self.title[0])
      # print(self.price)
      # print(self.price_100)
      # print(self.a_link)
