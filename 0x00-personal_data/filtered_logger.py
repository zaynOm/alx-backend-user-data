#!/usr/bin/env python3
"""Regex-ing"""

import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, sparator: str
):
    """Returns the log message obfuscated"""
    keys = "=|".join(fields)
    return re.sub(rf"(.+=.+{sparator}{keys}=)(.+?){sparator}",
                  rf"\1{redaction}{sparator}", message)
