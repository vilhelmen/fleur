#!/usr/bin/env python3

from pathlib import Path
import itertools

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
reset = '\u001b[30m'
bold = '\u001b(B\u001b[m'

cyan = '\u001b[38;5;37m'
green = '\u001b[38;5;64m'

yellow = '\u001b[38;5;226m'

brown = '\u001b[38;5;130m'
rose = '\u001b[38;5;168m'

'''
.-------.
|       |
|       |
|       |
.-------.
.-------.
|       |
|       |
|   .   |
.-------.
.-------.
|       |
|       |
|  ~,~  |
.-------.
.-------.
|       |
|  &    |
|  \)/  |
.-------.
.-------.
|  VWV  |
|   |   |
|  \|/  |
.-------.
'''  # noqa: W605

# Ok, dumping assets to disk.
# First is flower type, then stage, then just a unique identifier for alternates
# Missing type is generic
# So, everything looks the same right now
# Split loaded art by newline

# I give this a 0% chance to load the art dir right
ART_PATH = 'art/'

# assets are dict of lists of lists, TYPE, STAGE (as int), then a list of possible frames to select from

flower_frame = [
    '{{BORDER}}.-------.{}\n'.format(reset),
    '{{BORDER}}|{}'.format(reset), '{{BORDER}}|{}\n'.format(reset),
    '{{BORDER}}|{}'.format(reset), '{{BORDER}}|{}\n'.format(reset),
    '{{BORDER}}|{}'.format(reset), '{{BORDER}}|{}\n'.format(reset),
    '{{BORDER}}.-------.{}\n'.format(reset)
]

class FlowerRegistry:
    def __init__(self):
        self.flower_types = {'TULIP'}
        self.seed_types = {
            'TULIP': [
                [2, 0, 1], [0, 2, 0], [0, 0, 1]
            ]
        }
        self.flower_colors = {}  # lol UHHHHH I'm gonna have to just make a table or something
        self.flower_assets = {}

        self.flower_assets = compile_assets([0, 1, 2, 3, 4], self.flower_types)


def frame_asset(asset):
    return [
        flower_frame[0],
        ''.join([flower_frame[1], asset[0], flower_frame[2]]),
        ''.join([flower_frame[3], asset[1], flower_frame[4]]),
        ''.join([flower_frame[5], asset[2], flower_frame[6]]),
        flower_frame[7]
    ]


def compile_assets(flower_stages, flower_types):
    compiled_assets = {type: [] for type in flower_types}
    root_path = Path(art_path)

    for stage in flower_stages:
        # TODO: apply base colors
        generic_stage_assets = [frame_asset(file.read_text().split('\n')) for file in root_path.glob(''.join(['_', str(stage), '*']))]

        for type in flower_types:
            # TODO: apply base colors
            type_stage_assets = [frame_asset(file.read_text().split('\n')) for file in root_path.glob(''.join([type, '_', str(stage), '*']))]

            compiled_assets[type].append(generic_stage_assets + type_stage_assets)

            if not compiled_assets[type][stage]:
                raise Exception('Missing asset for {} stage {}'.format(type, str(stage)))

    return all_assets
