#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
環境設定載入器

所有 tools/ 下的 Python 工具都可以用這個來讀取 environments.json，
不用每個工具都寫死連線資訊。

使用方式：
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'config'))
    from env_loader import EnvConfig

    config = EnvConfig()
    dev_db = config.get_db('dev')      # {'host': ..., 'port': ..., ...}
    uat_db = config.get_db('uat')
    all_envs = config.get_env_names()  # ['dev', 'uat', 'prod_vnd', ...]
"""

import os
import json


class EnvConfig:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'environments.json')

        with open(config_path, 'r', encoding='utf-8') as f:
            self._data = json.load(f)

        self._envs = self._data.get('environments', {})

    def get_env_names(self):
        """取得所有環境名稱"""
        return list(self._envs.keys())

    def get_env(self, name):
        """取得完整的環境設定"""
        if name not in self._envs:
            raise ValueError(f"未知的環境: {name}，可用: {', '.join(self._envs.keys())}")
        return self._envs[name]

    def get_db(self, name):
        """取得 DB 連線設定（給 pymysql 用）"""
        env = self.get_env(name)
        db = env.get('db', {})
        return {
            'host': db.get('host', '127.0.0.1'),
            'port': db.get('port', 3306),
            'user': db.get('user', 'root'),
            'password': db.get('password', ''),
            'charset': 'utf8mb4',
        }

    def get_server(self, name):
        """取得 Server 連線設定"""
        env = self.get_env(name)
        return env.get('server', {})

    def get_databases_info(self):
        """取得資料庫用途說明"""
        return self._data.get('databases', {})

    def get_game_codes(self):
        """取得遊戲代碼對照"""
        return self._data.get('game_codes', {})

    def get_log_table_types(self):
        """取得 LogTableType 對照"""
        return self._data.get('log_table_types', {})

    @property
    def raw(self):
        """取得原始 JSON 資料"""
        return self._data
