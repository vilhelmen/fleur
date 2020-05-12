#!/usr/bin/env python3

import logging
import curses

from . import util, logic


def launch():
    # curses endwin resets the terminal contents, which is rude. So we're gonna go with manual setup again
    with util.console_prep() as stdscr:
        GL = logic.GameLogic(root_window=stdscr)

        GL.launch()


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, '')
    # I can't imagine I'm going to do any encoding
    # code = locale.getpreferredencoding()
    util.setup_logging()
    launch()
