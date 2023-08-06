#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    llmapi-cli
    
    LLMApi is OpenAPI for Large Language Models

    :date:      02/22/2023
    :author:    llmapi <llmapi@163.com>
    :homepage:  https://github.com/llmapi/
    :license:   MIT, see LICENSE for more details.
    :copyright: Copyright (c) 2023 llmapi. All rights reserved
"""
from __future__ import unicode_literals
from threading import Thread
import sys
import json
import re
import os
import argparse as ap
import getpass

__name__ = 'llmapi'
__version__ = '1.0.5'
__description__ = 'Do you want to talk directly to the LLMs? Try llmapi.'
__keywords__ = 'LLM OpenAPI LargeLanguageModel'
__author__ = 'llmapi'
__contact__ = 'llmapi@163.com'
__url__ = 'https://github.com/llmapi/'
__license__ = 'MIT'

import requests
import time
import json

lock = [True,'等待中']
def _loading():
    """
    等待函数
    """
    chars = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
    i = 0
    global lock
    cost_time = 0
    while lock[0]:
        i = (i+1) % len(chars)
        em = '✓' if lock[1] != "等待中" else chars[i]
        print('\033[A%s %s [%d s]' %
              (em, lock[1] or '' if len(lock) >= 2 else '', cost_time))
        time.sleep(0.25)
        cost_time += 0.25

def _is_json(jstr:str)->bool:
    try:
        jsobj = json.loads(jstr)
    except ValueError:
        return False
    return True

def _make_post(url,content):
    try:
        res = requests.post(url, data = json.dumps(content))
        rep = res.json()
        return rep
    except Exception:
        return {'code':-1,'msg':'request failed'}

def _get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

class LLMApi():
    def __init__(self, host='https://api.llmapi.online', bot_type:str = 'mock'):
        self.host = host
        self.token = ''
        self.session = ''
        self.chat_stub = ''
        self.bot_type = bot_type

    def _start_session(self)->dict:
        url = self.host + '/v1/chat/start'
        timestamp = _get_time()
        content = {'token':self.token, 'bot_type':self.bot_type, 'timestamp':timestamp}
        return _make_post(url,content)
 
    def _end_session(self)->dict:
        url = self.host + '/v1/chat/end'
        timestamp = _get_time()
        content = {'token':self.token, 'session':self.session, 'timestamp':timestamp}
        return _make_post(url,content)

    def _save_session(self):
        path = os.environ.get('HOME') + '/.llmapi'
        if not os.path.exists(path):
            os.mkdir(path)
        with open(path + '/session','w+') as f:
            info = {'host':self.host,'token':self.token,'session':self.session,'bot_type':self.bot_type}
            f.write(json.dumps(info))
            f.flush()
            f.close()
        
    def _load_session(self)->bool:
        path = os.environ.get('HOME') + '/.llmapi'
        if not os.path.exists(path):
            return False
        if not os.path.exists(path + '/session'):
            return False
        with open(path + '/session','r') as f:
            try:
                info = json.loads(f.read())
                self.host = info['host']
                self.token = info['token']
                self.session = info['session']
                self.bot_type = info['bot_type']
            except Exception:
                return False
        return True

    def login(self, email:str, password:str):
        url = self.host + '/v1/login'
        content = {'email':email, 'password':password}
        rep = _make_post(url,content)
        if rep['code'] == 0:
            self.token = rep['token']
            rep = self._start_session()
            if rep['code'] == 0:
                self.session = rep['session']
                self._save_session()

        return rep['msg']
 
    def logout(self):
        self._end_session()
        url = self.host + '/v1/logout'
        content = {'token':self.token}
        rep = _make_post(url,content)
        return rep['msg']

    def chat_send(self, prompt:str)->bool:
        url = self.host + '/v1/chat/send'
        timestamp = _get_time()
        content = {'token':self.token, 'session':self.session, 'timestamp':timestamp, 'content':prompt}
        rep = _make_post(url,content)
        if rep['code'] == 0:
            self.chat_stub = rep['stub']
        return rep['msg']
 
    def chat_recv(self):
        url = self.host + '/v1/chat/recv'
        timestamp = _get_time()
        content = {'token':self.token, 'session':self.session, 'timestamp':timestamp, 'stub':self.chat_stub}
        rep = _make_post(url,content)
        if rep['code'] == 0:
            if _is_json(rep['reply']):
                return json.loads(rep['reply'])
            else:
                return rep['reply']
        return rep['msg']
                       
    def chat_sync(self, prompt:str):
        url = self.host + '/v1/chat/sync'
        timestamp = _get_time()
        content = {'token':self.token, 'session':self.session, 'timestamp':timestamp, 'content':prompt}
        rep = _make_post(url,content)
        if rep['code'] == 0:
            if _is_json(rep['reply']):
                return json.loads(rep['reply'])
            else:
                return rep['reply']
        return rep['msg']

    def __str__(self):
        print(f"| [host]:{self.host}")
        print(f"| [token]:{self.token}")
        print(f"| [session]:{self.session}")
        print(f"| [stub]:{self.chat_stub}")
        print(f"| [bot_type]:{self.bot_type}")
        return ""
   
                                       
def _parse_arg():
    parse = ap.ArgumentParser(description="OpenApi for Large Language Models.")
    parse.add_argument('--host', type=str, default = 'https://api.llmapi.online', help='LLMApi server host.')
    parse.add_argument('--bot', type=str, default = 'mock', help='Choose which type of LLM bot you want to talk with.')
    parse.add_argument('--relogin', action='store_true',help='Force re-login account.')
    arg = parse.parse_args()
    return arg

def main():
    arg = _parse_arg()

    client = LLMApi(arg.host, arg.bot)
    if arg.relogin or not client._load_session():
        print( "-------------------------------------------------------")
        print( " You need to create an account on LLMApi first.")
        print( " [ https://llmapi.online/register ]")
        print( "-------------------------------------------------------")
        print(" [Input your account email:]")
        email = input()
        pd = getpass.getpass(" [Input your account password:]")
        ret = client.login(email,pd)
        if ret == False:
            exit()

    print( "\n =================================================")
    print(f" * LLMApi version {__version__}")
    print(f" * Visit 'https://llmapi.online' for more info.")
    print( " -------------------------------------------------")
    print(f" * Start talking with '{client.bot_type}'.")
    print( " * Press 'Ctrl+c' to quit.")
    print( " * Input your word and press 'Enter' key to send.")
    print( " =================================================\n\n")
    try:
        global lock
        count = 0
        while True:
            count += 1
            print(f"\033[1;32;44m ---- [{_get_time()}] [count:{count}] Input: \033[0m\n")
            while True:
                try:
                    prompt = input()
                    if prompt != "":
                        break
                except Exception:
                    print("[ERR] 输入中包含不能识别的字符，请重新输入:")

            print("")
            print("")

            lock = [True, '等待中']
            try:
                t = Thread(target=_loading)
                t.start()
            except Exception as e:
                print(e)
            try:
                rep = client.chat_sync(prompt=prompt)
            except Exception as e:
                lock[0] = False
                print("发生错误,请重试")
                continue

            lock[1] = f'[{client.bot_type}] 已回复 {_get_time()}'
            time.sleep(0.5)
            lock[0] = False

            print("-----------------< 回复开始 >-----------------")
            for i in rep:
                time.sleep(0.01)
                sys.stdout.write(i)
                sys.stdout.flush()
            print("")
            print("-----------------< 回复结束 >-----------------")
            print("")
    except KeyboardInterrupt:
        print('\n == [Bye~] ==')
        exit()

if __name__ == '__main__':
    main()
