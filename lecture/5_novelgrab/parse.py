# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import sys
import re
from sv_5 import*
from gs import NovelGrab
# json 파일이 위치한 경로를 값으로 줘야 합니다.

PRICE = 1000 #권당 가격 상한선
ISEND = True #완결된 것만 취득 ?
STORE = 'comic' #코믹겔러지(comic), 전체(whole)

ng = NovelGrab()
nv = Novel()

ng.store(STORE)

fantasy_h = nv.get_link(nv.fantasy)
muhyup_h = nv.get_link(nv.muhyup)
fantasy_comic = nv.get_link(nv.fantasy, nv.store())
muhyup_comic = nv.get_link(nv.muhyup, nv.store())

options = webdriver.ChromeOptions()
options.add_argument("headless")  # 헤드리스 모드 실행
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
# 혹은 options.add_argument("--disable-gpu")
# UserAgent값을 바꿔줍시다! - headless인 것을 속이기!
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR") # 한국어!


genres_web = []

driver = webdriver.Chrome(
  service=Service(ChromeDriverManager().install()),
  options=options
)
driver.implicitly_wait(3)
driver.get('about:blank')
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
if STORE == 'comic':  # 코믹겔러리 페이지수 수집
  driver.get(fantasy_comic)  
  driver.find_element(By.CSS_SELECTOR, '#short > div.numbox_last > a').click()
  pages_fantasy_comic = 1
  fn = 'page[=]\d{1,2}|page[=]\d{3,4}'
  while pages_fantasy_comic < 2:
    pages_fantasy_comic = int(''.join(re.split(r'\D+', ''.join(re.findall(fn, driver.current_url))))) # 현재 최대 페이지수 수집
  driver.get(muhyup_comic)    
  driver.find_element(By.CSS_SELECTOR, '#short > div.numbox_last > a').click()  
  pages_muhyup_comic = 1
  while pages_muhyup_comic < 2:    
    pages_muhyup_comic = int(''.join(re.split(r'\D+', ''.join(re.findall(fn, driver.current_url))))) # 현재 최대 페이지수 수집
  print('페이지수 - 판타지 코믹겔러리 :', pages_fantasy_comic)
  print('페이지수 - 무협 코믹겔러리 :', pages_muhyup_comic)
# 페이지 수 전체 (판타지, 무협)
pages_fantasy_h = 100
pages_muhyup_h = 100

if STORE == 'whole':
  fantasy = fantasy_h
  muhyup = muhyup_h
  pages_fantasy = pages_fantasy_h
  pages_muhyup = pages_muhyup_h
elif STORE == 'comic':
  fantasy = fantasy_comic
  muhyup = muhyup_comic
  pages_fantasy = pages_fantasy_comic
  pages_muhyup = pages_muhyup_comic

print(fantasy, '\n'+muhyup)
for page in range(1, pages_fantasy + 1):
  fantasy_ = fantasy.replace('page=1', f'page={page}')
  genres_web.append(fantasy_)
for page in range(1, pages_muhyup + 1):
  muhyup_ = muhyup.replace('page=1', f'page={page}')
  genres_web.append(muhyup_)
# print(genres_web)


for genre_ in genres_web:
  if 'CID=50928' in genre_: # 판타지(CID=50928) or 무협(CID=50932) 확인 
    genre = '판타지'    
  else:
    genre = '무협'
  driver.get(mainpage) # 알라딘 중고도서 접속
  driver.get(genre_) # 장르소설 검색
  
  html = driver.page_source  
  soup = BeautifulSoup(html, 'html.parser')  
  form = soup.select('#Myform > table > tbody > tr:nth-child(1) > td > table > tbody > tr > td > table > tbody > tr > td')  
  title_a = soup.select('#Myform > table > tbody > tr:nth-child(1) > td > table > tbody > tr > td > table > tbody > tr > td > a')  
  au_pu = soup.select('#Myform > table > tbody > tr:nth-child(1) > td > table > tbody > tr > td > table > tbody > tr > td > span.gw')
  price_1 = soup.select('#Myform > table > tbody > tr:nth-child(1) > td > table > tbody > tr > td > table > tbody > tr > td > span.p1_n > span')
  print(len(form), len(title_a), len(au_pu), len(price_1),'\n\n')

  for i in range(len(form)):
    title_l = re.split('[|/]|/s/s|\\\\', title_a[i].text)
    au_pu__ = []
    if len(title_l) == 1:
      title = title_l[0]
    else:
      title = title_l[0]
      del title_l[0]
      au_pu__ = ' / '.join(title_l)
    if '완' in title:
      isEnd = '완결됨'
    elif re.findall('전\d', title) != []:
      isEnd = '완결됨'
    else:
      if ISEND == True: # 완결이 아닐시 건너뜀 (선택)
        continue 
    link = title_a[i].get('href')
    bprice = price_1[i].text
    condition = form[i].text.split(']')[0].replace('[', '')
        
    au_pu_ = re.split('[|/]|/s/s|\\\\', au_pu[i].text.replace('ㅁ(미음)', ''))
    if au_pu__ != []:
      if len(au_pu_) == 1:
        author = '불확실 : ' + au_pu__
        publisher = au_pu_[0]
      else:
        author = au_pu_[0]
        publisher = au_pu_[1]
    else:
      if len(au_pu_) == 1:
        author = ''
        publisher = au_pu_[0]
      else:
        author = au_pu_[0]
        publisher = au_pu_[1]
    cq = '\d{1}[-~]\d{1,2}|\d{1}\s[-~]\d{1,2}|\d{1}[-~]\s\d{1,2}|\d{1}\s[-~]\s\d{1,2}' \
    '|\d{1}[-~]\d{3,4}|\d{1}\s[-~]\d{3,4}|\d{1}[-~]\s\d{3,4}|\d{1}\s[-~]\s\d{3,4}' \
    '|전\d{1,2}|전\s\d{1,2}|전\s\s\d{1,2}|전\d{3,4}|전\s\d{3,4}|전\s\s\d{3,4}'
    many = '-'.join(re.findall(cq, title))
    many = re.split(r'\D+', many)
    many = [one for one in many if one != '']
    if len(many) == 1:
      n_book = '1'
    elif len(many) == 0:
      n_book = '1'
    else:
      n_book = many[len(many)-1]
    price_a = [int(i) for i in price_1[i].text if i.isdigit()]
    price_b = int(''.join(map(str, price_a)))
    price = int(price_b / int(''.join(map(str, n_book))))
    print('\n\n가격 :', price_b, '\n가격(권당) :', price, '\n권수 :', n_book,'\n\n')
    if price > PRICE: #권당 가격 일정 이상 제외 (선택)
      continue
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
    
    ng.appends(genre, title, isEnd, condition, n_book, bprice, price, publisher, author, link)
    print('Items :',len(ng.titles))
driver.quit()
ng.save_cols()
ng.insert_cols(ng.doc_now, ng.now_cols)
ng.insert_rows(ng.doc_now, ng.genres)
ng.insert_cols(ng.doc_old, ng.old_cols)
ng.insert_rows(ng.doc_old, ng.genres_old)

print('여기서 테스트')
