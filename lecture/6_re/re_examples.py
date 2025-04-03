# -*- coding: utf-8 -*-
import re

test = '김기봉 장편소설 1 - 20, 언제까지 / 데스트'
test1 = '김기봉 장편소설 1-2, 언제까지 / 데스트'
test2 = '장기용 장편소설 전6권 완'
test3 = '장기용 장편소설 1 ~2 언제까지 전8권 / ㅌㅌ'



cq = '\d{1}[-~]\d{1,2}|\d{1}\s[-~]\d{1,2}|\d{1}[-~]\s\d{1,2}|\d{1}\s[-~]\s\d{1,2}' \
'|\d{1}[-~]\d{3,4}|\d{1}\s[-~]\d{3,4}|\d{1}[-~]\s\d{3,4}|\d{1}\s[-~]\s\d{3,4}' \
'|전\d{1,2}|전\s\d{1,2}|전\s\s\d{1,2}|전\d{3,4}|전\s\d{3,4}|전\s\s\d{3,4}'
result = '|'.join(re.findall(cq, test))
print(result)
result = re.split(r'\D+', result)
result = result[len(result)-1]
print(result)
result = '|'.join(re.findall(cq, test1))
print(result)
result = re.split(r'\D+', result)
result = result[len(result)-1]
print(result)
result = '|'.join(re.findall(cq, test3))
print(result)
result = re.split(r'\D+', result)
result = result[len(result)-1]
print(result)
result = re.findall('전\d', test1)
print(result)

test = '언제나/즐거운\우리집|앞마당  앞에는'
result = re.split('[/|]|\s\s|\\\\', test)
print(result)

title = ['아르토리아 로망스 3부(상 . 하) ', '라스네']
print(type(title[0]), type(title[len(title)-1]))
au_pu = '아르토리아 로망스 3부(상 . 하) '.split(' ')
print(au_pu)

publ = 'ㅁ(미음)'
publ1 = '알파인 / 시네마'

publ = publ.replace('ㅁ(미음)', '')
publ1 = publ1.replace('ㅁ(미음)', '')
print(publ, publ1)

PRICE = 1000 #권당 가격 상한선
ISEND = True #완결된 것만 취득?

print(PRICE)
if ISEND:
  print(ISEND)

text = 'and this page=1'
pages = 30
for page in range(1, pages + 1):
  text_ = text.replace('page=1', f'page={page}')
  print(text_)

current_url = 'this&page=20&dia'
fn = 'page[=]\d{1,2}|page[=]\d{3,4}'
rs = int(''.join(re.split(r'\D+', ''.join(re.findall(fn, current_url)))))
print(rs)
head =  [
    ['장르', '제목', '완결여부', '상태', '권', '가격', '가격(권당)', '출판사', '저자', '링크'], 
    ['genre', 'title', 'isEnd', 'condition', 'n_book', 'bprice', 'price', 'publisher', 'author', 'link']
    ]
print(head[0][0])