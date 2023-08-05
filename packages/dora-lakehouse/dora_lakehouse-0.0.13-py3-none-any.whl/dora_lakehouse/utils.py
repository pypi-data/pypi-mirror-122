# -*- coding: utf-8 -*-
#
# Copyright 2021 Compasso UOL
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
""" Utility methods """
import logging
import os
from pathlib import Path

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, os.environ.get('LOG_LEVEL','DEBUG')))

def sanitize(value):
    """Apply sanitize operations on value
    :param value: Original value
    :return: Sanitized value
    """
    if isinstance(value, str):
        return str(value).lower().strip().replace(' ','_')
    return value

def walk(path:Path, file_type:str):
    """Walk into directory and recovery the file names"""
    for dirpath, dirnames, filenames in os.walk(path):
        for dirname in dirnames:
            filenames.append(walk(os.path.join(dirpath, dirname),file_type))
        for filename in filenames:
            if str(filename).endswith(file_type): # If are an valid file
                yield os.path.join(dirpath, filename)
