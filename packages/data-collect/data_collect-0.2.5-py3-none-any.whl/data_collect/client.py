# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
DataCollectClient Library
"""
import asyncio
import datetime
import json
import os
import sys
import time
from threading import Thread

import cv2
import numpy as np
import PIL.Image
from loguru import logger as loguru_logger
from typing import Union, Sequence, Dict, List, Any, Mapping
from concurrent.futures import Executor, ThreadPoolExecutor

from pydantic import BaseModel
from .constants import (
    DEFAULT_CAPTURE_LOG_DIR, DEFAULT_CAPTURE_BLOB_DIR,
    CAPTURE_LOG_DIR, CAPTURE_BLOB_DIR,
    ENABLE_CAPTURE_INPUT, ENABLE_CAPTURE_PREDICTION, ENABLE_CAPTURE_GROUND_TRUTH, DEFAULT_CAPTURE_INPUT_DESIGNATION,
    TIME_DIRECTORY_FORMAT, DEFAULT_CAPTURE_PREDICTION_DESIGNATION,
)
from .utils import get_model_name, NpEncoder
from .data_types.blob import Blob as WindmillBlob
from .data_types.image import Image as WindmillImage
from .data_types.text import Text as WindmillText


def asyncF(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper

def _is_pillow_image(img):
    return isinstance(img, PIL.Image.Image)


def _is_numpy_array(img):
    return isinstance(img, np.ndarray)


def _is_windmill_image(img):
    return isinstance(img, WindmillImage)


class ModelCollectConfig(BaseModel):
    """Config model"""
    model_name: str = ''
    log_path: str = DEFAULT_CAPTURE_LOG_DIR
    blob_path: str = DEFAULT_CAPTURE_BLOB_DIR
    input_enable: bool = True
    prediction_enable: bool = True
    ground_truth_enable: bool = True


class DataCollectClient:
    """
    DataCollectClient
    """

    def __init__(self, config):
        """
        init logger
        :path log_dir_path:
        """
        self._job_pool: Executor = ThreadPoolExecutor(max_workers=10)
        self._load_env_setting_and_config(config)
        self._init_base_logger()

    def _init_base_logger(self):
        """
        init base logger
        :return:
        """
        # 取消console log的输出
        loguru_logger.remove(handler_id=None)
        log_file_path = f"{self.log_path}/{DEFAULT_CAPTURE_PREDICTION_DESIGNATION}/result.jsonl"
        # 异步，避免阻塞 编码格式设置为utf-8
        loguru_logger.add(
            log_file_path,
            rotation="100 MB",
            retention=10,
            encoding='utf-8',
            enqueue=True,
            level='INFO')
        self._logger = loguru_logger.opt(colors=False).opt(raw=True)

    def _is_data_capture_enable(self):
        """
        check is need print log
        :return:
        """
        return self.input_enable or \
            self.prediction_enable or \
            self.ground_truth_enable

    def _gen_image_save_path(self, correlation_id: str, designation: str = '') -> str:
        """
        generate image tmp save dir as yyyy-MM-dd/hh
        :return:
        """
        # generate time directory
        if len(designation) == 0:
            designation = DEFAULT_CAPTURE_INPUT_DESIGNATION
        time_tuple = time.localtime(int(time.time()))
        dir_name = os.path.join(f"{self.blob_path}/{designation}",
                                time.strftime(TIME_DIRECTORY_FORMAT, time_tuple))
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        file_name = f"{dir_name}/{correlation_id}.png"
        return file_name

    def _gen_default_message(self, correlation_id: str) -> {}:
        """
        generate default message
        :param correlation_id:
        :return:
        """
        message = {
            'correlation_id': correlation_id,
            'model_name': self.model_name,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        return message

    def log(self,
            correlation_id: str,
            log: Dict[str, Any] = None,
            text: Sequence = None,
            time_series: Sequence = None,
            image: Union[PIL.Image.Image, np.ndarray, WindmillImage] = None,
            blob: Union[WindmillImage, WindmillText, WindmillBlob] = None,
            prediction: Union[Dict, List, str] = None,
            ground_truth: Union[Dict, List] = None,
            designation: str = '',
            config: ModelCollectConfig = None,
            ):
        """
        data capture main log function
        :param correlation_id:
        :param log:
        :param designation:
        :param blob:
        :param image:
        :param text:
        :param time_series:
        :param prediction:
        :param ground_truth:
        :param config:
        :return:
        """
        if config is not None:
            self._load_env_setting_and_config(config)
            self._init_base_logger()

        message = {}

        if log is not None:
            message = self._gen_default_message(correlation_id)
            if not isinstance(log, Mapping):
                raise ValueError("data must be passed a dictionary")

            if any(not isinstance(key, str) for key in log.keys()):
                raise ValueError("Key values passed to data must be strings.")

            for k, v in log.items():
                if isinstance(v, (list, dict)):
                    message[k] = json.dumps(v, cls=NpEncoder)
                if isinstance(v, (int, float, str)):
                    message[k] = v

        if prediction is not None and self.prediction_enable:
            message = self._gen_default_message(correlation_id)
            message['prediction'] = prediction if isinstance(prediction, str) else json.dumps(prediction,
                                                                                              cls=NpEncoder)
        if ground_truth is not None and self.ground_truth_enable:
            message = self._gen_default_message(correlation_id)
            message['ground_truth'] = ground_truth if isinstance(ground_truth, str) else json.dumps(ground_truth,
                                                                                                    cls=NpEncoder)
        if image is not None and self.input_enable:
            self._log_image(correlation_id, image, designation)

        if blob is not None and self._is_data_capture_enable():
            self._log_blob(correlation_id, blob)

        if self._is_data_capture_enable() and len(message) > 0:
            self._record(message)

    def _record(self, message: Dict):
        """
        record log
        :param message:
        :return:
        """
        json_encode_message = json.dumps(message, cls=NpEncoder)
        self._logger.info(f"{json_encode_message}\n")

    def _load_env_setting_and_config(self, config: ModelCollectConfig):
        """
        load env setting and config
        :param config:
        :return:
        """
        self.model_name = config.model_name if config.model_name is not None else get_model_name()

        self.log_path = config.log_path.rstrip("/")
        if os.environ.get(CAPTURE_LOG_DIR) is not None and len(os.environ.get(CAPTURE_LOG_DIR)) > 0:
            self.log_path = os.environ.get(CAPTURE_LOG_DIR).rstrip("/")

        self.blob_path = config.blob_path.rstrip("/")
        if os.environ.get(CAPTURE_BLOB_DIR) is not None and len(os.environ.get(CAPTURE_BLOB_DIR)) > 0:
            self.blob_path = os.environ.get(CAPTURE_BLOB_DIR).rstrip("/")

        # env优先级高于config
        self.input_enable = config.input_enable
        if os.environ.get(ENABLE_CAPTURE_INPUT) is not None:
            self.input_enable = os.environ.get(ENABLE_CAPTURE_INPUT) == "True"

        self.prediction_enable = config.prediction_enable
        if os.environ.get(ENABLE_CAPTURE_PREDICTION) is not None:
            self.prediction_enable = os.environ.get(ENABLE_CAPTURE_PREDICTION) == "True"

        self.ground_truth_enable = config.ground_truth_enable
        if os.environ.get(ENABLE_CAPTURE_GROUND_TRUTH) is not None:
            self.ground_truth_enable = os.environ.get(ENABLE_CAPTURE_GROUND_TRUTH) == "True"

    def _log_image(self,
                   correlation_id: str,
                   image: Union[WindmillImage, np.ndarray, PIL.Image.Image],
                   designation: str = '',
                   metadata: Dict = None):

        def _normalize_to_uint8(x):
            # Based on: https://github.com/matplotlib/matplotlib/blob/06567e021f21be046b6d6dcf00380c1cb9adaf3c/lib/matplotlib/image.py#L684

            is_int = np.issubdtype(x.dtype, np.integer)
            low = 0
            high = 255 if is_int else 1
            if x.min() < low or x.max() > high:
                msg = (
                    "Out-of-range values are detected. "
                    "Clipping array (dtype: '{}') to [{}, {}]".format(x.dtype, low, high)
                )
                self._logger.warning(msg)
                x = np.clip(x, low, high)

            # float or bool
            if not is_int:
                x = x * 255

            return x.astype(np.uint8)

        tmp_path = self._gen_image_save_path(correlation_id, designation)
        if "PIL" in sys.modules and _is_pillow_image(image):
            image.save(tmp_path, format="PNG")
        elif "numpy" in sys.modules and _is_numpy_array(image):
            import numpy as np

            try:
                from PIL import Image
            except ImportError as exc:
                from PIL import Image
                raise ImportError(
                    "`log_image` requires Pillow to serialize a numpy array as an image."
                    "Please install it via: pip install Pillow"
                ) from exc

            # Ref.: https://numpy.org/doc/stable/reference/generated/numpy.dtype.kind.html#numpy-dtype-kind
            valid_data_types = {
                "b": "bool",
                "i": "signed integer",
                "u": "unsigned integer",
                "f": "floating",
            }

            if image.dtype.kind not in valid_data_types:
                raise TypeError(
                    f"Invalid array data type: '{image.dtype}'. "
                    f"Must be one of {list(valid_data_types.values())}"
                )

            if image.ndim not in [2, 3, 4]:
                raise ValueError(
                    "`image` must be a 2D or 3D or 4D array but got a {}D array".format(image.ndim)
                )

            if (image.ndim == 3) and (image.shape[2] not in [1, 3, 4]):
                raise ValueError(
                    "Invalid channel length: {}. Must be one of [1, 3, 4]".format(
                        image.shape[2]
                    )
                )

            # squeeze a 3D grayscale image since `Image.fromarray` doesn't accept it.
            if image.ndim == 3 and image.shape[2] == 1:
                image = image[:, :, 0]

            if image.ndim == 4:
                image = image.squeeze()
            else:
                image = _normalize_to_uint8(image)

            image = image[..., ::-1]  # BGR to RGB
            job_future = self._job_pool.submit(
                self.save_image,
                image,
                tmp_path,
            )

            job_future.add_done_callback(_log_async_job_exception)


        elif _is_windmill_image(image):
            if correlation_id is None:
                correlation_id = image.correlation_id
            self._log_image(correlation_id, image.data, designation, image.metadata)
        else:
            raise TypeError("Unsupported image object type: '{}'".format(type(image)))

    def _log_blob(self, correlation_id: str, blob: WindmillBlob):
        tmp_path = self._gen_blob_save_path(correlation_id, blob.metadata['extension'])
        with open(tmp_path, "wb", encoding="utf-8") as f:
            f.write(blob.data)



    def _gen_blob_save_path(self, correlation_id: str, extension: str):
        """
        generate blob save path
        :param correlation_id:
        :return:
        """
        time_tuple = time.localtime(int(time.time()))
        dir_name = os.path.join(f"{self.blob_path}/{DEFAULT_CAPTURE_INPUT_DESIGNATION}",
                                time.strftime(TIME_DIRECTORY_FORMAT, time_tuple))
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        return f"{dir_name}/{correlation_id}.{extension}"

    def save_image(self, image, tmp_path):
        cv2.imwrite(tmp_path, image)



def _log_async_job_exception(future):
    exception = future.exception()
    if exception is not None:
        print(f"Exception occurred during async logging job: {repr(exception)}")