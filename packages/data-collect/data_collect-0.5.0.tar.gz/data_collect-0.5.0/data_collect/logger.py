# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
import asyncio
import json
import sys
from typing import Dict

import cv2
import picologging
from picologging.handlers import RotatingFileHandler
from .utils import NpEncoder
from .data_types.image import Image as WindmillImage
from .data_types.blob import Blob as WindmillBlob


class Logger:
    def __init__(self, config: Dict = None):
        self._logger = None

    def log(self, correlation_id: str, **kwargs):
        raise NotImplementedError

    def close(self):
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

    def close(self):
        pass


class ImageLogger(Logger):
    """
    图片日志类
    """

    def __init__(self, config: Dict = None):
        super().__init__(config)
        # Create a queue for storing image log data
        self.image_queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self.stop_flag = False
        # Set up the async image logging task
        self.image_task = self.loop.create_task(self._async_image_log())

    async def _async_image_log(self):
        while not self.stop_flag:
            # Wait for an image log to be added to the queue
            data = await self.image_queue.get()
            # Log the image to file and/or S3
            image_bytes, designation, metadata = data
            cv2.imwrite(designation, image_bytes)
            # Mark the queue item as done
            self.image_queue.task_done()

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

        self.image_queue.put_nowait((image.data, designation, metadata))

    def close(self):
        self.stop_flag = True
        self.image_queue.join()
        self.loop.run_until_complete(self.image_task)
        super().close()


class BlobLogger(Logger):
    """
    二进制文件类
    """

    def __init__(self, config: Dict = None):
        super().__init__(config)
        # Create a queue for storing blob log data
        self.blob_queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self.stop_flag = False
        # Set up the async blob logging task
        self.image_task = self.loop.create_task(self._async_blob_log())

    async def _async_blob_log(self):
        while not self.stop_flag:
            # Wait for an image log to be added to the queue
            data = await self.blob_queue.get()
            # Log the bytes to file
            file_bytes, designation, metadata = data
            with open(designation, "wb") as f:
                f.write(file_bytes)
            # Mark the queue item as done
            self.blob_queue.task_done()

    def log(self,
            correlation_id: str,
            blob: WindmillBlob = None,
            designation: str = '',
            metadata: Dict = None):
        self.blob_queue.put_nowait((blob.data, designation, metadata))

    def close(self):
        self.stop_flag = True
        self.blob_queue.join()
        self.loop.run_until_complete(self.image_task)
        super().close()
