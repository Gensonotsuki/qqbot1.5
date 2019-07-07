#!/home/qbprjENV/bin/python
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand, NLPResult

import pandas as pd
import numpy as np
import os
import json

from DataBaseLinkStart import linksqlengine, savesth
from config import GROUP_LIST
from ALLplugins.plugins.catalyst.model import Hero, Nicename
from .data_source import get_chater

__plugin_name__ = '迷宫聊天查询器，输入‘qb 迷宫聊天'

# 获取根路径
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("qqbot\\") + len("qqbot\\")]

# 获取英雄名json文件路径和文件
nickname = os.path.abspath(rootPath + '\\nickname.json')
e7_hero_decode = json.load(open(nickname, 'r'))

# 获取迷宫聊天选项翻译文件
chat_decode = os.path.abspath(rootPath + '\\chat_decode.json')
e7_chat_decode = json.load(open(chat_decode, 'r'))

# 获取迷宫聊天数据路径与文件
migongdate = os.path.abspath(rootPath + '\\e7migongdate.xlsx')
chat_list = pd.read_excel(migongdate)

dbsession = linksqlengine()


# 从db中获取英雄名


@on_command('maza_chater', aliases=('迷宫聊天'), only_to_me=False)
async def maza_chater(session: CommandSession):
    user = session.ctx['user_id']
    hero_list = session.ctx['message'][0].data['text'].split(' ')[1:]

    ker = ''.join(hero_list)
    er_wd = [
        f'{ker}中的一个或多个未找到[CQ:face,id=106]\n请将他们的名字写正确哦[CQ:face,id=6]\n或输入q中断当前查询并通过\t添加外号 已有英雄外号如:木飞 该英雄新的外号如:木飞剑\t进行添加操作',
        '有重复的英雄呢[CQ:face,id=104]\n请输出正确的四名英雄']
    if hero_list and len(hero_list) == 4:
        rs = await get_unser(hero_list)
        if rs in er_wd:
            session.pause(f'[CQ:at,qq={user}]\n{rs}')
        await session.send(f'[CQ:at,qq={user}]\n' + rs)
    else:
        chat_menber = session.get('chat_menber', prompt='没有找到4个人,请单独列出想要聊天的4个人[CQ:face,id=13]')
        await session.send(f'[CQ:at,qq={user}]\n' + chat_menber)


@maza_chater.args_parser
async def _(session: CommandSession):
    cat = session.current_arg_text.strip()
    q = ('q', '已中断聊天查询')
    if cat == 'q':
        session.state[session.current_key] = q[1]
        return
    stripped_arg = cat.strip().split()
    ker = ''.join(stripped_arg)
    er_wd = [
        f'{ker}中的一个或多个未找到[CQ:face,id=106]\n请将他们的名字写正确哦[CQ:face,id=6]\n或输入q中断当前查询并通过\t添加外号 已有英雄外号如:木飞 该英雄新的外号如:木飞剑\t进行添加操作',
        '有重复的英雄呢[CQ:face,id=104]\n请输出正确的四名英雄']
    if session.is_first_run:
        if len(stripped_arg) == 4:
            rs = await get_unser(stripped_arg)
            if rs in er_wd:
                session.pause(f'{rs}')
            session.state['test'] = rs
        return
    if len(stripped_arg) != 4:
        session.pause('似乎没有4个人呢[CQ:face,id=106]\n请用空格将其隔开')
    rs = await get_unser(stripped_arg)

    if rs in er_wd:
        session.pause(f'{rs}')
    session.state[session.current_key] = rs


async def get_unser(chat_menber) -> str:
    global chat_list, e7_chat_decode, e7_hero_decode
    Hero1, Hero2, Hero3, Hero4 = chat_menber
    try:
        Hero1_en = dbsession.query(Hero).join(Nicename).filter(Nicename.nicename == Hero1).one().heroname
        Hero2_en = dbsession.query(Hero).join(Nicename).filter(Nicename.nicename == Hero2).one().heroname
        Hero3_en = dbsession.query(Hero).join(Nicename).filter(Nicename.nicename == Hero3).one().heroname
        Hero4_en = dbsession.query(Hero).join(Nicename).filter(Nicename.nicename == Hero4).one().heroname
    except:
        ker = ''.join(chat_menber)
        return f'{ker}中的一个或多个未找到[CQ:face,id=106]\n请将他们的名字写正确哦[CQ:face,id=6]\n或通过\t添加外号 已有英雄外号如:木飞 该英雄新的外号如:木飞剑\t进行添加操作'

    check_repeat = [Hero1_en, Hero2_en, Hero3_en, Hero4_en]
    if len(set(check_repeat)) != 4:
        return '有重复的英雄呢[CQ:face,id=104]\n请输出正确的四名英雄'

    pick = chat_list.loc[
        (chat_list['Hero'] == Hero1_en) | (chat_list['Hero'] == Hero2_en) | (chat_list['Hero'] == Hero3_en) | (
                chat_list['Hero'] == Hero4_en)]
    hero_chat = []
    for i in np.array(pick.iloc[:, :3]).tolist():
        hero_chat.append(i)
    creatVar = locals()
    k = {}
    for i in hero_chat:
        try:
            h1 = i[2] + '_' + str(i[0]).replace(' ', '')
            h2 = i[2] + '_' + str(i[1]).replace(' ', '')
        except:
            return f'{i[2]}他还不会聊天呢'
        creatVar[h1] = pick[~pick['Hero'].isin([i[2]])][i[0]]
        creatVar[h2] = pick[~pick['Hero'].isin([i[2]])][i[1]]
        k[h1] = sum(creatVar.get(h1))
        k[h2] = sum(creatVar.get(h2))
    chat_res = sorted(zip(k.values(), k.keys()), reverse=True)
    best_chater = []
    mood = ''
    total = 0
    times = 0
    for i in chat_res:
        chater, choice = i[1].split('_')
        if choice != mood:
            # 通过英文名得到中文名
            cnname = dbsession.query(Nicename).join(Hero).filter(Hero.heroname == chater).one().nicename
            # for j in filter(lambda x: chater == x[1], e7_hero_decode.items()):
            #     print(77777777777777, j)
            #     if j[0] in chat_menber and times != 2:
            #         total += i[0]
            #         best_chater.append(f'<{j[0]}>的<{e7_chat_decode[choice]}>让大家的疲劳值恢复了{i[0]}点')
            #         times += 1
            if cnname in chat_menber and times != 2:
                total += i[0]
                best_chater.append(f'<{cnname}>的<{e7_chat_decode[choice]}>让大家的疲劳值恢复了{i[0]}点')
                times += 1
        mood = choice
    best_chater.append(f'共增加大家{total}点疲劳值')

    best_chater_res = '\n'.join(best_chater[:2])
    return f'{best_chater_res}\n{best_chater[-1]}'


@on_natural_language(keywords={'迷宫聊天'})
async def _(session: NLPSession):
    return IntentCommand(100, 'maza_chater')


# 添加外号
@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    global nickname
    if session.ctx.get('group_id') not in GROUP_LIST:
        return None
    res = None
    msg_box = session.msg.strip().split()
    if msg_box[0] == '添加外号':
        # 得到英雄id
        Hero_id = dbsession.query(Hero).join(Nicename).filter(Nicename.nicename == msg_box[1]).one().id
        # 构造插入语句
        insert = {'hero_id': Hero_id, 'nicename': msg_box[2], 'delete': 1}
        try:
            rs = savesth(insert)
            if rs:
                # e7_hero_decode[msg_box[2]] = e7_hero_decode[msg_box[1]]
                res = NLPResult(100, 'add_nicname', {'message': '外号添加成功'})
                # json.dump(e7_hero_decode, open(nickname, 'w'))
                return res
            res = NLPResult(100, 'add_nicname', {'message': '外号添加超时'})
            return res
        except:
            res = NLPResult(100, 'add_nicname', {'message': '外号添加超时'})
            return res

    if msg_box[0] == '查看外号':
        try:
            hero_obj = dbsession.query(Hero).join(Nicename).filter(Nicename.nicename == msg_box[1]).one()
            res = NLPResult(100, 'check_nicname', {'message': hero_obj.heroname + f'：{hero_obj.nicename}'})
            return res
        except:
            res = NLPResult(100, 'check_nicname', {'message': '查询超时,请重试'})
            return res


@on_command('add_nicname', only_to_me=False)
async def _(session: CommandSession):
    rs = session.args['message']
    await session.send(rs)


@on_command('check_nicname', only_to_me=False)
async def _(session: CommandSession):
    rs = session.args['message']
    await session.send(rs)
