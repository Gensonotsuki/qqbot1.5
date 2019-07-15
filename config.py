#!/home/qbprjENV/bin/python
import re
from datetime import timedelta
from nonebot.default_config import *

SUPERUSERS = {}
HOST = '0.0.0.0'
PORT = 8080
NICKNAME = ['qb']
COMMAND_START = ['qb', re.compile(r'[\!]+')]
DEBUG = True
SESSION_RUN_TIMEOUT = timedelta(seconds=10)
DEFAULT_VALIDATION_FAILURE_EXPRESSION = '指令格式有误，请检查'

GROUP_LIST = []
