#!/usr/bin/env python3

from . import art
import secrets

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

reset = '\u001b[30m'
bold = '\u001b[1m'


green = '\u001b[38;5;64m'

yellow = '\u001b[38;5;226m'

brown = '\u001b[38;5;130m'
rose = '\u001b[38;5;168m'


class FlowerRegistry:
    def __init__(self):
        self.flower_types = {'Tulip'}
        self.seed_types = {
            'Tulip': [
                'RRyyWw', 'rrYYww', 'rryyWw'
            ]
        }

        self.flower_colors = {
            'Tulip': {
                'rryyww': 'White',
                'rryyWw': 'White',
                'rryyWW': 'White',
                'rrYyww': 'Yellow',
                'rrYyWw': 'Yellow',
                'rrYyWW': 'White',
                'rrYYww': 'Yellow',
                'rrYYWw': 'Yellow',
                'rrYYWW': 'Yellow',
                'Rryyww': 'Red',
                'RryyWw': 'Pink',
                'RryyWW': 'White',
                'RrYyww': 'Orange',
                'RrYyWw': 'Yellow',
                'RrYyWW': 'Yellow',
                'RrYYww': 'Orange',
                'RrYYWw': 'Yellow',
                'RrYYWW': 'Yellow',
                'RRyyww': 'Black',
                'RRyyWw': 'Red',
                'RRyyWW': 'Red',
                'RRYyww': 'Black',
                'RRYyWw': 'Red',
                'RRYyWW': 'Red',
                'RRYYww': 'Purple',
                'RRYYWw': 'Purple',
                'RRYYWW': 'Purple'
            }
        }

        self.render_codes = {
            'Red': '\u001b[38;5;1m',
            'Yellow': '\u001b[38;5;226m',
            'White': '\u001b[38;5;15m',
            'Pink': '\u001b[38;5;168m',
            'Orange': '\u001b[38;5;208m',
            'Purple': '\u001b[38;5;127m',
            'Black': '\u001b[38;5;240m',
            'Blue': '\u001b[38;5;63m',
            'Green': '\u001b[38;5;35m',
            'Plant': '\u001b[38;5;35m',
            'Water': '\u001b[38;5;38m',
            'StandardBorder': '\u001b[38;5;130m',
            'RESET': '\u001b[30m',
            'BOLD': '\u001b[5m',
            'BLINK': '\u001b[1m',
        }
        # Why not...some require it lol
        self.render_codes.update({k.upper(): v for k, v in self.render_codes.items()})

        self.flower_assets = art.compile_assets([0, 1, 2, 3, 4], self.flower_types)

    class Flower:
        def __init__(self):
            self.stage = 0
            self.type = None
            self.genes = None
            self.known = None  # Genes are known
            self.water_level = 0
            self.watered_now = False  # I was going to have the border turn blue but...?

    def render_flower(self, flower, highlighted, moving):
        border = []
        if highlighted:
            border.append(self.render_codes['BOLD'])
        if moving:
            border.append(self.render_codes['BLINK'])

        if flower.watered_now:
            border.append(self.render_codes['Water'])
        else:
            border.append(self.render_codes['StandardBorder'])

        border = ''.join(border)

        return (CURSOR_DOWN + CURSOR_LEFT_N.format(art.FRAME_WIDTH)).join(
            secrets.choice(self.flower_assets[flower.type][flower.stage])
        ).format(
            BORDER=border,
            FLOWER=self.render_codes[self.flower_colors[flower.type][flower.genes]],
            **self.render_codes
        )
