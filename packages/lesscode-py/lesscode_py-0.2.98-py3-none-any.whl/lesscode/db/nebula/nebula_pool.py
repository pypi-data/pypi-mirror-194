# -*- coding: utf-8 -*-
# author:chao.yy
# email:yuyc@ishangqi.com
# date:2022/2/17 2:45 下午
# Copyright (C) 2022 The lesscode Team
from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config

from lesscode.db.base_connection_pool import BaseConnectionPool


class NebulaPool(BaseConnectionPool):
    """
    mysql 数据库链接创建类
    """

    async def create_pool(self):
        pass

    def sync_create_pool(self):
        config = Config()
        config.max_connection_pool_size = self.conn_info.max_size
        config.min_connection_pool_size = self.conn_info.min_size
        config.timeout = self.conn_info.params.get("timeout", 0) if self.conn_info.params and isinstance(
            self.conn_info.params, dict) else 0
        config.idle_time = self.conn_info.params.get("idle_time", 0) if self.conn_info.params and isinstance(
            self.conn_info.params, dict) else 0
        config.interval_check = self.conn_info.params.get("interval_check", -1) if self.conn_info.params and isinstance(
            self.conn_info.params, dict) else 0
        pool = ConnectionPool()
        pool.init([(self.conn_info.host, self.conn_info.port)], config)
        return pool
