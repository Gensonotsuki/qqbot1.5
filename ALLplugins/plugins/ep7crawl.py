#!/home/qbprjENV/bin/python
import datetime
import json
import math
import pytz
import re
import time

import requests

from DataBaseLinkStart import link_local_mongo

# 获取了全部页面的新闻
'''
# def e7crawl(page=15):
#     # 全部文章页面的请求头
#     mainpage_header = {
#         'Host': 'api.onstove.com',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
#         'Accept': 'application/json, text/plain, */*',
#         'Accept-Language': 'en',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Referer': 'http://page.onstove.com/epicseven/tw/main?listType=2&searchBoardKey=e7tw001',
#         'Content-Type': 'application/json;charset=utf-8',
#         'X-Device-Type': 'P01',
#         'X-Client-Lang': 'EN',
#         'X-Nation': 'CN',
#         'X-Timezone': 'Asia/Shanghai',
#         'X-Utc-Offset': '480',
#         'X-Lang': 'EN',
#         'X-UUID': '67482891-d182-4f1c-93cf-8ebfeaddf4ba',
#         'Content-Length': '584',
#         'Origin': 'http://page.onstove.com',
#         'Connection': 'keep-alive',
#         'Cache-Control': 'max-age=0',
#         'TE': 'Trailers',
#     }
# 
#     # 全部文章页面表单请求
#     mainpage_form_data = {"board_key": "e7tw001",
#                           "direction": "latest",
#                           "list_type": "3",
#                           "display_opt": "usertag_on,html_remove",
#                           "notice_type": "A",
# 
#                           "page": 1,
#                           "size": 15,
#                           "not_headline_nos": [],
#                           "access_token": 'eyJhbGciOiJIUzI1NiJ9.eyJhcHBsaWNhdGlvbl9ubyI6MTAwMDIsImNoZWNrIjoiWTtOO047TjtHQjtDTjtaSCIsIm5pY2tuYW1lIjoiU1RPVkU4NjMzNTUyMiIsInRva2VuIjoiODM2Mzg4YzczMGZiMzZlMWFhMmUxNTFjMzE3MTI0NzA0ODQxOGNkMmE2ZDMyOWY0ZTgyY2NjMjE4YTdhYTQyNCIsImV4cGlyZV90aW1lIjoxNTU1NDM4MzE0MTYwLCJiaXJ0aF9kdCI6bnVsbCwibWVtYmVyX25vIjo4NjMzNTUyMn0.4EdooyX7HQmOYly57V13saIBasDWar2yhMnLltEibRk',
#                           "cafe_key": "epicseven",
#                           "channel_key": "tw"}
# 
#     # 某个文章页面的请求头
#     artic_data = {
#         "access_token": None,
#         "cafe_key": "epicseven",
#         "card_no": "",
#         "channel_key": "tw",
#         "display_opt": "usertag_on,html_escape",
#         "game_id": "141",
#         "more_card_type": "normal",
#         "not_headline_nos": [],
#         "show_like_yn": "Y",
#     }
# 
#     # 某个文章页面的表单请求
#     artic_head = {
#         'Host': 'api.onstove.com',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
#         'Accept': 'application/json, text/plain, */*',
#         'Accept-Language': 'en',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Referer': 'http://page.onstove.com/epicseven/tw/board/list/e7tw001/view/3089511?listType=3&display_opt=usertag_on,html_remove&afterBack=true&boardKey=e7tw001',
#         'Content-Type': 'application/json;charset=utf-8',
#         'X-Device-Type': 'P01',
#         'X-Client-Lang': 'EN',
#         'X-Nation': 'CN',
#         'X-Timezone': 'Asia/Shanghai',
#         'X-Utc-Offset': '480',
#         'X-Lang': 'EN',
#         'X-UUID': '67482891-d182-4f1c-93cf-8ebfeaddf4ba',
#         'Content-Length': '205',
#         'Origin': 'http://page.onstove.com',
#         'Connection': 'keep-alive',
#         'Cache-Control': 'max-age=0',
#         'TE': 'Trailers'
#     }
# 
#     # 全部文章的响应
#     artic_id = []
#     artic_title = []
# 
#     page += 1
#     for i in range(1, page):
#         # 全部文章页面的数据接口,一共16页
#         nocache = math.floor(time.time() * 1000)
#         mainpage_url = f'https://api.onstove.com/cafe/v1/ArticleList?nocache={nocache}'
#         mainpage_form_data['page'] = i
#         main_page_response = requests.post(url=mainpage_url, data=json.dumps(mainpage_form_data),
#                                            headers=mainpage_header)
# 
#         print(f'正在获取第{i}页信息---')
#         # 清洗数据得到每个文章的id
#         mainpage_list = json.loads(main_page_response.text)['context']['article_list']
# 
#         for j in mainpage_list:
#             artic_id.append(j['card_no'])
#             artic_title.append(j['title'])
#         time.sleep(1)
# 
#     # 去重
#     artic_id = reduce(lambda x, y: x if y in x else x + [y], [[], ] + artic_id)
#     artic_title = reduce(lambda x, y: x if y in x else x + [y], [[], ] + artic_title)
#     print('去重结束')
# 
#     print('正在获取文章内容----')
#     # 获取每个文章的内容，为js格式
#     # 某个文章页面的数据接口
#     nocache = math.floor(time.time() * 1000)
#     artic_url = f'https://api.onstove.com/cafe/v1/ArticleInfo?nocache={nocache}'
#     all_articl_response = []
#     for i in artic_id:
#         artic_data['card_no'] = i
#         artic_response = requests.post(url=artic_url, data=json.dumps(artic_data), headers=artic_head)
#         try:
#             all_articl_response.append(json.loads(artic_response.text)['context'][
#                                            'content'] + f'\n本文详细地址\nhttp://page.onstove.com/epicseven/tw/board/list/e7tw002/view/{i}')
#         except:
#             continue
#         print(f'文章{i}解析结束')
#         time.sleep(1)
#     print('所有文章解析结束')
#     print('正在清洗文章内容-----')
#     # 去除html标签并格式化表格等内容
#     all_articl_list = []
#     for i in all_articl_response:
#         wrap = re.sub('</tr>|■', '\n', i)
#         tab = re.sub('</td>|&nbsp', '\t', wrap)
#         all_articl_list.append(re.sub('<.*?>', '', tab))
# 
#     print('正在合并文章信息------')
#     ep7_all_news = []
#     for i in zip(artic_id, artic_title, all_articl_list):
#         ep7_all_news.append({'article_id': i[0], 'article_title': i[1], 'article': i[2]})
# 
#     return ep7_all_news
'''


# 获取首页的文章响应
def e7_mainpage_crawl():
    mainpage_header = {
        'Host': 'api.onstove.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'http://page.onstove.com/epicseven/tw/main?listType=2&searchBoardKey=e7tw001',
        'Content-Type': 'application/json;charset=utf-8',
        'X-Device-Type': 'P01',
        'X-Client-Lang': 'EN',
        'X-Nation': 'CN',
        'X-Timezone': 'Asia/Shanghai',
        'X-Utc-Offset': '480',
        'X-Lang': 'EN',
        'X-UUID': '67482891-d182-4f1c-93cf-8ebfeaddf4ba',
        'Content-Length': '584',
        'Origin': 'http://page.onstove.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers',
    }
    mainpage_form_data = {"board_key": "all",
                          "direction": "latest",
                          "list_type": "2",
                          "display_opt": "usertag_on,html_remove",
                          "notice_type": "M",
                          "page": 1,
                          "size": 15,
                          "not_headline_nos": [],
                          "access_token": None,
                          "cafe_key": "epicseven",
                          "channel_key": "tw",
                          "ISmAIN": True
                          }
    print('开始获取首页文章接口')
    nocache = math.floor(time.time() * 1000)
    mainpage_url = f'https://api.onstove.com/cafe/v1/ArticleList?nocache={nocache}'
    try:
        main_page_response = requests.post(url=mainpage_url, data=json.dumps(mainpage_form_data),
                                           headers=mainpage_header)
        artic_list = json.loads(main_page_response.text)['context']['article_list']
        print('首页文章获取结束')
        article_id_list = []
        for article_id in artic_list:
            print('123')

            if article_id['user']['nickname'] == '卡卡小編':
                article_id_list.append(article_id['card_no'])
            print('456')
        article_id_list.sort(reverse=True)
        article_id_list = article_id_list[:10]
        return article_id_list
    except:
        print('连接超时')
        return None


# 根据文章id获取文章正文,返回标题和响应
def e7ArticleCrawl(new_article_id):
    artic_data = {
        "access_token": None,
        "cafe_key": "epicseven",
        "card_no": "3093109",
        "channel_key": "tw",
        "display_opt": "usertag_on,html_escape",
        "game_id": "141",
        "more_card_type": "normal",
        "not_headline_nos": [],
        "show_like_yn": "Y",
    }
    artic_head = {
        'Host': 'api.onstove.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'Referer: http://page.onstove.com/epicseven/tw/main/view/3167984?listType=2',
        'Content-Type': 'application/json;charset=utf-8',
        'X-Device-Type': 'P01',
        'X-Client-Lang': 'EN',
        'X-Nation': 'CN',
        'X-Timezone': 'Asia/Shanghai',
        'X-Utc-Offset': '480',
        'X-Lang': 'EN',
        'X-UUID': '67482891-d182-4f1c-93cf-8ebfeaddf4ba',
        'Content-Length': '559',
        'Origin': 'http://page.onstove.com',
        'Connection': 'keep-alive',
        'TE': 'Trailers'
    }
    nocache = math.floor(time.time() * 1000)
    artic_url = f'https://api.onstove.com/cafe/v1/ArticleInfo?nocache={nocache}'

    all_articl_response = []
    all_articl_title = []
    print('开始解析新闻内容')
    for card_id in new_article_id:
        print(f'开始解析{card_id}的内容')
        artic_data['card_no'] = card_id
        artic_response = requests.post(url=artic_url, data=json.dumps(artic_data), headers=artic_head)
        try:
            print(123123)
            res = json.loads(artic_response.text)['context']
            all_articl_response.append(res['content'])
            all_articl_title.append(res['title'])
            print(f'{card_id}解析结束,休息10秒')
            # time.sleep(10)
        except:
            print('解析失败，请检查')
            continue
    return all_articl_title, all_articl_response


# 获取最新文章，得到标题和清洗后的正文
def new_article(E7news_set):
    res = E7news_set.find().sort('article_id', -1)
    local_article_id = []
    local_article_title = []
    # 获取本地数据
    for i in res:
        local_article_id.append(i['article_id'])
        local_article_title.append(i['article_title'])
    local_article_id = local_article_id
    e7tw001_id_list = e7_mainpage_crawl()
    if e7tw001_id_list:
        try:
            new_artic_id, all_article_title, all_article = re_news(e7tw001_id_list, local_article_id)
        except:
            return None
        return new_artic_id, all_article_title, all_article
    return None


# 解析最新文章
def re_news(article_id_list, local_article_id):
    article_id_list.sort(reverse=True)
    article_id_list = article_id_list[:10]
    if article_id_list != local_article_id:
        new_artic_id = set(article_id_list) - set(local_article_id)
        print('开始爬取最新新闻')
        all_article_title, all_article_list = e7ArticleCrawl(new_artic_id)
        all_article = []
        for i in all_article_list:
            b = re.sub('</tr>|■', '\n', i)
            c = re.sub('</td>|&nbsp', '\t', b)
            d = re.sub('<.*?>', '', c)
            e = re.sub('。|;|；', '\n', d)
            all_article.append(e)
        return new_artic_id, all_article_title, all_article
    else:
        return None


# 整合文章id，标题，正文
def zip_article(article_id_list, all_article_title, all_article):
    complete = zip(article_id_list, all_article_title, all_article)
    e7_news = []
    print('开始整理文章')
    for i in complete:
        now = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))
        e7_news.append({'article_id': i[0], 'article_title': i[1], 'article': i[2],
                        'up_time': now.strftime('%m-%d %H:%M'),
                        'url': f'http://page.onstove.com/epicseven/tw/main/view/{i[0]}'})
    print('整理结束')
    return e7_news


# 推送最新文章
def push_article(E7news_set):
    article_list = new_article(E7news_set)
    if article_list:
        new_artic_id, all_article_title, all_article = article_list
        latest_news = zip_article(new_artic_id, all_article_title, all_article)
        return latest_news
    print(f'{datetime.datetime.now(tz=pytz.timezone("Asia/Shanghai"))}\ne7tw002没有最新文章\n')
    return None


# 自动爬取文章
def auto_crawl():
    E7news_set = link_local_mongo(host='127.0.0.1', port=27017).ep7.ep7_news_set
    print('数据库连接成功')
    while True:
        now = datetime.datetime.now(tz=pytz.timezone("Asia/Shanghai"))
        weekday = now.weekday()
        day_time = now.hour
        print(f'现在时间是{weekday}{day_time}点')

        print('开始爬取文章')
        latest_news = push_article(E7news_set)
        if latest_news:
            saveE7news(latest_news)
            print('数据存储完毕，开始休眠')
            time.sleep(300)
        print('真的特么没有最新文章，开始休眠半小时')
        time.sleep(1800)


# 存进MongoDB
def saveE7news(mess):
    e7cnt = link_local_mongo(host='127.0.0.1', port=27017)
    print(mess)
    E7news_set = e7cnt.ep7.ep7_news_set

    E7news_set.insert(mess)


if __name__ == '__main__':
    # mess = e7crawl()
    # saveE7news(mess)
    lis = auto_crawl()
    print(lis)
