# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-20 9:51
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
    base_url = "https://www.taptap.cn/webapiv2/app-tag/v1/by-tag?_trackParams=%7B" \
               "%22refererLogParams%22:%7B%7D%7D&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Den-US%26VN_CODE%3D100%26VN%3D0.1.0" \
               "%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dffa4c2c9-ce96-4b18-b2ef-86cdce779912%26DT%3DPC%26OS" \
               "%3DWindows%26OSV%3D14.0.0"
    for i in range(len(tag)):
        url = (base_url + '&tag=' + tag[i]).replace(' ', '')
        save_path = 'tap/' + list_name[i] + '.csv'
        data = get_data(url)
        # print(data)
        save_data(data, save_path)