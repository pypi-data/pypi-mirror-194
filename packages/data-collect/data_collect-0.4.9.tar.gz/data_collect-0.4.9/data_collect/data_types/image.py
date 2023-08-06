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
                 data: Union[np.ndarray, PIL.Image.Image],
                 correlation_id: str = '',
                 metadata=None
                 ) -> None:
        super().__init__(data, correlation_id, metadata)

    def _is_pillow_image(self):
        return isinstance(self.data, PIL.Image.Image)

    def _is_numpy_array(self):
        return isinstance(self.data, np.ndarray)
