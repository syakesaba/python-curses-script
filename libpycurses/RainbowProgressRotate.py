#!/usr/bin/env python
# encoding: utf-8

import curses
from threading import Thread

from base import ProgressRotate

__author__ = "SYA-KE"
__version__ = ""
__date__ = "20130505"

class RainbowProgressRotate(ProgressRotate):
    """
    レインボオオオオオオウヽ(`Д´)ﾉ
    ウォォォォン！

    >>>rotate = RainbowProgressRotate(parentWindow=stdscr)
    >>> # some thing to do
    >>>rotate.stop()

    """
    def __init__(self, parentWindow, y=None, x=None, chars=["/","\\"], delay=0.1, fgColor=None):
        """Initialization

        This method only initialize the object.
        This will not call run() method.

        Args:
            parentWindow: A parent window to draw.
            y: A y-coordinate to draw.if None, upper side of the window.
            x: A x-coordinate to draw.if None, left side of the window.
            chars: Characters written per a rotation
            delay: A delay of alter the character in second.
            fgColor: A attribute.

        """

        if fgColor is not None:
            self.fgColor = fsColor
        else:
            self.fgColor = -1
        ProgressRotate.__init__(self, parentWindow, y=y, x=x, chars=chars, delay=delay, attr=curses.A_BOLD)

    def rainbow_colors(self):
        curses.start_color()
        curses.use_default_colors()
        for i in range(7):
            curses.init_pair(i,self.fgColor,i) # INCLUDES BLACK COLOR
        while 1:
            for i in range(7):
                yield curses.color_pair(i)

    def nextChar(self):
        genColor = self.rainbow_colors()
        for ch in self._infiniteChar():
            self.attr = genColor.next()
            if self.running:
                yield ch
            else:
                return

if __name__=="__main__":
    import curses
    import time
    def f(stdscr):
        win = stdscr
        win.leaveok(True)
        rot = RainbowProgressRotate(
            win,
            y=win.getmaxyx()[0]/2,
            x=win.getmaxyx()[1]/2,
            chars=[" "],
            delay=0.1,
            fgColor = None
            )
        rot.start()
        try:
            for i in range(5):
                win.addstr(i,i,"%s" % str(i))
                time.sleep(1)
            rot.stop()
            time.sleep(2)
            return 1
        except (KeyboardInterrupt, SystemExit):
            rot.stop()
            time.sleep(2)
            return -1
    curses.wrapper(f)
