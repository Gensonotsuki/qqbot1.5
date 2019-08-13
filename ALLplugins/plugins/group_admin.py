#!/home/qbprjENV/bin/python
from nonebot.permission import SUPERUSER, GROUP_ADMIN
from nonebot import on_notice, NoticeSession, RequestSession, on_request, on_command, get_bot
from nonebot import on_natural_language, NLPSession, IntentCommand, CommandSession

from config import GROUP_LIST

__plugin_name__ = '塞口球TIME！那么是谁想被塞口球呢'

@on_request('group')
async def _(session: RequestSession):
    if session.ctx['group_id'] in GROUP_LIST and int(session.ctx['comment']) >= 4000:
        await session.approve()
        user_id = session.ctx['user_id']
        comment = session.ctx['comment']
        await session.send(
            f'有新大佬[CQ:at,qq={user_id}]入群[CQ:emoji,id=127881][CQ:emoji,id=127881][CQ:emoji,id=127881]\n大佬的竞技场积分竟然有：{comment}！！！\nDL，SDL，AWSL')
        return


@on_notice('group_increase')
async def _(session: NoticeSession):
    if session.ctx['group_id'] in GROUP_LIST:
        user_id = session.ctx['user_id']
        operator_id = session.ctx['operator_id']
        if session.ctx['sub_type'] == 'approve':
            await session.send(
                f'[CQ:atqq={operator_id}]同意了有大佬[CQ:at,qq={user_id}]的入群申请[CQ:emoji,id=127881][CQ:emoji,id=127881][CQ:emoji,id=127881]\nDL，SDL，AWSL')
        elif session.ctx['sub_type'] == 'invite':
            await session.send(
                f'[CQ:atqq={operator_id}]邀请了大佬[CQ:at,qq={user_id}][CQ:emoji,id=127881][CQ:emoji,id=127881][CQ:emoji,id=127881]\nDL，SDL，AWSL')


@on_natural_language(keywords={'塞他'}, permission=SUPERUSER | GROUP_ADMIN)
async def _(session: NLPSession):
    return IntentCommand(100, 'bantalk')


sender_list = []


@on_command('bantalk', aliases='塞他', only_to_me=False)
async def _(session: CommandSession):
    global sender_list
    bot = get_bot()
    sender_rank = session.ctx['sender']['role']
    sender_id = session.ctx['sender']['user_id']
    someone = session.ctx['message'][1]['data']['qq']
    try:
        ban_time = session.ctx['message'][2]['data']['text'][:2] * 60
    except:
        ban_time = 60
    if sender_rank in ['owner', 'admin']:
        await bot.set_group_ban(group_id=745494370, user_id=someone, duration=ban_time)
        await bot.send_group_msg(group_id=745494370, message=f'根据{sender_id}的要求\n{someone}被赐予口球,并塞了他{ban_time}秒')
        return
    sender_list.append(sender_id)
    if len(set(sender_list)) >= 3:
        await bot.set_group_ban(group_id=745494370, user_id=someone, duration=ban_time)
        await bot.send_group_msg(group_id=745494370, message=f'应广大人民的的恳求\n{someone}被赐予口球,并塞了他{ban_time}秒')
        return


@on_natural_language(keywords={'给管理'}, permission=SUPERUSER)
async def _(session: NLPSession):
    return IntentCommand(100, 'addadmins')


@on_command('addadmins', aliases='给管理', only_to_me=False)
async def _(session: CommandSession):
    bot = get_bot()
    someone = session.ctx['message'][1]['data']['qq']
    await bot.set_group_admin(group_id=787941515, user_id=someone, enable=True)
