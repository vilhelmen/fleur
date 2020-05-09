#!/usr/bin/env python3

import logging
import logging.handlers
import atexit

import termios, sys, tty

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
    logging.debug('Logging Boot')


def restore_console_settings(fd, restore_conf):
    # be kind, rewind
    termios.tcsetattr(fd, termios.TCSAFLUSH, restore_conf)
    sys.stdout.write('\u001b[0m\u001b[1S\n')


# Mangled from docs
def setup_console_control(disable_echo=True):
    fd = sys.stdin.fileno()
    # Restore data
    restore = termios.tcgetattr(fd)
    # Raw mode
    tty.setraw(sys.stdin)

    if disable_echo:
        # Disable keypress echoing
        new_config = termios.tcgetattr(fd)
        new_config[3] = new_config[3] & ~termios.ECHO
        # Drain changes mode when output is flushed, TCSAFLUSH to discard pending input (tempting)
        termios.tcsetattr(fd, termios.TCSADRAIN, new_config)
        atexit.register(restore_console_settings, fd, restore)
    #
    # while True:
    #     char = sys.stdin.read(1)
    #     if ord(char) == 3: # CTRL-C
    #         break;
    #     print ord(char)
    #     sys.stdout.write(u"\u001b[1000D") # Move all the way left


def set_console_size(cols, rows):
    # define a signal handler, attach to whatever signal that is, also do an initial poll
    # It's SIGWINCH, but you gotta query again.
    # ...Or I could just ask in a loop until it's the right size.
    # I AM NO LONGER ASKING https://apple.stackexchange.com/a/47841/205576
    sys.stdout.write(''.join(['\u001b[8;', str(rows), ';', str(cols), 't']))


def clear_screen_and_reset_position():
    # may or may not reset position on clear, explicitly do it.
    sys.stdout.write('\u001b[2J\u001b[1;1H')


# Nuke stdin
# termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)

# This refuses to work despite test code that seems to work fine
# It shouldn't be needed anyway
# def get_cursor_position():
#     """
#     :return: row, column (1 based)
#     """
#     # I'm putting a lot into this function I don't expect to use
#     sys.stdout.write('\u001b[6n')
#     # ESC[n;mR
#     # At least 5 characters, then a terminal R
#     response = [sys.stdin.read(6)]
#     while ord(response[-1][-1]) != ord('R'):
#         response.append(sys.stdin.read(1))
#
#     # I mean, the correct option is regex. We don't even know if we've captured the response.
#     # Strip leading and trailing
#     response = ''.join(response)
#
#     response = response[response.find('\u001b[') + 2:-1].split(';')
#     n = int(response[0])
#     m = int(response[1])
#
#     return n, m
