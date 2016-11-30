#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import SysLogHandler


handler = SysLogHandler(address = '/dev/log')
handler.setLevel(logging.ERROR)
formatter = logging.Formatter("PNCAST - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
