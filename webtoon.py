import requests
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
            print(ep_name, ep_url)


get_list(641253) #외모 지상 주의