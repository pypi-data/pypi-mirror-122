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
""" Software Development Kit """
__version__ = '0.0.14'

from os import environ
from dora_lakehouse import __version__ as dora_version
from dora_lakehouse.utils import logger

logger.info("DORA:VERSION:%s", __version__)

environ['MAX_SIZE']  = environ.get('MAX_SIZE','128') #Max file size in MB
environ['MAX_ROWS']  = environ.get('MAX_ROWS','10000000') # Default max rows per file 10 millions
environ['MIN_ROWS']  = environ.get('MIN_ROWS','10000') # Default min rows per file 10 thousand

# Shared File System
if environ.get("SHAREDFS") is None:
    logger.warning("Environ variable 'SHAREDFS' not found!")
    environ["SHAREDFS"]= "/tmp/efs/"
logger.debug("SHAREDFS:%s",environ["SHAREDFS"])
environ["METADIR"] = f"{environ['SHAREDFS']}/meta/"

# Stage Bucket
if environ.get("BKT_STG") is None:
    logger.warning("Environ variable 'BKT_STG' not found!")
    environ["BKT_STG"] = "/tmp/bkt/stg"
logger.debug("BKT_STG:%s",environ["BKT_STG"])

# Error Bucket
if environ.get("BKT_ERR") is None:
    logger.warning("Environ variable 'BKT_ERR' not found!")
    environ["BKT_ERR"] = "/tmp/bkt/err"
logger.debug("BKT_ERR:%s",environ["BKT_ERR"])

# Master data bucket
if environ.get("BKT_ODS") is None:
    logger.warning("Environ variable 'BKT_ODS' not found!")
    environ["BKT_ODS"] = "/tmp/bkt/ods"
logger.debug("BKT_ODS:%s",environ["BKT_ODS"])

# Refined data bucket
if environ.get("BKT_RFN") is None:
    logger.warning("Environ variable 'BKT_RFN' not found!")
    environ["BKT_RFN"] = "/tmp/bkt/ref"
logger.debug("BKT_RFN:%s",environ["BKT_RFN"])
