# -*- coding: utf-8 -*-
import gspread
import datetime
now = datetime.datetime.now() # 현재시간
from sv_7 import spreadsheet_url, json_file_path
# 환경변수를 통해서는 json파일을 읽을 수 없다는 것을 확인

class Common:

  def wks(json_file_path, spreadsheet_url):
    gc = gspread.service_account(json_file_path)
    return gc.open_by_url(spreadsheet_url)

class Coupang:

  def __init__(self):
    self.wks = Common.wks(json_file_path, spreadsheet_url)
    self.doc = self.wks.worksheet('확인')
    self.products = ['여기서 시작 __ ']
    self.prices = [now.strftime("%Y-%m-%d %H:%M:%S")]
    self.price_100s = ['']
    self.deliverys = ['']
    self.links = ['']
    self.head = [
      ['상품명', '가격', '가격(100m당)', '배송', '링크'],
      ['product', 'price', 'price_100', 'delivery', 'link']
    ]

    self.cols=[]

  def appends(self, product, price, price_100, delivery, link):
    self.products.append(product)
    self.prices.append(price)
    self.price_100s.append(price_100)
    self.deliverys.append(delivery)
    self.links.append(link)

  def save_cols(self):
    self.cols = [
      self.products, self.prices, 
      self.price_100s, self.deliverys, 
      self.links
      ]
  
  def insert_cols(self):
    self.doc.clear()
    self.doc.insert_cols(self.cols, col=1)
  
  def insert_rows(self):
    if self.products[0] != '상품명':
      self.doc.insert_rows(self.head, row=1)
