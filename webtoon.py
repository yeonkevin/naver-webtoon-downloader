import requests, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from itertools import count
from collections import OrderedDict
from PIL import Image

def get_list(title_id):
    list_url = 'http://comic.naver.com/webtoon/list.nhn?'
    ep_dict = OrderedDict()

    for page in count(1):
        params = {
            'titleId' : title_id,
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
            ep_download(ep_url)

def ep_download(urls):
    img_path_list = [] 
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
        img_path_list.append(img_path)
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

    
    ep_merge(img_path_list, os.path.join(webtoon_name, ep_name))
        

def ep_merge(ep_list, ep_name):
    img_path_list = ep_list
    webtoon_name = ep_name
    im_list = []
    merge_path = '{}/merged.png'.format(webtoon_name)

    dir_path = os.path.dirname(merge_path)

    if os.path.isfile(dir_path):
        print('merged.png는 이미 존재 합니다.')
        return 0

    for img_path in img_path_list:
        im = Image.open(img_path)
        im_list.append(im)

    canvas_size = (max(im.width for im in im_list), sum(im.height for im in im_list))

    canvas = Image.new('RGB', canvas_size)

    left = 0
    top = 0

    for im in im_list:
        canvas.paste(im, (left, top))
        top += im.height

    canvas.save(merge_path)

get_list(696602)
print('SAVE COMPLETE!!')
