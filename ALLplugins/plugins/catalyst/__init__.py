#!/home/qbprjENV/bin/python
from nonebot import on_command, on_natural_language, \
    CommandSession, NLPSession, IntentCommand

from ALLplugins.plugins.catalyst.model import hero_constellations, constellation_catalyst, catalyst_shop, \
    Nicename, Hero, Constellation, Catalyst, Shop
from DataBaseLinkStart import linksqlengine

__plugin_name__ = '催化剂出处查询器，输入‘qb 催化剂 需求 催化剂名\nqb 催化剂 英雄名 需求'

dbsession = linksqlengine()

allcatalyst = dbsession.query(Catalyst).all()


@on_natural_language(keywords='催化剂')
async def _(session: NLPSession):
    return IntentCommand(100, 'getcatalyst')


@on_command('getcatalyst', aliases='催化剂', only_to_me=False)
async def getcatalyst(session: CommandSession):
    user = session.ctx['user_id']
    needlist = session.ctx['message'][0].data['text'].split(' ')[1:]
    if needlist[0] == '需求':
        rs = await hero_shop(needlist[1])
        await session.send(f'[CQ:at,qq={user}]\n{rs}')
    elif needlist[1] == '需求':
        rs = await shop_catalyst(needlist[0])
        await session.send(f'[CQ:at,qq={user}]\n{rs}')


@getcatalyst.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['havesth'] = stripped_arg


# 通过催化剂名查英雄列表和对应商店
async def hero_shop(sth):
    try:
        herolist = dbsession.query(Nicename.nicename).join(Hero).join(hero_constellations).join(Constellation).join(
            constellation_catalyst).join(Catalyst).filter(Catalyst.catalyst == sth).all()

        shoplist = dbsession.query(Shop).join(catalyst_shop).join(Catalyst).filter(Catalyst.catalyst == sth).all()
    except:
        return '查询超时,请稍后重试'
    if herolist and shoplist:
        wd = ''

        for heroname in herolist:
            wd += heroname.nicename + '，'

        rs = f'{wd[:-1]}\n以上英雄需求{sth}\n分别在↓↓↓\n{shoplist}\t有售\n或通过3级炼金塔炼制而成'
        return rs
    return f'没有催化剂---{sth}---请检查，以下为催化剂列表\n{allcatalyst}'


# 通过英雄名查所需催化剂和哪个图商店买
async def shop_catalyst(sth):
    try:
        catalystlist = dbsession.query(Catalyst).join(constellation_catalyst).join(Constellation).join(
            hero_constellations).join(
            Hero).join(Nicename).filter(Nicename.nicename == sth).all()

        shoplist = dbsession.query(Shop).join(catalyst_shop).join(Catalyst).join(constellation_catalyst).join(
            Constellation).join(
            hero_constellations).join(Hero).join(Nicename).filter(Nicename.nicename == sth).all()
    except:
        return '查询超时,请稍后重试'
    if catalystlist and shoplist:
        return f'{sth}需求{catalystlist}\n分别在↓↓↓\n{shoplist}\t有售\n或通过3级炼金塔炼制而成'
    return f'未找到---{sth}'
