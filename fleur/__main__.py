#!/usr/bin/env python3

import logging

from . import util, logic

util.setup_logging()

GL = logic.GameLogic()

GL.launch()
