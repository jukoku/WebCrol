import requests
from bs4 import BeautifulSoup
from sv_7 import*

class Coupang_re:
  
  def __init__(self):
    self.url = 'https://www.coupang.com'
    self.req = requests.get(self.url)
    self.html = self.req.text
    self.soup = BeautifulSoup(self.html, 'html.parser')
    self.title = 'li > a > dl > dd > div > div.name'
    self.price = 'li > a > dl > dd > div > div.price-area > div > div.price > em > strong'
    self.price_100 = 'li > a > dl > dd > div > div.price-area > div > div.price > span.unit-price > em:nth-child(2)'
    self.a_link = 'li > a'
    self.one = '#productList'

  def crolling(self, page:int):
    self.url = mainpage + str(page)
    self.req = requests.get(self.url)
    self.html = self.req.text
    self.soup = BeautifulSoup(self.html, 'html.parser')
    self.one = self.soup.select_one(self.one)      
    self.title = self.one.select(self.title)
    self.price = self.one.select(self.price)
    self.price_100 = self.one.select(self.price_100)      
    self.a_link = self.one.select(self.a_link)
    print(len(self.title), len(self.price), len(self.price_100), len(self.a_link))
    print(self.title)