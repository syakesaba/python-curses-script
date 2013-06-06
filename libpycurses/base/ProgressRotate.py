#!/usr/bin/env python
# encoding: utf-8

import time
from threading import Thread
from ProgressSpin import ProgressSpin

__author__ = "SYA-KE"
__version__ = ""
__date__ = "20130505"

class ProgressRotate(ProgressSpin):
    """

    >>>rotate = ProgressRotate(parentWindow=stdscr)
    >>> # some thing to do
    >>>rotate.stop()

    """
    def __init__(self, parentWindow, y=None, x=None, chars=["/","\\"], delay=0.1, attr=None):
        """Initialize Spin

        This method only initialize the object.
        This will not call run() method.

        Args:
            parentWindow: A parent window to draw.
            y: A y-coordinate to draw.if None, upper side of the window.
            x: A x-coordinate to draw.if None, left side of the window.
            chars: Characters written per a rotation
            delay: A delay of alter the character in second.
            attr: A attribute.

        """
        ProgressSpin.__init__(self, parentWindow, y=y, x=x, chars=chars, delay=delay, attr=attr)

    def rotate(self):
        """
        yields 2x2 rotating location
        """
        while True:
            yield 0,0
            yield 0,1
            yield 1,1
            yield 1,0

    def run(self):
        self.running = True
        if self.attr:
            def f(y,x,ch):
                self.parentWindow.addch(y, x, ch, self.attr) # Draw
        else:
            def f(y,x,ch):
                self.parentWindow.addch(y, x, ch) # Draw
        genRot = self.rotate()
        for ch in self.nextChar():
            posY,posX = genRot.next()
            x = self.x + posX
            y = self.y + posY
            f(y,x,ch)
            self.parentWindow.refresh()
            time.sleep(self.delay)
            self.parentWindow.addch(y, x, ord(" "))

if __name__=="__main__":
    import curses
    import time
    def f(stdscr):
        win = stdscr
        win.leaveok(True)
        rot = ProgressRotate(
            win,
            y=win.getmaxyx()[0]/2,
            x=win.getmaxyx()[1]/2,
            chars=["/","\\"],
            delay=0.2,
            attr=curses.A_REVERSE,
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
