# parser.py
import requests
from bs4 import BeautifulSoup as bs
import sv

# Session 생성, with 구문 안에서 유지
with requests.Session() as s:
    # 폰허브 홈페이지 접속
    start_page = s.get(sv.start_page)
    html = start_page.text
    soup = bs(html, 'html.parser')
    # 영상링크 하나를 가져오기
    target_page = s.get(sv.target_page)
    soup = bs(target_page.text, 'html.parser') # soup로 만들어 주기
    # 아래 CSS Selector는 영상 제목을 콕 하고 집어줍니다.
    title = soup.select('#hd-leftColVideoPage > div.topSectionGrid > div.videoWrapModelInfo.original > div > div.title-container > h1 > span')
    # 아래 CSS Selector는 마찬가지로 해당 영상을 게시한 Author를 콕 하고 집어줍니다.
    author = soup.select('#hd-leftColVideoPage > div.topSectionGrid > div.videoWrapModelInfo.original > div > div.video-actions-container > div.video-actions-tabs > div.video-action-tab.about-tab.active > div.video-detailed-info > div.video-info-row.userRow > div.userInfoBlock > div.userInfo > div > span > a')
    # HTML을 제대로 파싱한 뒤에는 .text속성을 이용합니다.
    print(title) # 영상 제목의 문자만 가져옵니다.
    # [0]을 하는 이유는 select로 하나만 가져와도 title자체는 리스트이기 때문입니다.
    # 즉, 제목 글자는 title이라는 리스트의 0번(첫번째)에 들어가 있습니다.
    print(author)

    # 위 소스는 첫 페이지에서 버튼을 클릭해야 넘어가는 시스템 설정상 불가능...
    # 다음 강의에서 가능할듯...



    


