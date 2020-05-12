#!/usr/bin/env python3

import logging
import logging.handlers
import contextlib
import curses
import sys

logger = logging.getLogger('util')

# console stuff
# https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#cursor-navigation


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


def teardown_console(stdscr):
    stdscr.keypad(False)
    curses.nocbreak()
    curses.curs_set(1)
    curses.echo()

    # Nothing says what this does and does not record and reset
    # So I'm still going to unwind my changes
    curses.reset_shell_mode()

    # curses.endwin()
    # We don't seem to reset out colors. It *might* not be possible to know what current colors are
    # But I don't buy that, there's an escape code for everything
    # Ehhhhhh maybe not. Let's just do a reset
    sys.stdout.write('\u001b[0m')


def setup_console():
    # using wrapper would be cool, but I can't unset visibility
    stdscr = curses.initscr()
    curses.def_shell_mode()  # Can I do this before init? (LOL NO CURSES MAD)

    curses.start_color()  # Turning on color mode SETS the text color to some weird grey. Why? WHO KNOWS.
    if curses.COLORS != 256:
        raise RuntimeError('256-color mode not detected')

    curses.noecho()
    curses.curs_set(0)

    curses.cbreak()  # TBH idk if this is helpful. I WON'T receive ^C
    stdscr.keypad(True)

    curses.def_prog_mode()  # I MEAN I GUESS

    # Moved to game logic because UGH, maybe I'll just use the wrapper
    # Wrapper sucks because endwin() resets terminal content
    # Atexit is after stacktrace printing
    # Making my OWN wrapper >:C
    # atexit.register(teardown_console, stdscr)

    return stdscr


@contextlib.contextmanager
def console_prep():
    logger.debug('Configuring terminal')
    stdscr = None
    try:
        stdscr = setup_console()
        yield stdscr
    finally:
        if stdscr is not None:
            logger.debug('Restoring terminal')
            teardown_console(stdscr)


def set_console_size(rows, cols):
    # define a signal handler, attach to whatever signal that is, also do an initial poll
    # It's SIGWINCH, but you gotta query again.
    # ...Or I could just ask in a loop until it's the right size.
    # I AM NO LONGER ASKING https://apple.stackexchange.com/a/47841/205576
    logging.debug('Set size to (x,y): (%s,%s)', cols, rows)
    sys.stdout.write(''.join(['\u001b[8;', str(rows), ';', str(cols), 't']))
