# parser.py
import requests
from bs4 import BeautifulSoup
import json
import os
from sv_1 import*


# python파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

req = requests.get(URL)
html = req.text
soup = BeautifulSoup(html, 'html.parser')
my_titles = soup.select(
    'h3 > a'
    )

data = {}

for title in my_titles:
    data[title.text] = title.get('href')

with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
    json.dump(data, json_file)
