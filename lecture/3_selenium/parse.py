from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import gspread
import datetime
now = datetime.datetime.now() # 현재시간
from sv_3 import*

# json 파일이 위치한 경로를 값으로 줘야 합니다.
gc = gspread.service_account(json_file_path)
wks = gc.open_by_url(spreadsheet_url)
doc_link = wks.worksheet("링크")
doc_crol = wks.worksheet("크롤")
doc_result = wks.worksheet("결과")



options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
# 혹은 options.add_argument("--disable-gpu")
# UserAgent값을 바꿔줍시다! - headless인 것을 속이기!
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR") # 한국어!



driver = webdriver.Chrome(options=options)
driver.implicitly_wait(3)
driver.get('about:blank')
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
driver.get(mainpage) # 폰헙 접속
driver.find_element('xpath', '//*[@id="modalWrapMTubes"]/div/div/button').click() # 19세 이상 클릭


# 스프레드시트 --> 리스트
mvlinks = doc_link.col_values(1)
res_cmd = doc_result.col_values(1)
res_cmd.append('여기서 시작  __  ' + now.strftime("%Y-%m-%d %H:%M:%S")) #현재시간 즉, 크롤한 시간을 같이 표시
mvsites = doc_result.col_values(2)
mvsites.append('')
chlinks = doc_result.col_values(3)
chlinks.append('')
filenames = doc_result.col_values(4)
filenames.append('')
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
  script = soup.select('#player > script:nth-child(1)') # m3u8 있는 부분의 script 추출
  # 아래 CSS Selector는 영상 제목을 콕 하고 집어줍니다.
  title = soup.select('#hd-leftColVideoPage > div.topSectionGrid > div.videoWrapModelInfo.original > div > div.title-container > h1 > span') # title 추출
  # 아래 CSS Selector는 마찬가지로 해당 영상을 게시한 Author를 콕 하고 집어줍니다.
  author_selector_1 = '#hd-leftColVideoPage > div.topSectionGrid > div.videoWrapModelInfo.original > div > div.video-actions-container > div.video-actions-tabs > div.video-action-tab.about-tab.active > div.video-detailed-info > div.video-info-row.userRow > div.userInfoBlock > div.userInfo > div > a'
  author_selector_2 = '#hd-leftColVideoPage > div.topSectionGrid > div.videoWrapModelInfo.original > div > div.video-actions-container > div.video-actions-tabs > div.video-action-tab.about-tab.active > div.video-detailed-info > div.video-info-row.userRow > div.userInfoBlock > div.userInfo > div > span > a'
  author = soup.select(author_selector_2)  # 채널주인명 부분 추출
  if author == []:
    author = soup.select(author_selector_1)
  print(title)
  print(author)
  chlink = mainpage + author[0].get('href') # 채널주인 부분에서 링크 추출
  chlinks.append(chlink) # 채널 링크 추가
  # HTML을 제대로 파싱한 뒤에는 .text속성을 이용합니다.  
  # [0]을 하는 이유는 select로 하나만 가져와도 title자체는 리스트이기 때문입니다.
  # 즉, 제목 글자는 title이라는 리스트의 0번(첫번째)에 들어가 있습니다.
  filename = ' "' + author[0].text +' __ '+ title[0].text + '"'
  filename = filename.replace('/', '-').replace("\\", '-').replace('|', '-') # 파일명에 쓰면 에러나는 특수기호 변경
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
res_cols = [res_cmd, mvsites, chlinks, filenames] # 명령어, 영상링크, 채널링크, 파일이름을 리스트로 추가 
doc_result.insert_cols(res_cols, col=1) # 위에서 추가한 리스트를 '결과' 시트에 추가
driver.quit()