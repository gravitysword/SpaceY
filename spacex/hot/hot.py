import requests,json,time,threading

from datetime import datetime
from lxml import html
from playwright.sync_api import sync_playwright


import sys,os
sys.path.append("/".join(os.path.abspath(__file__).split("\\")[:-3]))
from utils import sql

with open(r"../config/config.json", 'r', encoding='utf-8') as f:
    conf = json.load(f)
    executable_path = conf["executable_path"]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}


def bili():
    url = 'https://app.bilibili.com/x/v2/search/trending/ranking?csrf=2428441945548b6375dcfafc0d488df4&limit=80'
    response = requests.get(url, headers=headers).text
    b = [{"rank": i['position'], "name": i['show_name'], "hot": "0", "hot_id": i['hot_id'],
          "hot_url": "https://search.bilibili.com/all?keyword=" + i['keyword']}
         for i in json.loads(response)['data']['list']]

    sql.update_hot('bili', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), b)


def baidu():
    url = "https://top.baidu.com/board?tab=realtime"
    tree = html.fromstring(requests.get(url, headers=headers).text)
    hot_list = tree.xpath(
        '/html/body/div/div/main/div[2]/div/div[2]//div[@class="category-wrap_iQLoo horizontal_1eKyQ"]')

    b = [{"rank": i.xpath('./a/div')[0].text_content().replace(' ', ''),
          "name": i.xpath('.//div[@class="c-single-text-ellipsis"]')[0].text_content(),
          "hot": i.xpath('./div[1]/div[2]')[0].text_content(),
          "hot_id": "0",
          "hot_url": i.xpath('./a')[0].get('href')}
         for i in hot_list if i.xpath('./a/div')[0].text_content().replace(' ', '') != '']

    sql.update_hot('baidu', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), b)


def zhihu():
    url = "https://www.zhihu.com/billboard"
    tree = html.fromstring(requests.get(url, headers=headers).text)
    script = json.loads(tree.xpath('//script[@id="js-initialData"]')[0].text_content())
    hot_list = script["initialState"]["topstory"]["hotList"]

    b = [{"rank": rank+1,
          "name":  i["target"]["titleArea"]["text"],
          "hot": i["target"]["metricsArea"]["text"],
          "hot_id": i["id"],
          "hot_url": i["target"]["link"]["url"]}
         for rank,i in enumerate(hot_list)]


    sql.update_hot('zhihu', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), b)


def weibo():
    url = "https://weibo.com/ajax/side/hotSearch"
    hot_list = json.loads(requests.get(url, headers=headers).text)['data']['realtime']
    b = [{"name": i['word'],
          "rank": i['rank'],
          "hot": i['num'],
          "hot_id": i["word_scheme"],
          "hot_url": f'https://s.weibo.com/weibo?q=%23{i["word_scheme"]}%23'}
         for i in hot_list if not i.get('dot_icon')]

    sql.update_hot('weibo', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), b)


def douyin():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,executable_path=executable_path)
        context = browser.new_context()
        def intercept_request(route, request):
        # 拦截并阻止加载媒体文件
            if request.resource_type in ["image", "media", "font"]:
                route.abort()
            else:
                route.continue_()

    # 设置请求拦截器
        context.route('**/*', intercept_request)
        page = context.new_page()
        page.goto("https://www.douyin.com/hot/")
        page.wait_for_selector(".NINGm7vw")

        tree = html.fromstring(page.content())
        hot_list = tree.xpath('//ul[@class="WxZ6fnC5"]//li')[1:]
        b = [{"name": i.xpath('.//h3')[0].text_content(),
              "rank": index + 1,
              "hot": i.xpath('./div[@class="LiUahKtA"]/div[@class="iDGU44Jx"]/span[@class="WreZoKD3"]')[
                  0].text_content(),
              "hot_id": "0",
              "hot_url": "https://www.douyin.com" + i.xpath('.//div[@class="LiUahKtA"]/div[@class="DLjn0BsN"]/a')[
                  0].get('href')}
             for index, i in enumerate(hot_list)]

    sql.update_hot('douyin', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), b)


def toutiao():
    url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
    response = requests.get(url, headers=headers)
    data_response = json.loads(response.text)["data"]
    b = [{"name": i["Title"],
          "rank": rank + 1,
          "hot": i["HotValue"],
          "hot_id": i["ClusterIdStr"],
          "hot_url": i["Url"]}
         for rank, i in enumerate(data_response)]
    sql.update_hot('toutiao', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), b)


def kuaishou():
    url = "https://kuaishou.cn/?isHome=1"
    tree = html.fromstring(requests.get(url, headers=headers).text)
    ht_json = tree.xpath('//script')[1].text_content().replace('window.__APOLLO_STATE__=', '').replace(
        ';(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1]).parentNode.removeChild(s);}());',
        '')
    hot_li = json.loads(ht_json)['defaultClient']['$ROOT_QUERY.visionHotRank({"page":"home"})']["items"]
    items = json.loads(ht_json)['defaultClient']
    hot_list = [i["id"] for i in hot_li][1:]

    b = [{"rank": items[i]['rank'],
          "name": items[i]['name'],
          "hot": items[i]['hotValue'],
          "hot_id": items[i]['photoIds']['json'][:3],
          "hot_url": "https://www.kuaishou.cn/short-video/" + items[i]['photoIds']['json'][:3][0]}
         for i in hot_list]
    sql.update_hot('kuaishou', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), b)

def hot():
    platform = [baidu, bili, kuaishou, toutiao, weibo, zhihu, douyin]
    th = [threading.Thread(target=i, name=i.__name__) for i in platform]

    for t in th:
        t.start()
    for t in th:
        t.join()


if __name__ == '__main__':
    hot()
