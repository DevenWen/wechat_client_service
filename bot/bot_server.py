#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from wcferry import Wcf, WxMsg
from bot.conf import config
import time
import os
import logging
import queue
from threading import Thread
from typing import Optional
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

_queue = queue.Queue()


class BotServer:
    def __init__(self):
        self.wcf = Wcf(block=False)
        # 创建消息队列
        self.msg_queue = _queue
        # 控制标志
        self.is_running = True
        self.is_login = False
        logger.info("微信机器人服务启动成功")
        Thread(target=self.__run__, daemon=True).start()

    def stop(self):
        self.is_running = False

    def send_msg(self, msg, target_wxid, alters=None):
        """外部调用接口：将消息推送到队列"""
        if not self.is_running:
            raise Exception("机器人服务未启动")

        if not self.is_login:
            self.__block_wait_login__()

        self.msg_queue.put((
            self.__handle_send_msg__,
            {
                "msg": msg,
                "target_wxid": target_wxid,
                "alters": alters
            })
        )

    def __block_wait_login__(self, timeout=10):
        """阻塞等待微信登录"""
        start_time = time.time()
        while not self.is_login:
            if time.time() - start_time > timeout:
                raise Exception("等待微信登录超时")
            time.sleep(1)

    def __handle_send_msg__(self, msg, target_wxid, alters=None):
        """处理发送消息"""
        self.wcf.send_text(msg, target_wxid, alters)

    def __run__(self):
        """运行机器人主循环"""
        while True:
            try:
                if self.wcf.is_login():
                    self.is_login = True
                    logger.info("微信已登录")
                    break
            except Exception as e:
                logger.error(f"微信未登录: {e}")
                time.sleep(1)

        # 获取联系人列表并保存到文件
        try:
            logger.info("正在获取联系人列表...")
            contacts = self.wcf.get_contacts()
            
            # 确保 logs 目录存在
            if not os.path.exists("logs"):
                os.makedirs("logs")
                
            # 将联系人列表保存到文件
            contacts_file = os.path.join("logs", "current_contract.json")
            with open(contacts_file, "w", encoding="utf-8") as f:
                json.dump(contacts, f, ensure_ascii=False, indent=2)
                
            logger.info(f"联系人列表已保存到 {contacts_file}")
        except Exception as e:
            logger.error(f"获取联系人列表失败: {e}")

        while True:
            logger.info("开始监听消息...")
            try:
                # 主循环处理 __queue__ 里的信息
                while self.is_running:
                    try:
                        (func, args) = self.msg_queue.get(timeout=1)
                        func(**args)
                    except queue.Empty:
                        continue
                    time.sleep(0.5)

            except KeyboardInterrupt:
                logger.info("机器人服务正在停止...")
            except Exception as e:
                logger.error(f"运行时发生错误: {e}")
            finally:
                self.is_running = False
                self.wcf.cleanup()

# 创建一个全局的 BotServer 实例
_bot_instance = None

def get_bot_instance() -> BotServer:
    """获取全局 BotServer 实例"""
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = BotServer()
    return _bot_instance

def stop_bot_instance():
    """停止全局 BotServer 实例"""
    if _bot_instance is not None:
        _bot_instance.stop()
        _bot_instance = None