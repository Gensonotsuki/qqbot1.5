import os, time
import urllib.request

from selenium import webdriver
from nonebot import CommandSession, on_command, on_natural_language, NLPResult, NLPSession, IntentCommand

# 获取文件地址
root_pic = 'G:\火狐下载\酷Q Pro\data\image'

# 保存图片的地址
save_path = root_pic + 'ColourPicture.png'


@on_natural_language(keywords={'色图'})
async def _(session: NLPSession):
    return IntentCommand(100, 'setu')


@on_command('setu', only_to_me=False, aliases=('色图'))
async def _(session: CommandSession):
    user = session.ctx['user_id']

    pic_name = time.strftime("%Y%m%d%H%M%S", time.localtime())
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("qqbot/") + len("qqbot/")]
    pic = os.path.abspath(rootPath + f'/img/{pic_name}.png')
    setu = os.path.abspath(f'/home/coolq-data/data/image/{pic_name}Source.png')
    cq_pic = session.ctx['message'][1].data['url']
    with urllib.request.urlopen(
            f'{cq_pic}') as rs, open(
        pic, 'wb') as img:
        img.write(rs.read())
        img.flush()
        img.close()
    await session.send('[CQ:emoji:id=128013]图已收到,该过程较长,请耐心等待')
    await search_pic(pic, setu)
    await session.send(f'[CQ:at,qq={user}]\n[CQ:image,file={pic_name}Source.png]')


# 搜索结果并保存
async def search_pic(pic, setu):
    opt = webdriver.ChromeOptions()
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(chrome_options=opt)
    browser.get('http://saucenao.com/')
    img = browser.find_element_by_id('file')
    getsauce = browser.find_element_by_xpath('//input[@value="get sauce"]')
    img.send_keys(pic)
    getsauce.click()
    res = browser.find_element_by_id('middle')
    res.screenshot(setu)
    browser.quit()
