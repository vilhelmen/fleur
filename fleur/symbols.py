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

# Annotate a line's color with a dict. key = character position, value = format code to apply
# Please don't forget to reset colors
# '{XXXX}' for color setting XXXX that is applied later (don't forget to reset)


def stitch(template, color_spec):
    """
    Given a frame of data (a list of lines), and a list of line colorings (a dict of positions and color codes), compost them together

    :param templates: List of base art
    :param color_specs: Spec bundles for each row
    :return: List of colored frame data (list of lines)
    """
    # oh baby python's sort is stable. That means I can just stick everything together and make it python's problem
    # (and I don't have to construct strings backwards! or forwards but an offset tracker based on the inserted... no)

    # Convert the color specs into a collection of sorted tuples (index, code)
    processed_color_specs = [[(x, frame_colors[x]) for x in sorted(frame_colors)] for frame_colors in color_spec]

    # convert the frames into a collection of sorted tuples (index, character)
    processed_templates = [[_ for _ in enumerate(template)] for template in template]

    # Append the template data to the color code data
    # Do them NASTY and sort it by the index. It's stable, so the color code will always come before the character
    # Also helpfully means I won't accidentally index out of bounds if you messed up earlier
    glued_data = [a + b for a, b in zip(processed_color_specs, processed_templates)]

    # join the contents back together
    return [''.join([x[1] for x in sorted(frame_line, key=itemgetter(0))]) for frame_line in glued_data]


# UGH THIS FORMAT iS TOTALLY DIFFERENT THAT WHAT I WROTE THE STITCHER FOR
# WHAT HAVE I DONE
unframed_flowers = [
    stitch(
        [
            '       ',
            '       ',
            '   .   '
        ],
        [
            None,
            None,
            {
                3: green,
                4: reset
            }]),
    stitch(
        [
            '       ',
            '       ',
            '  ~.~  '
        ],
        [
            None,
            None,
            {
            16: green,
            19: reset
        }
        ]
    ),
    stitch(),
    stitch()
]

unframed_flowers = deepstitch(
    [

        ,
        [
            '       ',
            '  &    ',
            '  \\)/  '
        ],
        [
            '  VWV  ',
            '   |   ',
            '  \\|/  '
        ],
    ], [
        ,
        ,
        {
            9: '{FLOWER}',
            10: reset,
            16: green,
            19: reset,
        },
        {
            2: '{FLOWER}',
            5: reset,
            10: green,
            11: reset,
            16: green,
            19: reset,
        }
    ])

colored_frame = stitch(
    ['.-------.',
     '|', '|',
     '|', '|',
     '|', '|',
     '.-------.'],
    [
        {
            0: '{BORDER}',
            9: reset
        },
    ] + [
        {
            0: '{BORDER}',
            1: reset
        }
    ] * 6 + [
        {
            0: '{BORDER}',
            9: reset
        },
    ]
)

framed_flowers = []
for flower in unframed_flowers:
    # Shut up, I've thrown out a day of work. THIS IS FINE
    framed_flowers.append(
        [
            colored_frame[0],
            [colored_frame[1]] + flower[0] + [colored_frame[2]],
            [colored_frame[3]] + flower[1] + [colored_frame[4]],
            [colored_frame[5]] + flower[2] + [colored_frame[6]],
            colored_frame[7]
        ]
    )

print('\n'.join(framed_flowers[0]).format(BORDER=brown, FLOWER=rose))
print('\n'.join(framed_flowers[1]).format(BORDER=brown, FLOWER=rose))
print('\n'.join(framed_flowers[2]).format(BORDER=brown, FLOWER=rose))
print('\n'.join(framed_flowers[3]).format(BORDER=brown, FLOWER=rose))
