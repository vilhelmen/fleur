#!/usr/bin/env python3

from operator import itemgetter

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
|   .   |
.-------.
.-------.
|       |
|       |
|  ~.~  |
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

flower_stage_one = [
    '       ',
    '       ',
    '   {}.{}   '.format(green, reset)
]

flower_stage_two = [
    '       ',
    '       ',
    '  {}~.~{}  '.format(green, reset)
]

flower_stage_three = [
    '       ',
    '  {{FLOWER}}&{}    '.format(reset),
    '  {}\\)/{}  '.format(green, reset)
]
flower_stage_four = [
    '  {{FLOWER}}VWV{}  '.format(reset),
    '   {}|{}   '.format(green, reset),
    '  {}\\|/{}  '.format(green, reset)
]

frame = [
    '{{BORDER}}.-------.{}\n'.format(reset),
    '{{BORDER}}|{}'.format(reset), '{{BORDER}}|{}\n'.format(reset),
    '{{BORDER}}|{}'.format(reset), '{{BORDER}}|{}\n'.format(reset),
    '{{BORDER}}|{}'.format(reset), '{{BORDER}}|{}\n'.format(reset),
    '{{BORDER}}.-------.{}\n'.format(reset)
]

framed_flowers = []
for flower in [flower_stage_one, flower_stage_two, flower_stage_three, flower_stage_four]:
    # Shut up, I've thrown out a day of work. THIS IS FINE
    framed_flowers.append(
        ''.join([
            frame[0],
            frame[1], flower[0], frame[2],
            frame[3], flower[1], frame[4],
            frame[5], flower[2], frame[6],
            frame[7]
        ])
    )

#print(framed_flowers[0].format(BORDER=brown, FLOWER=rose))
#print(framed_flowers[1].format(BORDER=brown, FLOWER=rose))
#print(framed_flowers[2].format(BORDER=brown, FLOWER=rose))
#print(framed_flowers[3].format(BORDER=brown, FLOWER=rose))
