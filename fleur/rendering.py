#!/usr/bin/env python3

import curses
import itertools

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

BG = {
    'STANDARD': 238,
}

FG = {
    'RED': 1,  # May be a bit much
    'ORANGE': 208,
    'YELLOW': 226,
    'WHITE': 15,
    'PINK': 168,
    'PURPLE': 127,
    'BLACK': 234,
    'BLUE': 63,
    'GREEN': 35,  # TODO: Differentiate from PLANT
    'PLANT': 35,
    'WATER': 38,
    'BORDER': 130,
    'TEXT': 253,
    'ANY': 0  # Doesn't matter
}

# Horrid dict of dicts mapping [bg][fg] to a color pair number
COLOR_PAIRS = {k: {} for k in BG.keys()}


def init_color_palette():
    # I hate curses so much
    # Having to use a palette makes me want to cry
    # Just let me set the colors individually
    # I almost want to ignore curses graphics altogether and use stdout (hmmm)
    for pair_no, ((bgname, bgno), (fgname, fgno)) in enumerate(itertools.product(BG.items(), FG.items()), start=1):
        # 0 is reserved
        curses.init_pair(pair_no, fgno, bgno)
        COLOR_PAIRS[bgname][fgname] = pair_no


class Renderable:
    def __init__(self, y=0, x=0, rows=0, cols=0, window=None):
        if window is not None:
            self.window = window
        elif rows == 0 or cols == 0:
            raise RuntimeError('Renderable with no size!')
        else:
            self.window = curses.newwin(y, x, rows, cols)

    def render(self):
        raise RuntimeError('render() not set!')
