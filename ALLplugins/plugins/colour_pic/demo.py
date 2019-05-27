import os
import urllib.request

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("qqbot\\") + len("qqbot\\")]

pic = os.path.abspath(rootPath + '/img/345.png')

with urllib.request.urlopen('https://gchat.qpic.cn/gchatpic_new/1105569635/2087126250-2873294443-7A8A405C505566733624CD34BEC83BED/0?vuin=2121587358&amp;term=2') as rs,open(pic,'wb') as img:
    img.write(rs.read())
    img.flush()
    img.close()
