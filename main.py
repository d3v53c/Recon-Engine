import argparse
import curses
import time
import traceback
import math

from curses import wrapper, A_REVERSE, curs_set
from core.utils import banner, start_timer
from scapy.all import *
from recon.handler import ReconEngine

HEADER_HEIGHT, HEADER_WIDTH = 13, 60
TIMER_HEIGHT, TIMER_WIDTH = 13, 9
FOOTER_OFFSET = 2
DEBUG = True


def main(win):
    # no echo of characters typed
    curses.noecho()

    # init color pair
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)

    # clear window before start
    win.clear()

    # set background
    win.bkgd(' ', curses.color_pair(1))

    try:
        curs_set(0)
    except Exception as e:
        raise

    # header banner
    HEADER_Y, HEADER_X = 0, math.floor((curses.COLS - (HEADER_WIDTH + 5)) / 2)
    header = win.subwin(HEADER_HEIGHT, HEADER_WIDTH, HEADER_Y, HEADER_X)
    header_text = banner()
    # curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # header.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
    header.addstr(1, 1, header_text)
    header.refresh()

    # parser = argparse.ArgumentParser(description=banner())
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Target address", nargs='?')
    # parser.add_argument("-p", metavar="", help="Single port e.g. 80")
    # parser.add_argument("-pl", metavar="", help="Port list e.g. 21,22,80")
    # parser.add_argument("-pr", metavar="", help="Port range e.g. 20-30")
    # parser.add_argument(
    #     "-t",
    #     metavar="",
    #     type=int,
    #     default=2,
    #     help="Timeout value (default 2)",
    # )

    args = parser.parse_args()
    win.refresh()

    # timer window
    TIMER_Y, TIMER_X = 9, (HEADER_X + HEADER_WIDTH + 1)
    timer = win.subwin(TIMER_HEIGHT, TIMER_WIDTH, TIMER_Y, TIMER_X)
    # curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    # timer.bkgd(' ', curses.color_pair(2) | curses.A_BOLD)
    # timer.addstr(1, 1, '00:00')
    timer.refresh()

    # content window
    CONTENT_HEIGHT = curses.LINES - (HEADER_HEIGHT + FOOTER_OFFSET)
    CONTENT_WIDTH = round(curses.COLS * 0.60)
    CONTENT_X, CONTENT_Y = round(curses.COLS * 0.15), 13
    content = win.subwin(
        CONTENT_HEIGHT,
        CONTENT_WIDTH,
        CONTENT_Y,
        CONTENT_X,
    )
    # win.addstr(f'cols = {str(curses.COLS)}, width = {str(curses.COLS - 31)}')
    # win.refresh()
    # content.bkgd(' ', curses.color_pair(2) | curses.A_BOLD)
    content.refresh()

    RIGHTMENU_HEIGHT = CONTENT_HEIGHT
    RIGHTMENU_WIDTH = round(curses.COLS * 0.2)
    RIGHTMENU_Y, RIGHTMENU_X = CONTENT_Y, CONTENT_X + CONTENT_WIDTH + 5
    right_menu = win.subwin(
        RIGHTMENU_HEIGHT,
        RIGHTMENU_WIDTH,
        RIGHTMENU_Y,
        RIGHTMENU_X,
    )
    # right_menu.bkgd(' ', curses.color_pair(2) | curses.A_BOLD)
    right_menu.refresh()

    # scapy verbose
    conf.verbose = 3
    conf.nofilter = 1
    conf.checkIPaddr = False

    # create an exit event for timer
    exit_e = threading.Event()

    # handler = ReconEngine(args, content, exit_e)

    # start timer
    start_time = time.time()
    start_timer(timer, exit_e)

    try:
        # initiate handler
        handler = ReconEngine(args, content, exit_e, right=right_menu)

        # run handler
        handler.run()
    except Exception as e:
        content.addstr(f"\n\n [+] Error occurred : {str(e)}")
        content.addstr(f"\n\n{traceback.format_exc()}")

        # log error into a file
        with open('error.txt', 'w') as f:
            f.write(traceback.format_exc())

        content.refresh()
    else:
        end_time = time.time()
        elapsed_time = end_time - start_time
        content.addstr(f"\n\n [+] Execution time : {elapsed_time} seconds.")
        content.refresh()

    # stop the timer
    if not exit_e.is_set():
        exit_e.set()

    content.addstr(f"\n\n [+] Please press <space_bar> to exit.")
    content.refresh()
    while True:
        ch = content.getch()
        if int(ch) == 32:
            break


if __name__ == "__main__":
    wrapper(main)