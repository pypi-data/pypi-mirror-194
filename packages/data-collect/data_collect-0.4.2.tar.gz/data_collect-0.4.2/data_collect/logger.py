# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
import picologging
from picologging.handlers import RotatingFileHandler
from .utils import convert_rotation


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
        return self._get_pico_logger()

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
