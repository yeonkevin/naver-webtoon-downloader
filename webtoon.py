import requests
from bs4 import BeautifulSoup

list_url = 'http://comic.naver.com/webtoon/list.nhn?'

params = {
    'titleId' : 641253,
    'pages' : 1
}

html = requests.get(list_url, params=params).text
soup = BeautifulSoup(html, 'html.parser')

tag_list = soup.select('.title > a')

for tag in tag_list:
    print(tag.text)
