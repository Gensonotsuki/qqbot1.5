# from nonebot import on_natural_language, NLPResult, NLPSession
# from nonebot import on_command, CommandSession
#
#
# @on_natural_language(only_to_me=False)
# async def _(session: NLPSession):
#     msg_box = session.msg.strip().split()
#     user_id=session.ctx['user_id']
#     print(msg_box,'============')
#     res = NLPResult(100, 'curse_sb', {'message': msg_box})
#     return res
#
# @on_command('curse_sb', only_to_me=False)
# async def _(session: CommandSession):
#     rs = session.args['message']
#     await session.send(rs)
