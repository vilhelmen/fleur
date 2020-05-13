#!/usr/bin/env python3

import logging
import logging.handlers
import contextlib
import curses
import sys
import termios

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


def teardown_console(stdscr, tcattr):
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

    # TBH I'm not sure why I'm bothering asking curses when I know what I'm gonna get back
    # I'm so mad at curses I never want to talk to it again
    # sys.stdout.write(curses.tparm(curses.tigetstr("sgr"), 0))
    sys.stdout.write('\u001b[0m')

    # Something is still up with newlines after an exit, this seems to fix it
    # So we unwind curses, do a reset, and then just smash it with a hammer to be sure
    termios.tcsetattr(sys.stdout.fileno(), termios.TCSAFLUSH, tcattr)


def setup_console():
    # Curses wipes scrollback on exit and that's lame. I'm probably already wiping scrollback on start...
    # but that's not entirely my fault
    tcattr = termios.tcgetattr(sys.stdout.fileno())

    stdscr = curses.initscr()
    curses.def_shell_mode()  # Can I do this before init? (LOL NO CURSES MAD)

    curses.start_color()  # Turning on color mode SETS the text color to some weird grey. Why? WHO KNOWS.
    curses.use_default_colors()
    if curses.COLORS != 256:
        raise RuntimeError('256-color mode not detected')

    # WHY DO I HAVE TO MAKE THE COLORS
    for i in range(curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    # Color pair for color number x is 256*x
    # They can be redefined.
    # Do i just need to init all of them
    curses.init_pair(100, 100, 0)

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

    return stdscr, tcattr


@contextlib.contextmanager
def console_prep():
    logger.debug('Configuring terminal')
    stdscr, tcattr = (None, None)
    try:
        stdscr, tcattr = setup_console()
        yield stdscr
    finally:
        if stdscr is not None:
            logger.debug('Restoring terminal')
            teardown_console(stdscr, tcattr)


def set_console_size(rows, cols):
    # define a signal handler, attach to whatever signal that is, also do an initial poll
    # It's SIGWINCH, but you gotta query again.
    # ...Or I could just ask in a loop until it's the right size.
    # I AM NO LONGER ASKING https://apple.stackexchange.com/a/47841/205576
    logging.debug('Set size to (x,y): (%s,%s)', cols, rows)
    # I cannot for the life of me find the magic tput name for this
    # Best I can tell is that it's extremely nonstandard, but X does it, so everyone should anyway
    # It's not even in tcap/terminfo
    sys.stdout.write(''.join(['\u001b[8;', str(rows), ';', str(cols), 't']))
