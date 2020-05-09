#!/usr/bin/env python3

import sys
import threading

# COLUMN IS X AND ROW IS Y AND I'M PUTTING IT HERE BEFORE I LOSE MY MIND ALSO IT'S ONE BASED

# Ripped from my terminal
'''
# Solarized Dark colour scheme
BOLD="$(tput bold)"
RESET="$(tput sgr0)"
YELLOW="$(tput setaf 136)"
ORANGE="$(tput setaf 166)"
RED="$(tput setaf 124)"
MAGENTA="$(tput setaf 125)"
VIOLET="$(tput setaf 61)"
BLUE="$(tput setaf 33)"
CYAN="$(tput setaf 37)"
GREEN="$(tput setaf 64)"
WHITE="$(tput setaf 254)"
'''

# printf "$(tput sgr0)" | uniscribe

CURSOR_UP = '\u001b[1A'
CURSOR_DOWN = '\u001b[1B'
CURSOR_RIGHT = '\u001b[1C'
CURSOR_LEFT = '\u001b[1D'

CURSOR_UP_N = '\u001b[{}A'
CURSOR_DOWN_N = '\u001b[{}B'
CURSOR_RIGHT_N = '\u001b[{}C'
CURSOR_LEFT_N = '\u001b[{}D'

CURSOR_DOWN_FAR_LEFT = '\u001b[1E'

def set_cursor_position_string(row, col):
    return '\u001b[{};{}H'.format(row, col)


FULL_RESET = '\u001b[0m'
BOLD = '\u001b[1m'
BLINK = '\u001b[5m'
BLINK_OFF = '\u001b[25m'
INVERT = '\u001b[7m'


RENDER_LOCK = threading.Event()


class Renderable:
    def __init__(self, render_x=1, render_y=1):
        self.render_target = (render_x, render_y)

    def move_to_render_target_string(self):
        return '\u001b[{};{}H'.format(self.render_target[1], self.render_target[0])

    def move_to_render_target(self):
        sys.stdout.write(self.move_to_render_target_string())

    def render(self):
        raise Exception('Render not set!')
