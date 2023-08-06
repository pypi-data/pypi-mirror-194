# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
import typing
import numpy as np
from typing import Union


class Blob:
    def __init__(self,
                 correlation_id: str,
                 data: Union[np.ndarray, bytes, typing.IO],
                 metadata=None) -> None:
        if metadata is None:
            metadata = {}
        self.data = data
        self.correlation_id = correlation_id
        self.metadata = metadata
