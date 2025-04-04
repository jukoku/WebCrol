# -*- coding: utf-8 -*-
import gspread
import datetime
now = datetime.datetime.now() # 현재시간
from sv_5 import json_file_path, spreadsheet_url

class Common:

  
  def wks(json_file_path, spreadsheet_url):
    gc = gspread.service_account(json_file_path)
    return gc.open_by_url(spreadsheet_url)

class NovelGrab:

  def __init__(self):
    self.seller = ''    
    self.wks = Common.wks(json_file_path, spreadsheet_url)
    self.doc_now = self.wks.worksheet('지금(테스트)')
    self.doc_old = self.wks.worksheet('과거(테스트)')
    self.genres = ['여기서 시작 __ ']
    self.titles = [now.strftime("%Y-%m-%d %H:%M:%S")]
    self.isEnds = ['']
    self.conditions = ['판매자']
    self.n_books = [] # 스토어(셀러 선택)
    self.bprices = ['']
    self.prices = ['']
    self.publishers = ['']
    self.authors = ['']
    self.links = ['']
    self.head = []
    self.now_cols = []
    self.old_cols = []
    

  def store(self, store='whole'): #코믹겔러지(comic), 전체(whole)
    if store == 'whole':
      self.seller = '전체'
    elif store == 'comic':
      self.seller = '코믹겔러리'
    self.n_books = [self.seller] # 스토어(셀러 선택)
    self.head = [
    ['장르', '제목', '완결여부', '상태', '권', '가격', '가격(권당)', '출판사', '저자', '링크', '판매자', self.seller], 
    ['genre', 'title', 'isEnd', 'condition', 'n_book', 'bprice', 'price', 'publisher', 'author', 'link']
    ]
    self.genres_old = self.doc_old.col_values(1)
    self.titles_old = self.doc_old.col_values(2)
    self.isEnds_old = self.doc_old.col_values(3)
    self.conditions_old = self.doc_old.col_values(4)
    self.n_books_old = self.doc_old.col_values(5)
    self.bprices_old = self.doc_old.col_values(6)
    self.prices_old = self.doc_old.col_values(7)
    self.publishers_old = self.doc_old.col_values(8)
    self.authors_old = self.doc_old.col_values(9)
    self.links_old = self.doc_old.col_values(10)
    
    self.genres_old.append(self.genres[0])
    self.titles_old.append(self.titles[0])
    self.isEnds_old.append(self.isEnds[0])
    self.conditions_old.append(self.conditions[0])
    self.n_books_old.append(self.n_books[0])
    self.bprices_old.append(self.bprices[0])
    self.prices_old.append(self.prices[0])
    self.publishers_old.append(self.publishers[0])
    self.authors_old.append(self.authors[0])
    self.links_old.append(self.links[0])
  
  def appends(self, genre, title, isEnd, condition, n_book, bprice, price, publisher, author, link):
    self.genres.append(genre)
    self.titles.append(title)
    self.isEnds.append(isEnd)
    self.conditions.append(condition)
    self.n_books.append(n_book)
    self.bprices.append(bprice)
    self.prices.append(price)
    self.publishers.append(publisher)
    self.authors.append(author)
    self.links.append(link)

    self.genres_old.append(genre)
    self.titles_old.append(title)
    self.isEnds_old.append(isEnd)
    self.conditions_old.append(condition)
    self.n_books_old.append(n_book)
    self.bprices_old.append(bprice)
    self.prices_old.append(price)
    self.publishers_old.append(publisher)
    self.authors_old.append(author)
    self.links_old.append(link)

  def save_cols(self): # 각 열을 스프레드시트에 입력할 리스트로 저장
    self.now_cols = [self.genres, self.titles, self.isEnds, self.conditions, self.n_books, self.bprices, self.prices, self.publishers, self.authors, self.links]
    self.old_cols = [self.genres_old, self.titles_old, self.isEnds_old, self.conditions_old, self.n_books_old, self.bprices_old, self.prices_old, self.publishers_old, self.authors_old, self.links_old]
  
  def test(self):
    for i in self.genres:
      print(i)
    
  def insert_cols(self, doc, cols):
    doc.clear()
    doc.insert_cols(cols, col=1)

  def insert_rows(self, doc, geners):
    if geners[0] != '장르':
      doc.insert_rows(self.head, row=1)
  
