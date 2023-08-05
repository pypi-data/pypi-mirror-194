# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
import json
import os
import uuid
import numpy as np

from .constants import WORKSPACE_ID, MODEL_STORE_NAME, MODEL_NAME, MODEL_VERSION


def get_model_name(
        workspace_id: str = None,
        model_store_name: str = None,
        model_name: str = None,
        version: int = None
) -> str:
    """
    get model name from param or env
    :return:
    """
    workspace_id = os.environ.get(WORKSPACE_ID) if workspace_id is None else workspace_id
    model_store_name = os.environ.get(MODEL_STORE_NAME) if model_store_name is None else model_store_name
    model_name = os.environ.get(MODEL_NAME) if model_name is None else model_name
    version = os.environ.get(MODEL_VERSION) if version is None else version
    return f"/workspaces/{workspace_id}/modelstores/{model_store_name}/" \
           f"models/{model_name}/versions/{version}"


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
        default function for type transform
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
