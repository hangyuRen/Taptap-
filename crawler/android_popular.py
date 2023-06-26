# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-19 15:37
@Auth ： hyuRen
"""

import urllib.error
import urllib.request
import json
import csv
from json import JSONDecodeError


def get_game_id(base_url, XUA):
    id_list = []
    for i in range(15):
        url = base_url + XUA + f'&from={i * 10}' + '&limit=10'
        response = ask_url(url)
        response = json.loads(response)
        data = response['data']['list']

        for dt in data:
            try:
                game_id = dt['app']['id']

            except KeyError as e:
                continue
            id_list.append(game_id)
    return id_list


def get_data(detail_base_url, XUA, download_base_url, review_url, data_id):
    data_list = []
    for i in data_id:
        data = []
        url = detail_base_url + f'{i}?' + XUA
        print(url)
        try:
            response = ask_url(url)
            response = json.loads(response)
        except JSONDecodeError as e:
            continue
        # 游戏名称
        game_name = response['data']['title']
        data.append(game_name)
        # 游戏评分
        score = response['data']['stat']['rating']['score']
        data.append(score)
        # 下载量
        hits_total = response['data']['stat']['hits_total']
        data.append(hits_total)
        # 粉丝数
        fans_count = response['data']['stat']['fans_count']
        data.append(fans_count)
        # 一个月之内的积极评价与消极评价数
        review = review_url + f'{i}&' + XUA
        result = json.loads(ask_url(review))
        comments = result['data']['trend']
        pos_count = 0
        neg_count = 0
        for comment in comments:
            pos_count += comment['positive_count']
            neg_count += comment['negative_count']
        data.append(pos_count)
        data.append(neg_count)

        try:
            # 游戏类型标签
            tags = response['data']['tags']
            t = []
            for tag in tags:
                t.append(tag['value'])
            all_tag = ",".join(t)
        except KeyError as e:
            all_tag = None
        data.append(all_tag)
        # 游戏下载链接
        download_url = download_base_url + f'{i}'
        data.append(download_url)
        # 游戏图像下载链接
        image_url = response['data']['icon']['original_url']
        data.append(image_url)
        # 游戏公司名称
        company_name = response['data']['developers'][0]['name']
        data.append(company_name)
        data_list.append(data)

    return data_list


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
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def save_data(data_list, save_path):
    with open(save_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['game_name', 'score', 'hits', 'fans', 'pos_count', 'neg_count',
                         'type', 'download_url', 'image_url', 'company_name'])
        for data in data_list:
            writer.writerow(data)


if __name__ == '__main__':
    base_url = "https://www.taptap.cn/webapiv2/app-top/v2/hits?platform=android&type_name=hot&dataSource=Android&"

    detail_base_url = "https://www.taptap.cn/webapiv2/app/v2/detail-by-id/"

    XUA = "X-UA=V%3D1%26PN%3DWebApp%26LANG%3Den-US%26VN_CODE%3D101%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid" \
          "%26UID%3Dffa4c2c9-ce96-4b18-b2ef-86cdce779912%26DT%3DPC%26OS%3DWindows%26OSV%3D14.0.0"

    review_url = "https://www.taptap.cn/webapiv2/review/v1/trend?app_id="

    download_base_url = "https://www.taptap.cn/app/"

    save_path = 'tap/android_popular.csv'

    data_id = get_game_id(base_url, XUA)
    data = get_data(detail_base_url, XUA, download_base_url, review_url, data_id)
    # print(data)
    save_data(data, save_path)