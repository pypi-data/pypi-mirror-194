# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
import picologging
from loguru import logger as loguru_logger
from picologging.handlers import RotatingFileHandler
from .utils import convert_rotation

LOGURU_LOGGER = 'loguru'

class Logger(object):
    """
    日志类
    """

    def __init__(self, config: dict):
        self.file_path = config.get('file_path')
        self.rotation = config.get('rotation')
        self.retention = config.get('retention')

    def get_logger(self, name: str = ''):
        """
        获取logger
        """
        if name == LOGURU_LOGGER:
            return self._get_loguru_logger()
        return self._get_pico_logger()

    def _get_loguru_logger(self):
        """
        获取loguru logger
        """
        # 取消console log的输出
        loguru_logger.remove(handler_id=None)
        # 异步，避免阻塞 编码格式设置为utf-8
        loguru_logger.add(
            self.file_path,
            rotation=self.rotation,
            retention=self.retention,
            encoding='utf-8',
            enqueue=True,
            level='INFO')
        return loguru_logger.opt(colors=False).opt(raw=True)

    def _get_pico_logger(self):
        """
        获取pico logger
        """
        handler = RotatingFileHandler(
            self.file_path,
            maxBytes=convert_rotation(self.rotation),
            backupCount=self.retention)
        logger = picologging.getLogger()
        formatter = picologging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(picologging.INFO)
        return logger
