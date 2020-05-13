#!/usr/bin/env python3

from pathlib import Path
import logging

log = logging.getLogger('ART')

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

# Deal with it, update it yourself. I'm not scanning for non-printables every time I render, this is inefficient enough
# If you go wider than the frame was designed for, that's on you
FRAME_WIDTH = 9
FRAME_HEIGHT = 5

# FLOWER_FRAME = {
#     'ls': '|', 'rs': '|', 'ts': '-', 'bs': '-',
#     'tl': '+', 'tr': '+', 'bl': '+', 'br': '+'
# }
# CURSES >:C
FLOWER_FRAME = [
    '|', '|', '-', '-', '+', '+', '+', '+'
]

flower_frame = [
    '{BORDER}+-------+{RESET}',
    '{BORDER}|{RESET}', '{BORDER}|{RESET}',
    '{BORDER}|{RESET}', '{BORDER}|{RESET}',
    '{BORDER}|{RESET}', '{BORDER}|{RESET}',
    '{BORDER}+-------+{RESET}'
]


# assets are dict of lists of lists, TYPE, STAGE (as int), then a list of possible frames to select from
def frame_asset(asset):
    return [
        flower_frame[0],
        ''.join([flower_frame[1], asset[0], flower_frame[2]]),
        ''.join([flower_frame[3], asset[1], flower_frame[4]]),
        ''.join([flower_frame[5], asset[2], flower_frame[6]]),
        flower_frame[7]
    ]


def compile_assets(flower_types):
    compiled_assets = {type: {} for type in flower_types}
    root_path = Path(__file__).parent

    # Empty frame assets
    compiled_assets[0] = [frame_asset(file.read_text().split('\n')) for file in root_path.glob(''.join(['0_*']))]

    for stage in [1, 2, 3, 4]:
        # TODO: apply base colors?
        generic_stage_assets = [frame_asset(file.read_text().split('\n')) for file in root_path.glob(''.join(['_', str(stage), '*.txt']))]

        for type in flower_types:
            # TODO: apply base colors?
            type_stage_assets = [frame_asset(file.read_text().split('\n')) for file in root_path.glob(''.join([type, '_', str(stage), '*.txt']))]
            compiled_assets[type][stage] = (generic_stage_assets + type_stage_assets)

            if not compiled_assets[type][stage]:
                raise Exception('Missing asset for {} stage {}'.format(type, str(stage)))

    return compiled_assets
