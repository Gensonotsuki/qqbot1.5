#!/home/qbprjENV/bin/python
from nonebot import on_notice, NoticeSession

from config import GROUP_LIST


@on_notice('group_increase')
async def _(session: NoticeSession):
    if session.ctx['group_id'] in GROUP_LIST:
        print(session.ctx, '============')
        print(session,'----------------')
        user_id = session.ctx['user_id']
        await session.send(
            f'有新大佬[CQ:at,qq={user_id}]入群[CQ:emoji,id=127881][CQ:emoji,id=127881][CQ:emoji,id=127881]')
