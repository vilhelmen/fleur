#!/usr/bin/env python3

from . import art, rendering
import secrets


RENDER_CODES = {
    'Red': '\u001b[38;5;1m',
    'Yellow': '\u001b[38;5;226m',
    'White': '\u001b[38;5;15m',
    'Pink': '\u001b[38;5;168m',
    'Orange': '\u001b[38;5;208m',
    'Purple': '\u001b[38;5;127m',
    'Black': '\u001b[38;5;234m',
    'Blue': '\u001b[38;5;63m',
    'Green': '\u001b[38;5;35m',
    'Plant': '\u001b[38;5;35m',
    'Background': '\u001b[48;5;238m',  # TODO: Pull this up and out somewhere?
    'WaterBorder': '\u001b[38;5;38m',
    'NormalBorder': '\u001b[38;5;130m',
    'RESET': '\u001b[30m',
    'BOLD': '\u001b[5m',
    'BLINK': '\u001b[1m',
}
# RENDER_CODES.update({k.upper(): v for k, v in render_codes.items()})

FLOWER_TYPES = {'Tulip'}

SEED_TYPES = {
    'Tulip': [
        'RRyyWw', 'rrYYww', 'rryyWw'
    ]
}

FLOWER_COLORS = {
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

# [type][stage], or [0] for empty
FLOWER_ASSETS = art.compile_assets(FLOWER_TYPES)


class Flower:
    def __init__(self, type=None, stage=None, genes=None, known=False):
        self.type = type
        self.stage = stage
        self.genes = genes
        self.known = known  # Genes are known
        self.water_level = 0
        self.watered_now = False  # I was going to have the border turn blue but...?


# TODO: Move border rendering up a level?
# Make corners of known genes a different shape? *?
def render_flower(flower, highlighted, moving):
    border = []
    if highlighted:
        border.append(RENDER_CODES['BOLD'])
    if moving:
        border.append(RENDER_CODES['BLINK'])

    if flower is not None and flower.watered_now:
        border.append(RENDER_CODES['WaterBorder'])
    else:
        border.append(RENDER_CODES['NormalBorder'])

    border = ''.join(border)

    if flower is None or flower.stage == 0:  # Hell, there are at least two NULL flowers
        return (rendering.CURSOR_DOWN + rendering.CURSOR_LEFT_N.format(art.FRAME_WIDTH)).join(secrets.choice(FLOWER_ASSETS[0])
        ).format(
            BORDER=border,
            **RENDER_CODES
        )
    else:
        return (rendering.CURSOR_DOWN + rendering.CURSOR_LEFT_N.format(art.FRAME_WIDTH)).join(
            secrets.choice(FLOWER_ASSETS[flower.type][flower.stage])
        ).format(
            BORDER=border,
            FLOWER=RENDER_CODES[FLOWER_COLORS[flower.type][flower.genes]],
            **RENDER_CODES
        )
