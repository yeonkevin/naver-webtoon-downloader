import requests, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from itertools import count
from collections import OrderedDict

def get_list(title_id):
    list_url = 'http://comic.naver.com/webtoon/list.nhn?'
    ep_dict = OrderedDict()

    for page in count(1):
        params = {
            'titleId' : 641253,
            'page' : page,
        }

        html = requests.get(list_url, params=params).text
        soup = BeautifulSoup(html, 'html.parser')

        tag_list = soup.select('.title > a')

        for tag in tag_list:
            ep_name = tag.text
            ep_url = urljoin(list_url, tag['href'])
            if ep_url in ep_dict:
                return ep_dict

            ep = {
                'url' : ep_url,
                'name' : ep_name,
            }

            ep_dict[ep_url] = ep
            
            
def download_img():
    ep_url = 'http://comic.naver.com/webtoon/detail.nhn?titleId=641253&no=141&weekday=fri'
    html = requests.get(ep_url).text
    soup = BeautifulSoup(html, 'html.parser')

    for idx, tag in enumerate(soup.select('.wt_viewer img'), 1):
        img_url = tag['src']

        headers = {
            'Referer' : ep_url
        }
        img_data = requests.get(img_url, headers=headers).content
        img_name = str(idx) + '' + os.path.basename(img_url)[-4:]

        with open(img_name, 'wb') as f:
            f.write(img_data)

        

get_list(641253) #외모 지상 주의
download_img()