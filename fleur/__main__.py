#!/usr/bin/env python3

import logging

from . import util, logic

util.setup_logging()

util.setup_console_control()

util.clear_screen_and_reset_position()

GL = logic.GameLogic()

GL.render()

