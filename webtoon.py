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
            download_img(ep_url)
            
            
def download_img(urls):
    ep_url = urls
    html = requests.get(ep_url).text
    soup = BeautifulSoup(html, 'html.parser')

    for idx, tag in enumerate(soup.select('.wt_viewer img'), 1):
        img_url = tag['src']
        webtoon_name =  ' '.join(soup.select('.comicinfo .detail h2')[0].text.split())
        ep_name = soup.select('.tit_area h3')[0].text

        headers = {
            'Referer' : ep_url
        }

        img_name = str(idx) + '' + os.path.basename(img_url)[-4:]

        img_path = os.path.join(webtoon_name, ep_name, img_name)
        dir_path = os.path.dirname(img_path)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        if not os.path.exists(img_path):
            img_data = requests.get(img_url, headers=headers).content
            with open(img_path, 'wb') as f:
                f.write(img_data)
            print('DOWNLOAD COMPLETE %s%s' % (ep_name, img_name))
        else:
            print('DOWNLOAD SKIP %s%s' % (ep_name, img_name))
        

get_list(641253) #외모 지상 주의