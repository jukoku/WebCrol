# -*- coding: utf-8 -*-
import re
import sys
#sv는 환경변수로 지정된 폴더 내에 있는 파일 sv.py -> class lec_6
from sv_6 import Examples

ex = Examples()

print(ex.getpart(ex.cq, ex.test))
print(ex.gennum(ex.getpart(ex.cq, ex.test)))
print(ex.getpart(ex.cq, ex.test1))
print(ex.gennum(ex.getpart(ex.cq, ex.test1)))
print(ex.getpart(ex.cq, ex.test2))
print(ex.gennum(ex.getpart(ex.cq, ex.test2)))
print(ex.getpart(ex.cq, ex.test3))
print(ex.gennum(ex.getpart(ex.cq, ex.test3)))
print(ex.getpart(ex.cq1, ex.test3))

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

print(sys.path)