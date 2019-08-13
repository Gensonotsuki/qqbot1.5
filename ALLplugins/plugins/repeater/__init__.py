#!/home/qbprjENV/bin/python
from random import randint
from nonebot import on_natural_language, NLPSession, NLPResult
from nonebot import on_command, CommandSession

from config import GROUP_LIST
from .data_source import send_repeate

__plugin_name__ = '复读机模式'
_last_session = None
_repeate_wd = ''
repeat_box = []
repeat_time = randint(1, 2)




# 自然语言处理器
@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    if session.ctx.get('group_id') not in GROUP_LIST:
        return None
    global _last_session, _repeate_wd, repeat_box, repeat_time
    result = None
    if _last_session and \
            _last_session.ctx['user_id'] != session.ctx['user_id'] and \
            _last_session.msg == session.msg and \
            _last_session.msg != _repeate_wd and \
            len(repeat_box) == repeat_time:
        result = NLPResult(100.0, 'repeat', {'message': _last_session.msg})
        _repeate_wd = _last_session.msg
        repeat_box = []
        repeat_time = randint(1, 2)
    elif _last_session and \
            _last_session.ctx['user_id'] != session.ctx['user_id'] and \
            _last_session.msg == session.msg and \
            _last_session.msg != _repeate_wd:
        repeat_box.append(_last_session.msg)
    else:
        repeat_box = []
        _last_session = session
        repeat_time = randint(1, 2)
        repeat_box.append(_last_session.msg)
    return result


@on_command('repeat', only_to_me=False)
async def _(session: CommandSession):
    wd = session.args['message']
    await session.send(wd)
