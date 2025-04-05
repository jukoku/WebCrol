# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import sys
from sv_7 import*
from gs import Coupang
from wd import Coupang_web

PRICE = 200 # 100m당 가격 상한선

cp = Coupang()

cw = Coupang_web()

cw.store_pages()
cw.grab()