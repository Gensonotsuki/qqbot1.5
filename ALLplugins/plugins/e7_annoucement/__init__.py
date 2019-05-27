#!/home/qbprjENV/bin/python
from nonebot.permission import SUPERUSER, GROUP_ADMIN
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

from ALLplugins.plugins.ep7crawl import push_article, saveE7news
from DataBaseLinkStart import link_local_mongo
from config import SESSION_RUN_TIMEOUT
from .data_source import get_annoucement

__plugin_name__ = '官方论坛公告查询，输入‘qb公告’'
__plugin_usage__ = r'''
官方论坛公告查询

请回复qb 公告
'''

e7OBJ = link_local_mongo(host='127.0.0.1', port=27017)


@on_command('e7news', aliases=('公告'), only_to_me=False)
async def e7news(session: CommandSession):
    world = await get_act_title()
    wtsact = session.get('wtsact', prompt=world)
    act_text = await get_act(wtsact)
    await session.send(act_text)
    return act_text


# 收到公告命令后进入等待态，执行后续
@e7news.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）

        if stripped_arg:
            # 第一次运行参数不为空
            session.state['wtsact'] = stripped_arg
        return
    if not stripped_arg:
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要查询的公告编号不能为空[CQ:face,id=74][CQ:face,id=74]')

    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


# 查询数据库，返回最近公告列表
async def get_act_title() -> str:
    global e7OBJ
    e7news = e7OBJ.ep7.ep7_news_set
    res = e7news.find().sort('article_id', -1).limit(10)
    title_list = ''
    No = 1
    for i in res:
        try:
            title_list += (str(No) + '、' + i['article_title'] + '\t' + i['up_time'] + '\n')
        except:
            title_list += (str(No) + '、' + i['article_title'] + '\n')
        No += 1

    return f'官方论坛最新公告：\n{title_list}请回复数字查看详情~'


# 查询数据库，返回所查询公告
async def get_act(numbuer) -> str:
    global e7OBJ
    e7news = e7OBJ.ep7.ep7_news_set
    res = e7news.find().sort('article_id', -1).limit(10)
    article = res[int(numbuer) - 1]['article']
    return f'{article}'


# 使用自然语言处理器
@on_natural_language(keywords={'公告'})
async def _(session: NLPSession):
    return IntentCommand(90, 'e7news')


@on_natural_language(keywords={'更新论坛'}, permission=SUPERUSER | GROUP_ADMIN)
async def _(session: NLPSession):
    return IntentCommand(90, 'forceFix')


@on_command('forceFix', aliases='更新论坛', only_to_me=False)
async def _(session: CommandSession):
    await session.send('请稍等，该过程会比较慢')
    global e7OBJ
    E7_news_set = e7OBJ.ep7.ep7_news_set
    article = push_article(E7_news_set)
    if not article:
        await session.send('暂时没有更新新闻哦，请稍后再尝试查询')
        return
    e7_local_news = E7_news_set.find().sort('article_id', -1).limit(10)
    local_news_title = [i['article_title'] for i in e7_local_news]
    bbs_article_title = [i['article_title'] for i in article]
    new_article_title = set(bbs_article_title) - set(local_news_title)
    saveE7news(article)
    await session.send('论坛有最新公告哟~请使用‘qb 公告’进行查询\n' + '\n'.join(new_article_title))
