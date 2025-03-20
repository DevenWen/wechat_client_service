#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request
from bot.conf import config
from wcferry import Wcf, WxMsg

app = Flask(__name__)
wcf = Wcf()

@app.route('/')
def index():
    return 'Hello, wechat bot!'

@app.route('/msg', methods=['POST'])
def msg():
    body = request.get_json()
    if not wcf.is_login():
        return 'not wechat account login', 404
    
    wxid = body['wxid']
    msg = body['msg']
    aters = []
    for at in body['aters']:
        alia = config.get_wxid_by_alias(at)
        if alia is None:
            continue
        aters.append(alia)

    aters_str = ','.join(aters)
    if wcf.send_text(msg, wxid, aters_str) == 0:
        return 'send msg success', 201
    else:
        return 'send msg failed', 400

if __name__ == '__main__':
    app.run(debug=True) 