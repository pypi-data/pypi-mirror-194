# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
import json
import picologging
from typing import Union
from picologging.handlers import RotatingFileHandler
from .utils import NpEncoder


class Logger(object):
    """
    日志类
    """

    def __init__(self, config: dict):
        self._logger = None
        self.config = config
        self.file_path = config.get('file_path')
        self.rotation = config.get('rotation')
        self.retention = config.get('retention')

    def get_logger(self):
        """
        获取logger
        """
        self._get_pico_logger()
        return self._logger

    def _get_pico_logger(self):
        """
        获取pico logger
        """
        return PicoLogger(self.config)

    def info(self, message: Union[str, dict]):
        """
        log record
        """
        if isinstance(message, dict):
            message = json.dumps(message, cls=NpEncoder)
        return self._logger.info(f"{message}")

    def _convert_rotation(self) -> int:
        """
        convert rotation
        :return:
        """
        if self.rotation.endswith('KB'):
            return int(self.rotation[:-2]) * 1024
        if self.rotation.endswith('MB'):
            return int(self.rotation[:-2]) * 1024 * 1024
        if self.rotation.endswith('GB'):
            return int(self.rotation[:-2]) * 1024 * 1024 * 1024
        return int(self.rotation)


class PicoLogger(Logger):
    """
    pico logger
    """

    def __init__(self, config: dict):
        super().__init__(config)
        handler = RotatingFileHandler(
            self.file_path,
            maxBytes=self._convert_rotation(),
            backupCount=self.retention)
        self._logger = picologging.getLogger()
        formatter = picologging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(picologging.INFO)
