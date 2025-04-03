# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import gspread
import datetime
import sys
import re
now = datetime.datetime.now() # 현재시간
import sv

# json 파일이 위치한 경로를 값으로 줘야 합니다.

gc = gspread.service_account(sv.json_file_path)
wks = gc.open_by_url(sv.spreadsheet_url)

doc_now = wks.worksheet('지금(알라딘)')
doc_old = wks.worksheet('과거(알라딘)')

genres = []
titles = []
isEnds = []
conditions = []
n_books = []
bprices = []
prices = []
publishers = []
authors = []
links = []

genres_old = doc_old.col_values(1)
titles_old = doc_old.col_values(2)
isEnds_old = doc_old.col_values(3)
conditions_old = doc_old.col_values(4)
n_books_old = doc_old.col_values(5)
bprices_old = doc_old.col_values(6)
prices_old = doc_old.col_values(7)
publishers_old = doc_old.col_values(8)
authors_old = doc_old.col_values(9)
links_old = doc_old.col_values(10)

options = webdriver.ChromeOptions()
options.add_argument("headless")  # 헤드리스 모드 실행
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
# 혹은 options.add_argument("--disable-gpu")
# UserAgent값을 바꿔줍시다! - headless인 것을 속이기!
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR") # 한국어!


genres_web = []
mainpage = 'https://www.aladin.co.kr'
pages_fantasy = 101
pages_muhyup = 101
for page in range(1, pages_fantasy):
  fantasy = f'https://www.aladin.co.kr/shop/wbrowse.aspx?ItemType=100&ViewRowsCount=48&ViewType=Simple&PublishMonth=0&SortOrder=6&page={page}&UsedShop=0&PublishDay=84&CID=50928&SearchOption=&QualityType=&OrgStockStatus=&IsFlatPrice='
  genres_web.append(fantasy)
for page in range(1, pages_muhyup):
  muhyup = f'https://www.aladin.co.kr/shop/wbrowse.aspx?ItemType=100&ViewRowsCount=48&ViewType=Simple&PublishMonth=0&SortOrder=6&page={page}&UsedShop=0&PublishDay=84&CID=50932&SearchOption=&QualityType=&OrgStockStatus=&IsFlatPrice='
  genres_web.append(muhyup)
print(genres_web)

driver = webdriver.Chrome(
  service=Service(ChromeDriverManager().install()),
  options=options
)
driver.implicitly_wait(3)
driver.get('about:blank')
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
count = 0
for genre_ in genres_web:
  if count == 0:
    genre = '무협'
  else:
    genre = '판타지'
  driver.get(mainpage) # 알라딘 중고도서 접속
  driver.get(genre_) # 장르소설 검색
  
  html = driver.page_source  
  soup = BeautifulSoup(html, 'html.parser')  
  form = soup.select('#Myform > table > tbody > tr:nth-child(1) > td > table > tbody > tr > td > table > tbody > tr > td')  
  title_a = soup.select('#Myform > table > tbody > tr:nth-child(1) > td > table > tbody > tr > td > table > tbody > tr > td > a')  
  au_pu = soup.select('#Myform > table > tbody > tr:nth-child(1) > td > table > tbody > tr > td > table > tbody > tr > td > span.gw')
  price_1 = soup.select('#Myform > table > tbody > tr:nth-child(1) > td > table > tbody > tr > td > table > tbody > tr > td > span.p1_n > span')
  print(len(form), len(title_a), len(au_pu), len(price_1),'\n\n')
  count = 0
  for i in range(len(form)):
    title = title_a[i].text
    link = title_a[i].get('href')
    bprice = price_1[i].text
    condition = form[i].text.split(']')[0].replace('[', '')
    if '완' in title:
      isEnd = '완결됨'
    else:
      isEnd = ''

    au_pu_ = au_pu[i].text.split('|')
    if len(au_pu_) == 1:
      au_pu_ = au_pu_[0].split('/')
      if len(au_pu_) == 1:
        au_pu_ = au_pu_[0].split('  ')
    if len(au_pu_) == 2:
      author = au_pu_[0]    
      publisher = au_pu_[1]    
    elif len(au_pu_) == 1:
      author = ''
      publisher = au_pu_[0]
    many = re.split(r'\D+', title_a[i].text)
    many = [one for one in many if one != '']
    if len(many) == 1:
      n_book = '1'
    elif len(many) == 0:
      n_book = '1'
    else:
      n_book = many[len(many)-1]
    price_a = [int(i) for i in price_1[i].text if i.isdigit()]
    price_b = int(''.join(map(str, price_a)))
    print('\n\n', 'price_b :', price_b, '\nn_book :', n_book, '\npage :', genre_, '\n\n')
    price = int(price_b / int(''.join(map(str, n_book))))
    print('장르 : ',genre)
    print('제목 : ',title)
    print('완결여부 : ',isEnd)
    print('상태 : ',condition)
    print('권 : ',n_book)
    print('가격 : ',bprice)
    print('가격(권당) : ',price)
    print('출판사 : ',publisher)
    print('저자 : ',author)
    print('링크 : ',link,'\n')
    
    genres.append(genre)
    titles.append(title)
    isEnds.append(isEnd)
    conditions.append(condition)
    n_books.append(n_book)
    bprices.append(bprice)
    prices.append(price)
    publishers.append(publisher)
    authors.append(author)
    links.append(link)

    count = count + 1

for i in genres:
  genres_old.append(i)
for i in titles:
  titles_old.append(i)
for i in isEnds:
  isEnds_old.append(i)
for i in conditions:
  conditions_old.append(i)
for i in n_books:
  n_books_old.append(i)
for i in bprices:
  bprices_old.append(i)
for i in prices:
  prices_old.append(i)
for i in publishers:
  publishers_old.append(i)
for i in authors:
  authors_old.append(i)
for i in links:
  links_old.append(i)
now_cols = [genres, titles, isEnds, conditions, n_books, bprices, prices, publishers, authors, links]
old_cols = [genres_old, titles_old, isEnds_old, conditions_old, n_books_old, bprices_old, prices_old, publishers_old, authors_old, links_old]
doc_now.clear()
doc_now.insert_cols(now_cols, col=1)
doc_now.insert_rows(
  [
    ['장르', '제목', '완결여부', '상태', '권', '가격', '가격(권당)', '출판사', '저자', '링크'], 
    ['genre', 'title', 'isEnd', 'condition', 'n_book', 'bprice', 'price', 'publisher', 'author', 'link'],     
    ['여기서 시작 __ ', now.strftime("%Y-%m-%d %H:%M:%S"), '', '', '', '', '', '', '', '']
    ], row=1
    )
doc_old.clear()
doc_old.insert_cols(old_cols, col=1)