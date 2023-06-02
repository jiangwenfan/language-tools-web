import datetime
import random


def generate_random_num() -> str:
    """返回一个随机数字字符串"""
    timestamp = str(int(datetime.datetime.now().timestamp() * 100000))
    random_num = str(int(random.random() * 10000000))
    return timestamp + random_num