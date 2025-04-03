# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import gspread
import datetime
import sys
now = datetime.datetime.now() # 현재시간
from sv import*

# json 파일이 위치한 경로를 값으로 줘야 합니다.
gc = gspread.service_account(json_file_path)
wks = gc.open_by_url(spreadsheet_url)
doc_link = wks.worksheet("링크")

# 링크 있는지 확인 후 없으면 종료
mvlinks = doc_link.col_values(1)
print(mvlinks)
if mvlinks == []:
  sys.exit(0)

doc_crol = wks.worksheet("크롤")
doc_result = wks.worksheet("결과")
doc_result_old = wks.worksheet("결과(old)")


options = webdriver.ChromeOptions()
options.add_argument("headless")  # 헤드리스 모드 실행
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
# 혹은 options.add_argument("--disable-gpu")
# UserAgent값을 바꿔줍시다! - headless인 것을 속이기!
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR") # 한국어!

driver = webdriver.Chrome(
  service=Service(ChromeDriverManager().install()),
  options=options
)
driver.implicitly_wait(3)
driver.get('about:blank')
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
driver.get(mainpage) # 폰헙 접속
driver.find_element('xpath', '//*[@id="modalWrapMTubes"]/div/div/button').click() # 19세 이상 클릭


# 스프레드시트 --> 리스트
res_cmd = []
res_cmd.append('여기서 시작  __  ' + now.strftime("%Y-%m-%d %H:%M:%S")) #현재시간 즉, 크롤한 시간을 같이 표시
res_cmd_old = doc_result_old.col_values(1)
mvsites = []
mvsites.append('')
mvsites_old = doc_result_old.col_values(2)
chlinks = []
chlinks.append('')
chlinks_old = doc_result_old.col_values(3)
filenames = []
filenames.append('')
filenames_old = doc_result_old.col_values(4)
script_cols = []

# 영상 크롤용 스프레드시트에서 영상링크 가져오기
for link in mvlinks:
  # print(mvlinks)
  # print(res_cmd)
  # print(mvsites)
  # print(chlinks)
  print(filenames)
  mvsites.append(link) # 영상링크 추가
  driver.get(link)
  html = driver.page_source # 페이지 내용 추출
  soup = BeautifulSoup(html, 'html.parser') #soup로 변경
  
  main_title = soup.select('head > title') # 사이트 제목 (페이지 오류 혹은 위반 문제로 영상 삭제시 page not found 임)
  if 'Page Not Found' in main_title: # 오류 페이지가 존자하면 이번 링크는 스킵하고 다음으로 넘김
    chlinks.append(main_title)
    filenames.append(main_title)
    res_cmd.append(main_title)
    script_cols.append([main_title, main_title, main_title])
    if len(mvlinks) == 1: # 오류 페이지만 존재하면 더 이상 진행하지 않고 종료 
      sys.exit(0)
    continue # for문을 완전히 종료하지 않고 다음회차를 실행
  script = soup.select('#player > script:nth-child(1)') # m3u8 있는 부분의 script 추출
  # 아래 CSS Selector는 영상 제목을 콕 하고 집어줍니다.
  title = soup.select('#hd-leftColVideoPage > div.topSectionGrid > div.videoWrapModelInfo.original > div > div.title-container > h1 > span') # title 추출
  # 아래 CSS Selector는 마찬가지로 해당 영상을 게시한 Author를 콕 하고 집어줍니다.                       
  author_selector_1 = '#hd-leftColVideoPage > div.topSectionGrid > div.videoWrapModelInfo.original > div > div.video-actions-container > div.video-actions-tabs > div.video-action-tab.about-tab.active > div.video-detailed-info > div.video-info-row.userRow > div.userInfoBlock > div.userInfo > div > a'
  author_selector_2 = '#hd-leftColVideoPage > div.topSectionGrid > div.videoWrapModelInfo.original > div > div.video-actions-container > div.video-actions-tabs > div.video-action-tab.about-tab.active > div.video-detailed-info > div.video-info-row.userRow > div.userInfoBlock > div.userInfo > div > span > a'
  author = soup.select(author_selector_2)  # 채널주인명 부분 추출
  print(title)
  print(author)
  if author == []:
    author = soup.select(author_selector_1)    
  chlink = mainpage + author[0].get('href') # 채널주인 부분에서 링크 추출
  chlinks.append(chlink) # 채널 링크 추가
  # HTML을 제대로 파싱한 뒤에는 .text속성을 이용합니다.  
  # [0]을 하는 이유는 select로 하나만 가져와도 title자체는 리스트이기 때문입니다.
  # 즉, 제목 글자는 title이라는 리스트의 0번(첫번째)에 들어가 있습니다.
  filename = ' "' + author[0].text +' __ '+ title[0].text + '_"'
  filename = filename.replace('/', '-').replace("\\", '-').replace('|', '-').replace('!', '') # 파일명에 쓰면 에러나는 특수기호 변경
  scriptmix = script[0].text.split('"')
  filelink = ''
  for link in scriptmix:
    if 'master.m3u8?' in link:
      if '1080P' in link:
        filelink = link
      elif '720P' in link:
        filelink_720p = link
  filenames.append(filename) # 파일 이름 추가 
  print(filename)
  print('1080P: ' + filelink + '\n720P: ' + filelink_720p)  
  print(len(scriptmix))
  print(scriptmix.count('m3u8'))  
  if filelink == '':
    file_cmd = 'yt-dlp.sh ' + filelink_720p + filename # 명령어 작성
  else:
    file_cmd = 'yt-dlp.sh ' + filelink + filename # 명령어 작성
  res_cmd.append(file_cmd) # 명령어 추가
  script_cols.append(scriptmix)
doc_crol.clear() # 에러 방지를 위해서 작성 전에 모든 데이터를 저장 후 스프레드시트를 지운후 재작성
doc_crol.insert_cols(script_cols, col=1) # m3u8 부분 크롤한 내용 추가 ( 확인용 - 사이트에서 임의로 위치 변경시 수정해야됨 )
doc_result.clear()
for i in res_cmd:
  res_cmd_old.append(i)
for i in mvsites:
  mvsites_old.append(i)
for i in chlinks:
  chlinks_old.append(i)
for i in filenames:
  filenames_old.append(i)
res_cols = [res_cmd, mvsites, chlinks, filenames] # 명령어, 영상링크, 채널링크, 파일이름을 리스트로 추가 
res_cols_old = [res_cmd_old, mvsites_old, chlinks_old, filenames_old]
doc_result.insert_cols(res_cols, col=1) # 위에서 추가한 리스트를 '결과' 시트에 추가
doc_result.insert_rows(
  [
    ['명령어', '영상링크', '채널링크', '파일명'],
    ['res_cmd', 'mvsite', 'chlink', 'filename']
    ], row=1
    ) # 스프레드 시트 첫 두 줄에 기본적인 내용을 넣어서 보기 편하도록 만듬
doc_result_old.clear()
doc_result_old.insert_cols(res_cols_old, col=1) # 기존의 이전 내용까지 모두 포함하여 결과(old)시트에 등록
doc_link.clear() #사용된 링크 삭제
driver.quit()