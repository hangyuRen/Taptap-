# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-20 9:51
@Auth ： hyuRen
"""

import urllib.error
import urllib.request
import json
import csv


def get_game_id(base_url, XUA):
    id_list = []
    for i in range(50):
        try:
            url = base_url + XUA + f'&from={i * 10}' + '&limit=10'
            response = ask_url(url)
            response = json.loads(response)
            data = response['data']['list']

            for dt in data:
                game_id = dt['id']
                id_list.append(game_id)
        except:
            continue
    return id_list


def get_data(detail_base_url, XUA, download_base_url, review_url, id_list):
    data_list = []
    for i in id_list:
        try:
            data = []
            url = detail_base_url + f'{i}?' + XUA

            response = ask_url(url)

            response = json.loads(response)

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
            # 游戏类型标签
            tags = response['data']['tags']
            t = []
            for tag in tags:
                t.append(tag['value'])
            all_tag = ",".join(t)

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
        except:
            continue
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


if __name__ == '__main__':
    tag = ['Tap+Exclusive', '%E5%8D%95%E6%9C%BA', '%E5%8A%A8%E4%BD%9C', '%E5%A4%9A%E4%BA%BA',
           '%E6%A8%A1%E6%8B%9F%E7%BB%8F%E8%90%A5', '%E8%A7%92%E8%89%B2%E6%89%AE%E6%BC%94', '%E4%BC%91%E9%97%B2',
           '%E7%AD%96%E7%95%A5', '%E5%86%92%E9%99%A9', '%E5%8D%A1%E7%89%8C', '%E5%B0%84%E5%87%BB',
           '%E4%BA%8C%E6%AC%A1%E5%85%83', 'Roguelike', '%E8%A7%A3%E8%B0%9C', '%E6%96%87%E5%AD%97', '%E9%9F%B3%E6%B8%B8',
           '%E5%A5%B3%E6%80%A7%E5%90%91', '%E6%B2%99%E7%9B%92', '%E5%BC%80%E6%94%BE%E4%B8%96%E7%95%8C', 'MMORPG',
           '%E6%AD%A6%E4%BE%A0', '%E5%9B%BD%E9%A3%8E', '%E7%AB%9E%E9%80%9F', '%E7%9B%8A%E6%99%BA',
           '%E7%94%9F%E5%AD%98', 'MOBA', '%E6%94%BE%E7%BD%AE', '%E5%A1%94%E9%98%B2', '%E5%83%8F%E7%B4%A0',
           '%E6%B2%BB%E6%84%88', '%E6%A0%BC%E6%96%97', '%E9%AD%94%E6%80%A7', '%E6%9C%AB%E6%97%A5']

    list_name = ['tap_exclusive', 'single_player', 'action', 'multi_player', 'simulation', 'rpg', 'casual', 'strategy',
                 'adventure', 'card', 'shooter', 'acgn', 'rogue_like', 'puzzle', 'word', 'music', 'otome_game',
                 'sand_box', 'open_world', 'mmorpg', 'swords_man', 'chinese_style', 'racing', 'intelligence',
                 'survival', 'moba', 'idle', 'tower_defence', 'pixel', 'healing', 'fighting', 'addictive', 'apocalypse']

    base_url = "https://www.taptap.cn/webapiv2/app-tag/v1/by-tag?_trackParams=%7B%22refererLogParams%22:%7B%7D%7D&"

    detail_base_url = "https://www.taptap.cn/webapiv2/app/v2/detail-by-id/"

    XUA = "&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Den-US%26VN_CODE%3D101%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid" \
          "%26UID%3Dffa4c2c9-ce96-4b18-b2ef-86cdce779912%26DT%3DPC%26OS%3DWindows%26OSV%3D14.0.0"

    review_url = "https://www.taptap.cn/webapiv2/review/v1/trend?app_id="

    download_base_url = "https://www.taptap.cn/app/"

    save_path = "tap/all_kind.csv"

    with open(save_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['game_name', 'score', 'hits', 'fans', 'pos_count', 'neg_count',
                         'type', 'download_url', 'image_url', 'company_name'])

        for i in range(len(tag)):
            url = base_url + "&tag=" + tag[i]
            id_list = get_game_id(url, XUA)
            print(i, id_list)
            data_list = get_data(detail_base_url, XUA, download_base_url, review_url, id_list)
            for data in data_list:
                writer.writerow(data)
