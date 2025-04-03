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
from sv import*

# json 파일이 위치한 경로를 값으로 줘야 합니다.

gc = gspread.service_account(json_file_path)
wks = gc.open_by_url(spreadsheet_url)
doc = wks.worksheet('확인')

