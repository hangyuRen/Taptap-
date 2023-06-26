# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-21 20:39
@Auth ： hyuRen
"""

import urllib.error
import urllib.request
import json
import csv
from json import JSONDecodeError

def get_data(base_url, XUA, save_path, download_base_url, review_url):
    with open(save_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['game_name', 'score', 'hits', 'fans', 'pos_count', 'neg_count',
                         'type', 'download_url', 'image_url', 'company_name'])

        for i in range(1, 200000):
            print(i)
            try:
                url = base_url + f'{i}?' + XUA
                try:
                    response = ask_url(url)
                    response = json.loads(response)
                except JSONDecodeError as e:
                    continue
                # 游戏名称
                game_name = response['data']['title']
                # 游戏评分
                score = response['data']['stat']['rating']['score']
                # 下载量
                hits_total = response['data']['stat']['hits_total']
                # 粉丝数
                fans_count = response['data']['stat']['fans_count']
                # 一个月之内的积极评价与消极评价数
                review = review_url + f'{i}&' + XUA
                result = json.loads(ask_url(review))
                comments = result['data']['trend']
                pos_count = 0
                neg_count = 0
                for comment in comments:
                    pos_count += comment['positive_count']
                    neg_count += comment['negative_count']
                # 游戏类型标签
                try:
                    tags = response['data']['tags']
                    t = []
                    for tag in tags:
                        t.append(tag['value'])
                    all_tag = ",".join(t)
                except KeyError as e:
                    all_tag = ""
                # 游戏下载链接
                download_url = download_base_url + f'{i}'
                # 游戏图像下载链接
                image_url = response['data']['icon']['original_url']
                # 游戏公司名称
                company_name = response['data']['developers'][0]['name']

            except KeyError as e:
                continue
            writer.writerow([game_name, score, hits_total, fans_count, pos_count, neg_count, all_tag, download_url,
                             image_url, company_name])

def ask_url(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/114.0.0.0 Safari/537.36"
    }
    request = urllib.request.Request(url=url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        pass
    return html


if __name__ == '__main__':
    base_url = "https://www.taptap.cn/webapiv2/app/v2/detail-by-id/"

    XUA = "X-UA=V%3D1%26PN%3DWebApp%26LANG%3Den-US%26VN_CODE%3D101%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid" \
          "%26UID%3Dffa4c2c9-ce96-4b18-b2ef-86cdce779912%26DT%3DPC%26OS%3DWindows%26OSV%3D14.0.0 "

    review_url = "https://www.taptap.cn/webapiv2/review/v1/trend?app_id="

    download_base_url = "https://www.taptap.cn/app/"

    save_path = 'tap/game_list.csv'

    get_data(base_url, XUA, save_path, download_base_url, review_url)