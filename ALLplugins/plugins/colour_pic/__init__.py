import os, time
import urllib.request

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from nonebot import CommandSession, on_command, on_natural_language, NLPSession, IntentCommand

__plugin_name__ = '[CQ:emoji,id=128013]图求出处，输入‘qb色图’或‘qb色番’'


@on_natural_language(keywords={'色图'})
async def _(session: NLPSession):
    return IntentCommand(100, 'setu')


@on_command('setu', only_to_me=False, aliases=('色图'))
async def setu(session: CommandSession):
    user = session.ctx['user_id']
    pic_name = time.strftime("%Y%m%d%H%M%S", time.localtime())
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("qqbot/") + len("qqbot/")]
    recive_pic = os.path.abspath(rootPath + f'/img/{pic_name}.png')
    save_setu = os.path.abspath(f'/home/coolq-data/data/image/{pic_name}Source.png')
    try:
        cq_pic = session.ctx['message'][1].data['url']
        await tool_man2(session, cq_pic, recive_pic, save_setu, user, pic_name)
    except:
        se_pic = session.get('pic', prompt='请发送[CQ:emoji,id=128013]图')
        await tool_man2(session, se_pic[0], recive_pic, save_setu, user, pic_name)


# 保存图片,搜索图片,发送图片
async def tool_man2(session, se_pic, recive_pic, save_setu, user, pic_name):
    await save_pic(se_pic, recive_pic)
    await session.send('[CQ:emoji,id=128013]图已收到,该过程较长,请耐心等待')
    # await search_anime(recive_pic, save_path)
    c = await search_pic(recive_pic, save_setu)
    if c:
        await session.send('[CQ:emoji,id=128013]图搜索超时,请不要再次重复搜索该[CQ:emoji,id=128013]图')
        return
    await session.send(f'[CQ:at,qq={user}]\n[CQ:image,file={pic_name}Source.png]')


@setu.args_parser
async def _(session: CommandSession):
    cq_pic = session.current_arg_images
    if session.is_first_run:
        if cq_pic:
            session.state['pic'] = cq_pic
        return
    if not cq_pic:
        session.pause('[CQ:emoji,id=128013]图没有收到呢')
    session.state[session.current_key] = cq_pic


# 搜索色图结果并保存
async def search_pic(recive_pic, save_setu):
    opt = webdriver.ChromeOptions()
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(chrome_options=opt)
    browser.get('http://saucenao.com/')
    browser.implicitly_wait(20)
    try:
        img = browser.find_element_by_id('file')
        getsauce = browser.find_element_by_xpath('//input[@value="get sauce"]')
        img.send_keys(recive_pic)
        getsauce.click()
        res = browser.find_element_by_id('middle')
        res.screenshot(save_setu)
    except NoSuchElementException as E:
        return E
    finally:
        browser.quit()


# 保存图片
async def save_pic(cq_pic, recive_pic):
    with urllib.request.urlopen(
            f'{cq_pic}') as rs, open(
        recive_pic, 'wb') as img:
        img.write(rs.read())
        img.flush()
        img.close()


@on_natural_language(keywords={'色番'})
async def _(session: NLPSession):
    return IntentCommand(100, 'sefan')


@on_command('sefan', only_to_me=False, aliases=('色番'))
async def sefan(session: CommandSession):
    # 获取文件地址
    root_pic = 'G:\\火狐下载\\酷Q Pro\\data\\image\\'

    # 保存图片的地址
    save_path = root_pic + 'ColourPicture.png'

    user = session.ctx['user_id']
    pic_name = time.strftime("%Y%m%d%H%M%S", time.localtime())
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("qqbot/") + len("qqbot/")]
    # rootPath = curPath[:curPath.find("qqbot\\") + len("qqbot\\")]
    recive_pic = os.path.abspath(rootPath + f'/img/{pic_name}.gif')
    # recive_pic = os.path.abspath(rootPath + f'\\img\\{pic_name}.png')
    save_setu = os.path.abspath(f'/home/coolq-data/data/image/{pic_name}Source.png')

    try:
        cq_pic = session.ctx['message'][1].data['url']
        await tool_man(session, cq_pic, recive_pic, save_setu, user, pic_name)
    except:
        se_pic = session.get('pic', prompt='请发送[CQ:emoji,id=128013]番')
        await tool_man(session, se_pic[0], recive_pic, save_setu, user, pic_name)


# 保存图片,搜索图片,发送图片
async def tool_man(session, se_pic, recive_pic, save_setu, user, pic_name):
    await save_pic(se_pic, recive_pic)
    await session.send('[CQ:emoji,id=128013]番已收到,该过程较长,请耐心等待(低帧gif会等待3-5分钟')
    # await search_anime(recive_pic, save_path)
    c = await search_anime(recive_pic, save_setu)
    if c:
        await session.send('[CQ:emoji,id=128013]番搜索超时,请不要再次重复搜索该[CQ:emoji,id=128013]番')
        return
    await session.send(f'[CQ:at,qq={user}]\n[CQ:image,file={pic_name}Source.png]')


@sefan.args_parser
async def _(session: CommandSession):
    cq_pic = session.current_arg_images
    if session.is_first_run:
        if cq_pic:
            session.state['pic'] = cq_pic
        return
    if not cq_pic:
        session.pause('[CQ:emoji,id=128013]番没有收到呢')
    session.state[session.current_key] = cq_pic


# 搜索色番结果并保存
async def search_anime(recive_pic, save_setu):
    opt = webdriver.ChromeOptions()
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(chrome_options=opt)
    browser.get('https://trace.moe/')
    browser.implicitly_wait(20)
    try:
        img = browser.find_element_by_id('file')
        searchBtn = browser.find_element_by_xpath('//button[@id="searchBtn"]')
        img.send_keys(recive_pic)
        searchBtn.click()
        time.sleep(10)
        res = browser.find_element_by_id('results')
        res.screenshot(save_setu)
    except NoSuchElementException as E:
        return E
    finally:
        browser.quit()
