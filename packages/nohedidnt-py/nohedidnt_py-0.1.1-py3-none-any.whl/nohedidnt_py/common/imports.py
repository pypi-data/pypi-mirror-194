# -*- coding: utf-8 -*-
from __future__ import annotations


import difflib
import json
import locale
import logging
import math
import os
import re
import sys
import typing
import urllib.parse
import uuid

from argparse import ArgumentParser as ArgParser, SUPPRESS
from collections import Counter
from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta
from enum import Enum, IntEnum
from logging import Logger, NullHandler, StreamHandler
from logging.handlers import RotatingFileHandler
from pathlib import Path
from re import Pattern
from typing import Any, AnyStr, Callable, ClassVar, Dict, ForwardRef, Generic, IO, Iterable, Iterator, List, Mapping, MutableMapping, NoReturn, Optional, \
    Sequence, Set, Tuple, Type, TypeVar, Union


import catalogue
import chardet
import pycountry
import pycountry_convert
import pytz
import pytz_deprecation_shim as pds
import requests

from babel import Locale
from box import Box, BoxList
from catalogue import Registry
from charset_normalizer import from_bytes, from_path
from codetiming import Timer
from colour import Color
from deepdiff import DeepDiff, Delta
from devtools import debug
from dotenv import dotenv_values
from pydantic import AnyHttpUrl, BaseConfig, BaseModel, BaseSettings, create_model, DirectoryPath, EmailStr, Field, FilePath, FutureDate, Json, NameEmail, \
    NegativeFloat, NegativeInt, NoneBytes, NoneStr, NoneStrBytes, NonNegativeFloat, NonNegativeInt, NonPositiveFloat, NonPositiveInt, PastDate, PositiveFloat, \
    PositiveInt, PrivateAttr, root_validator, SecretStr, StrBytes, UUID4, validate_arguments, ValidationError, validator
from pydantic.color import Color as PyColor
from pydantic.dataclasses import dataclass
from pydantic.env_settings import SettingsSourceCallable
from pydantic.json import pydantic_encoder
from pytz import BaseTzInfo, timezone, utc as UtcTz
from pytz_deprecation_shim._impl import _PytzShimTimezone as ShimTimezone
from typeguard import typechecked, typeguard_ignore
from typeguard.importhook import install_import_hook
from typing_extensions import Final, Literal, TypedDict
from tzlocal import get_localzone, get_localzone_name
