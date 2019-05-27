#!/home/qbprjENV/bin/python

from os import path
import nonebot as nb
import config

if __name__ == '__main__':
    # 加载配置文件
    nb.init(config)
    # 加载插件
    nb.load_plugins(
        path.join(path.dirname(__file__), 'ALLplugins', 'plugins'),
        'ALLplugins.plugins'
    )
    nb.run()
