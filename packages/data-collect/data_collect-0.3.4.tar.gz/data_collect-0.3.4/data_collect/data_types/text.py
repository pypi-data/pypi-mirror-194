# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
from .blob import Blob


class Text(Blob):
    def __init__(self,
                 correlation_id: str,
                 data: bytes,
                 metadata=None
                 ):
        super().__init__(correlation_id, data, metadata)
