#!/usr/bin/env python3

import logging

from . import util

util.setup_logging()


class FlowerCell:
    def __init__(self):


        self.highlighted = False # cursor over it
        self.selected_move = False # A move target. Idk, blink?
        self._render = None
        self.update()

    def update(self):
        """Render and cache"""


    @@property
    def render(self):
        return self._render



class Game:
    def __init__(self, col, row):
