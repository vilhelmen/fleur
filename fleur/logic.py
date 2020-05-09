#!/usr/bin/env python3

import sys, logging

from . import rendering, rendering, flowers, util, art


class FlowerCell(rendering.Renderable):
    def __init__(self, render_x=1, render_y=1):
        super().__init__(render_x=render_x, render_y=render_y)
        self.highlighted = False  # cursor over it
        self.moving = False  # Selected to move
        self.flower = None
        self._render_cache = None

    def set_flower(self, flower):
        self.flower = flower

    def get_flower(self):
        return self.flower

    def render(self):
        if not self._render_cache:
            render = ''.join([
                self.move_to_render_target_string(),
                flowers.render_flower(self.flower, self.highlighted, self.moving)
            ])
            self._render_cache = render
        sys.stdout.write(self._render_cache)


class FlowerGrid(rendering.Renderable):
    def __init__(self, render_x=1, render_y=1, rows=5, cols=4):
        super().__init__(render_x=render_x, render_y=render_y)
        self.rows = rows
        self.cols = cols
        # X, Y
        self.size = (self.cols * art.FRAME_WIDTH, self.rows * art.FRAME_HEIGHT)

        self.cells = [[FlowerCell(render_x=render_x+art.FRAME_WIDTH*x,
                                  render_y=render_y+art.FRAME_HEIGHT*y) for y in range(self.rows)] for x in range(self.cols)]

    def render(self):
        # Move background render to here
        # We're just gonna assume rendering the cells can handle clearing their render space for now
        # We could blank our region first, though
        # I might wrap the flower bed in a border, but that may go to a higher level render b/c sidebar?
        # No border on sidebar and render here? render origin will need to move over one in cell init
        sys.stdout.write(flowers.RENDER_CODES['Background'])
        for x in range(self.cols):
            for y in range(self.rows):
                self.cells[x][y].render()

    def flowers_pls(self):
        # Just make some things pls
        self.cells[0][0].set_flower(flowers.Flower(type='Tulip', stage=1, genes='RrYyww'))
        self.cells[1][1].set_flower(flowers.Flower(type='Tulip', stage=2, genes='RrYyww'))
        self.cells[1][2].set_flower(flowers.Flower(type='Tulip', stage=3, genes='RrYYww'))
        self.cells[2][2].set_flower(flowers.Flower(type='Tulip', stage=3, genes='RrYyWw'))
        self.cells[3][3].set_flower(flowers.Flower(type='Tulip', stage=4, genes='RRYYWW'))
        self.cells[3][4].set_flower(flowers.Flower(type='Tulip', stage=4, genes='rrYyWW'))
        self.cells[0][3].set_flower(flowers.Flower(type='Tulip', stage=4, genes='RRYyww'))


class Sidebar(rendering.Renderable):
    def __init__(self, render_x=1, render_y=1, height=40):  # fix default height
        super().__init__(render_x=render_x, render_y=render_y)
        # also maybe make a minimum height
        self.height = height
        self.width = 20  # TODO: figure out

    def render(self):
        # blank space
        render = ''.join([
            self.move_to_render_target_string(),
            rendering.FULL_RESET,
            ''.join([rendering.CURSOR_DOWN, rendering.CURSOR_LEFT_N.format(self.width)]).join(
                [' '*self.width] * self.height
            )
        ])
        sys.stdout.write(render)


class GameLogic(rendering.Renderable):
    def __init__(self, rows=5, cols=4):
        super().__init__()
        self.grid = FlowerGrid(render_x=2, render_y=2, rows=rows, cols=cols)
        self.grid.flowers_pls()
        self.sidebar = Sidebar(render_x=self.grid.size[0]+3, render_y=2, height=self.grid.size[1])
        util.set_console_size(self.grid.size[0]+self.sidebar.width+3, self.grid.size[1]+self.sidebar.height+2)

    def render(self):
        sys.stdout.write(''.join([
            self.move_to_render_target_string(),
            rendering.FULL_RESET,
            ''.join(['╔', '═'*self.grid.size[0], '╦', '═'*self.sidebar.width, '╗']),
            ''.join([rendering.CURSOR_DOWN_FAR_LEFT, '║', rendering.CURSOR_RIGHT_N.format(self.grid.size[0]), '║', rendering.CURSOR_RIGHT_N.format(self.sidebar.width), '║'])*self.grid.size[1],
            ''.join([rendering.CURSOR_DOWN_FAR_LEFT, '╚', '═'*self.grid.size[0], '╩', '═'*self.sidebar.width, '╝'])
        ]))
        self.grid.render()
        self.sidebar.render()
