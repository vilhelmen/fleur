#!/usr/bin/env python3

import logging
import logging.handlers
import atexit
import curses

import termios, sys, tty

logger = logging.getLogger('util')

# console stuff
# https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#cursor-navigation

# Arbitrary notes: ESC 7 and ESC 8 might be a position save and restore. That could be cool. Or useless? A faster reset?
# ESC [ s
# ESC [ u
# http://man7.org/linux/man-pages/man4/console_codes.4.html


# Just ripped from the docs
def setup_logging():
    rootLogger = logging.getLogger('')
    rootLogger.setLevel(logging.DEBUG)
    socketHandler = logging.handlers.SocketHandler('localhost',
                                                   logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    # don't bother with a formatter, since a socket handler sends the event as
    # an unformatted pickle
    rootLogger.addHandler(socketHandler)

    # Now, we can log to the root logger, or any other logger. First the root...
    logging.debug('Logging online')


def breakdown_console(stdscr):
    stdscr.keypad(False)
    curses.nocbreak()
    curses.curs_set(1)
    curses.echo()
    curses.endwin()


def setup_console():
    # using wrapper would be cool, but I can't unset visibility
    stdscr = curses.initscr()
    curses.start_color()

    curses.noecho()
    curses.curs_set(0)

    curses.cbreak()  # TBH idk if this is helpful. I WON'T receive ^C
    stdscr.keypad(True)

    # Moved to game logic because UGH, maybe I'll just use the wrapper
    # atexit.register(breakdown_console, stdscr)

    return stdscr

def set_console_size(cols, rows):
    # define a signal handler, attach to whatever signal that is, also do an initial poll
    # It's SIGWINCH, but you gotta query again.
    # ...Or I could just ask in a loop until it's the right size.
    # I AM NO LONGER ASKING https://apple.stackexchange.com/a/47841/205576
    logging.debug('Reset to (x,y): (%s,%s)', cols, rows)
    sys.stdout.write(''.join(['\u001b[8;', str(rows), ';', str(cols), 't']))
