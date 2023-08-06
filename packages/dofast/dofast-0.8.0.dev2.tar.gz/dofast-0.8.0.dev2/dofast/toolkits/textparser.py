#!/usr/bin/env python
import os
import random
import re
import sys
from collections import defaultdict
from functools import reduce
from typing import Union, List

import codefast as cf
import numpy as np
import pandas as pd


class TextParser(object):
    def __init__(self):
        ...

    @staticmethod
    def _string_match(pattern: str, text: str) -> bool:
        return True if re.search(re.compile(pattern), text) else False

    @staticmethod
    def match(pattern: Union[str, List], text: str) -> bool:
        '''whether text matches any of item from pattern'''
        if isinstance(pattern, str):
            return TextParser._string_match(pattern, text)

        assert isinstance(pattern, list), 'Pattern is either list or str'
        return any(TextParser._string_match(e, text) for e in pattern)
