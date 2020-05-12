#!/usr/bin/env python3

import sys, logging, curses

from . import rendering, rendering, flowers, util, art


class FlowerCell(rendering.Renderable):
    def __init__(self, x=1, y=1):
        super().__init__(x=x, y=y)
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
    def __init__(self, x=1, y=1, rows=5, cols=4):
        super().__init__(x=x, y=y)
        self.rows = rows
        self.cols = cols
        # X, Y
        self.size = (self.cols * art.FRAME_WIDTH, self.rows * art.FRAME_HEIGHT)

        self.cells = [[FlowerCell(x=x + art.FRAME_WIDTH * x,
                                  y=y + art.FRAME_HEIGHT * y) for y in range(self.rows)] for x in range(self.cols)]

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
    def __init__(self, x=1, y=1, height=40):  # fix default height
        super().__init__(x=x, y=y)
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
    def __init__(self, root_window, rows=5, cols=4):
        super().__init__(window=root_window)
        #self.grid = FlowerGrid(x=2, y=2, rows=rows, cols=cols)
        #self.grid.flowers_pls()
        #self.sidebar = Sidebar(x=self.grid.size[0] + 3, y=2, height=self.grid.size[1])

        # (r,g,b) 0-1000 is wack
        self.window.clear()

        # Uhh, bootscreen here if I feel creative

        # Something about this breaks text display, which is to say it went black on black and took AGES to figure out
        # Mother of god I think it's initializing the 8-bit colorspace to all (0,0,0)
        # WHY ARE YOU LIKE THIS
        self.window.bkgd('#', curses.color_pair(1))
        logging.debug('color %s', curses.color_pair(238))
        logging.debug('Color is (rgb), %s', curses.color_content(238))  # it SAYS (0,1000,1000) but yeah right.
        self.window.addstr(0, 0, "Current mode: Typing mode") #, curses.A_REVERSE)
        self.window.addstr('WHY ARE YOU LIKE THIS')
        self.window.refresh()
        self.window.addstr('WHY CANT YOU BE NORMAL')
        self.window.refresh()
        # But this printed in the right color (??? coincidence? Default grey may just be similar enough)
        sys.stdout.write('uuuuu')
        sys.stdout.flush()
        self.window.getch()

        # Something about the resize blanks the display, probably a curses SIGWICH handler blanking the canvas
        logging.debug('Old size, maybe WHO KNOWS: %s', self.window.getmaxyx())
        logging.debug('CURSES WILL NOT EMIT RESIZE >:C')
        util.set_console_size(40, 80)
        curses.resizeterm(40, 80)  # Literally none of this works, don't bother checking the resize

    # WHAT DO YOU MEAN NO KEYWORD ARGUMENTS THEY ARE EXPLICITLY NAMED THESE THINGS EVERYWHERE
    # Freaking C bindings
    # BORDER = {
    #     'ls': '║', 'rs': '║', 'ts': '═', 'bs': '═',
    #     'tl': '╔', 'tr': '╗', 'bl': '╚', 'br': '╝'
    # }
    BORDER = ['║', '║', '═', '═', '╔', '╗', '╚', '╝']

    def render(self):
        #self.window.refresh()
        self.window.addstr(10, 10, 'ASLDJALSJDLAJSDLK')
        self.window.refresh()
        #self.window.border(*self.BORDER)
        # sys.stdout.write(''.join([
        #     self.move_to_render_target_string(),
        #     rendering.FULL_RESET,
        #     ''.join(['╔', '═'*self.grid.size[0], '╦', '═'*self.sidebar.width, '╗']),
        #     ''.join([rendering.CURSOR_DOWN_FAR_LEFT, '║', rendering.CURSOR_RIGHT_N.format(self.grid.size[0]), '║', rendering.CURSOR_RIGHT_N.format(self.sidebar.width), '║'])*self.grid.size[1],
        #     ''.join([rendering.CURSOR_DOWN_FAR_LEFT, '╚', '═'*self.grid.size[0], '╩', '═'*self.sidebar.width, '╝'])
        # ]))
        # self.grid.render()
        # self.sidebar.render()
        # sys.stdout.flush()  # This may need to move

    def launch(self):
        state = {}
        local_state = {}
        # Boot screen? Also why is the game like 20 rows taller than it should be.
        self.render()
        while True:
            break

        util.teardown_console(self.window)
