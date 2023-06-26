# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-20 9:29
@Auth ： hyuRen
"""

import urllib.error
import urllib.request
import json
import csv

def get_data(base_url):
    data_list = []
    for i in range(50):
        url = base_url + '&from=' + str(i * 10) + '&limit=' + str(10)
        url = url.replace(' ', '')
        response = ask_url(url)
        response = json.loads(response)
        data = response['data']['list']
        for dt in data:
            data_ = []
            game_name = dt['title']
            rate = dt['stat']['rating']['score']
            hits_total = dt['stat']['hits_total']
            fans = dt['stat']['fans_count']
            tags = dt['tags']
            t = []
            for tag in tags:
                t.append(tag['value'])
            all_tag = ",".join(t)

            data_.append(game_name)
            data_.append(rate)
            data_.append(hits_total)
            data_.append(fans)
            data_.append(all_tag)
            data_list.append(data_)
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
        writer.writerow(['游戏名称', '评分', '下载量', '粉丝数', '游戏类型'])
        for data in data_list:
            writer.writerow(data)


if __name__ == '__main__':
    base_url = "https://www.taptap.cn/webapiv2/app-tag/v1/by-tag?tag=%E5%8D%A1%E7%89%8C&_trackParams=%7B" \
               "%22refererLogParams%22:%7B%7D%7D&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Den-US%26VN_CODE%3D100%26VN%3D0.1.0" \
               "%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dffa4c2c9-ce96-4b18-b2ef-86cdce779912%26DT%3DPC%26OS" \
               "%3DWindows%26OSV%3D14.0.0 "
    save_path = 'card_list.csv'
    data = get_data(base_url)
    # print(data)
    save_data(data, save_path)