import os,json

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("qqbot\\") + len("qqbot\\")]
chat_decode = os.path.abspath(rootPath + '\\chat_decode.json')

print(json.load(chat_decode))