#!/usr/bin/env python3

import logging

from . import util

util.setup_logging()


class FlowerCell:
    def __init__(self):
        self.stage = 0
        self.type = None
        self.genes = None
        self.known = None # Genes are known
        self.water = 0
        self.watered_now = False # I was going to have the border turn blue but...?

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
