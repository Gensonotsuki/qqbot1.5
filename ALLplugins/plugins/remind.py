#!/home/qbprjENV/bin/python
import time
from datetime import datetime

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
from ALLplugins.plugins.ep7crawl import push_article, saveE7news
from DataBaseLinkStart import link_local_mongo

__plugin_name__ = '会战前一天晚上进行配置提醒\n自动转发论坛'
bot = nonebot.get_bot()
e7MDB = link_local_mongo()


# 每周2,4,星期天晚上11点半提醒团战配置
@nonebot.scheduler.scheduled_job('cron', day_of_week='1,3,6', hour=23, minute=20, jitter=30, timezone='Asia/Shanghai')
async def _():
    global bot
    try:
        await bot.send_group_msg(group_id=615086637,
                                 message='现在晚上11点20分，[CQ:at,qq=309787171]赶快去配置团战[CQ:emoji,id=128522][CQ:emoji,id=128522][CQ:emoji,id=128522]')
    except CQHttpError:
        pass


# 每周3下午3点到10点，半小时爬一次，有更新时就推送到群里面
@nonebot.scheduler.scheduled_job('cron',
                                 day_of_week=2,
                                 hour='14-22',
                                 minute='0,5,10,15,20,25,30,35,40,45,50,55',
                                 jitter=30, timezone='Asia/Shanghai')
async def _():
    global bot, e7MDB
    e7news_set = e7MDB.ep7.ep7_news_set
    e7_local_news = e7news_set.find().sort('article_id', -1)
    local_news_title = [i['article_title'] for i in e7_local_news]
    latest_news = push_article(e7news_set)
    if latest_news:
        print(latest_news)
        bbs_article_title = [i['article_title'] for i in latest_news]
        new_article_title = set(bbs_article_title) - set(local_news_title)
        if new_article_title:
            try:
                await bot.send_group_msg(group_id=615086637,
                                     message='论坛有最新公告哟~请使用‘qb 公告’进行查询\n' + '\n'.join(new_article_title))
                saveE7news(latest_news)
            except CQHttpError:
                pass
    time.sleep(30)

    # e7news = e7news_set.find().sort('article_id', -1).limit(10)
    # local_news_title = [i['article_title'] for i in e7news]


@nonebot.scheduler.scheduled_job('cron',
                                 day_of_week='0, 1, 3, 4, 5, 6',
                                 hour='8-18',
                                 minute='0,30',
                                 jitter=40, timezone='Asia/Shanghai')
async def _():
    global bot, e7MDB
    e7news_set = e7MDB.ep7.ep7_news_set
    e7_local_news = e7news_set.find().sort('article_id', -1).limit(10)
    local_news_title = [i['article_title'] for i in e7_local_news]
    latest_news = push_article(e7news_set)
    if latest_news:
        bbs_article_title = [i['article_title'] for i in latest_news]
        new_article_title = set(bbs_article_title) - set(local_news_title)
        print(local_news_title)
        try:
            await bot.send_group_msg(group_id=615086637,
                                     message='论坛有最新公告哟~请使用‘qb 公告’进行查询\n' + '\n'.join(new_article_title))

        except CQHttpError:
            pass
        saveE7news(latest_news)
    time.sleep(30)

    # e7news = e7news_set.find().sort('article_id', -1).limit(10)
    # local_news_title = [i['article_title'] for i in e7news]
