# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
import PIL.Image
import numpy as np
from typing import Union

from .blob import Blob


class Image(Blob):
    def __init__(self,
                 correlation_id: str,
                 data: Union[np.ndarray, PIL.Image.Image],
                 metadata=None
                 ) -> None:
        super().__init__(correlation_id, data, metadata)
