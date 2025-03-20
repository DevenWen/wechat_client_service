#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request
from bot.conf import config
from bot.bot_server import get_bot_instance

app = Flask(__name__)
wcbot = get_bot_instance()

@app.route('/')
def index():
    return 'Hello, wechat bot!'

@app.route('/msg', methods=['POST'])
def msg():
    body = request.get_json()
    
    wxid = body['wxid']
    msg = body['msg']
    aters = []
    for at in body['aters']:
        alia = config.get_wxid_by_alias(at)
        if alia is None:
            continue
        aters.append(alia)

    aters_str = ','.join(aters)
    wcbot.send_msg(msg, wxid, aters_str)
    return 'send msg success', 201

if __name__ == '__main__':
    app.run(debug=True) 