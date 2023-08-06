# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
import json
import os
import uuid
import numpy as np
from data_collect.constants import MODEL_NAME


def get_model_name() -> str:
    """
    get model name
    :return: str
    """
    return os.environ.get(MODEL_NAME)


def gen_correlation_id() -> str:
    """
    gen correlation id
    :return: str
    """
    return str(uuid.uuid4().hex)


def format_correlation_id(correlation_id: np.ndarray) -> str:
    """
    format correlation id
    :param correlation_id:
    :return:
    """
    return correlation_id[0][0].decode('utf-8')


class NpEncoder(json.JSONEncoder):
    """
    Numpy array encoder
    """

    def default(self, obj):  # pylint: disable=E0202
        """
        Rewrite json.JSONEncoder have to set default function.
        :param obj:
        :return:
        """
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            # alternatively use str()
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
