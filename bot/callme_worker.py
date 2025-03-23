#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import argparse
import uuid
import sys
import os
from flask import Flask
from dotenv import load_dotenv
load_dotenv()
from bot.conf import config
from bot.bot_server import get_bot_instance

# 导入所需的模块
from callme import register_handler, worker_sdk, HttpJob

wcbot = get_bot_instance()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("counter_worker")

@register_handler("/api/wechat/msg", method="POST")
def api_wechat_msg(job: HttpJob):
    body = job.body
    logger.info(f"收到消息: {body}")
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
    return {"code": 0, "msg": "success"}

def main(version=None):
    """工作节点主函数入口点"""
    # 如果没有指定版本，使用随机版本
    worker_version = version or f"worker-{uuid.uuid4().hex[:8]}"
    logger.info(f"启动工作节点，版本: {worker_version}")
    worker_sdk.on_call(version=worker_version)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="微信机器人 worker")
    parser.add_argument("--version", help="节点版本", default=None)
    args = parser.parse_args()
    
    main(version=args.version)