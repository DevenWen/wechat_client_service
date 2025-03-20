#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import yaml
from typing import Any


class Config:
    def __init__(self, config_file: str = "config.yml"):
        self._config = {}
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}
        except FileNotFoundError as e:
            print(f"配置文件 {config_file} 不存在")
        except yaml.YAMLError as e:
            print(f"配置文件解析错误: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """支持 a.b.c 格式的配置读取"""
        keys = key.split('.')
        value = self._config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_wxid_by_alias(self, name: str) -> str:
        """获取微信别名"""
        contacts = self.get(f"wechat.contacts")
        if contacts is None:
            return None
        map = {}
        for item in contacts:
            wxid = item['wxid']
            for n in item['alias']:
                map[n] = wxid
        return map.get(name, None)

# 创建全局配置对象
config = Config()
