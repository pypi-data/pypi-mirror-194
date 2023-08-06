# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
import json
import sys
from typing import Dict
from concurrent import futures
import cv2
import picologging
from picologging.handlers import RotatingFileHandler

from .utils import NpEncoder
from .data_types.image import Image as WindmillImage
from .data_types.blob import Blob as WindmillBlob


class Logger:
    def __init__(self, config: Dict = None):
        """
        :param config
        """
        self._logger = None
        self._thread_executor = futures.ThreadPoolExecutor(max_workers=1)

    def log(self, correlation_id: str, **kwargs):
        raise NotImplementedError


class LineLogger(Logger):
    """
    文本日志类
    """

    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.file_path = config.get('file_path')
        self.rotation = config.get('rotation')
        self.retention = config.get('retention')
        self._logger = self._get_pico_logger()

    def _get_pico_logger(self):
        """
        获取pico logger
        """
        handler = RotatingFileHandler(
            self.file_path,
            maxBytes=self._convert_rotation(),
            backupCount=self.retention)
        _logger = picologging.getLogger()
        formatter = picologging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        _logger.addHandler(handler)
        _logger.setLevel(picologging.INFO)
        return _logger

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

    def log(self, correlation_id: str, message=None):
        if isinstance(message, dict):
            message = json.dumps(message, cls=NpEncoder)
        self._logger.info(f"{message}")


class ImageLogger(Logger):
    """
    图片日志类
    """

    def __init__(self, config: Dict = None):
        super().__init__(config)

    def log(self,
            correlation_id: str,
            image: WindmillImage = None,
            designation: str = '',
            metadata: Dict = None):
        # Encode the image as PNG bytes
        if "PIL" in sys.modules and image.is_pillow_image():
            image.covert_to_rgb()
        elif "numpy" in sys.modules and image.is_numpy_array():
            image.covert_cv_image()

        self._thread_executor.submit(cv2.imwrite, designation, image.data)


class BlobLogger(Logger):
    """
    二进制文件类
    """

    def __init__(self, config: Dict = None):
        super().__init__(config)

    def file_write(self, designation, file_bytes):
        with open(designation, "wb") as f:
            f.write(file_bytes)

    def log(self,
            correlation_id: str,
            blob: WindmillBlob = None,
            designation: str = '',
            metadata: Dict = None):
        self._thread_executor.submit((self.file_write, designation, blob.data))
