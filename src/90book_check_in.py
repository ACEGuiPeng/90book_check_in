#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
# @Time: 18-6-19 下午6:50
# @Author: guipeng
# @Version: V1.0
# @File: 90book_check_in.py
# @Contact: aceguipeng@foxmail.com 
# @desc: 90book网自动签到
'''
import logging
import time

import requests
import schedule

"""
# 1 登录
# 2 签到
"""
LOGIN_URL = 'http://book.90xz.com/us/login'
POST_LOGIN_URL = 'http://book.90xz.com/u/login'
# https://book.90xz.com/u/punchin?time=1529406905069
CHECK_URL = 'http://book.90xz.com/u/punchin'
USERNAME = 'test'
PWD = 'test'
REFERER = 'Referer'
LOGIN_REFERER = 'https://book.90xz.com/us/login'
CHECK_REFERER = 'https://book.90xz.com/us/index'
HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,de;q=0.6',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'book.90xz.com',
    'Origin': 'https://book.90xz.com',
    'Pragma': 'no-cache',
    # 'Referer': 'https://book.90xz.com/us/login',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/66.0.3359.181 Chrome/66.0.3359.181 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def _init_logger():
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("90_book.log")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.addHandler(console)


_init_logger()


def _get_login_cookie():
    resp = requests.get(LOGIN_URL, timeout=12)
    return resp.cookies


def _post_login_data(cookies):
    form_data = {
        'txtUserName': USERNAME,
        'txtPassword': PWD,
        'chkRemember': 'checked'
    }
    HEADERS[REFERER] = LOGIN_REFERER
    resp = requests.post(POST_LOGIN_URL, data=form_data, cookies=cookies, headers=HEADERS)
    return resp.cookies


def _go_check_in(login_cookie):
    HEADERS[REFERER] = CHECK_REFERER
    params = {
        'time': str(round(time.time() * 1000))
    }
    resp = requests.get(CHECK_URL, cookies=login_cookie, headers=HEADERS, params=params)
    logger.info('status_code: {},resp_info: {}'.format(resp.status_code, resp.json()))


def check_in_job():
    # 防止误差
    try:
        cookies = _get_login_cookie()
        login_cookie = _post_login_data(cookies)
        _go_check_in(login_cookie)
    except Exception as e:
        logger.exception(str(e))


schedule.every().day.at("08:00").do(check_in_job)


def check_in():
    while True:
        logger.debug('check in 90book app is starting')
        schedule.run_pending()
        time.sleep(0.1)


if __name__ == '__main__':
    check_in()
