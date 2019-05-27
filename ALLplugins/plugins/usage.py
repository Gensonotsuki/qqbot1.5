#!/home/qbprjENV/bin/python
import nonebot
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession,IntentCommand



@on_natural_language(keywords={'帮助'})
async def _(session:NLPSession):
    return IntentCommand(60,'usage')



@on_command('usage', aliases=['帮助'],only_to_me=False)
async def _(session: CommandSession):
    plugins = list(filter(lambda p: p.name, nonebot.get_loaded_plugins()))
    print(plugins)
    arg = session.current_arg_text.strip().lower()
    if not arg:
        await session.send('现在有以下功能：\n' + '\n'.join(p.name for p in plugins))
        return

    for p in plugins:
        if p.name.lower() == arg:
            await session.send(p.usage)
