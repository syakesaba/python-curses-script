#!/usr/bin/env python
# encoding: utf-8

import time
from threading import Thread

__author__ = "SYA-KE"
__version__ = ""
__date__ = "20130505"

class ProgressSpin(Thread):
    """

    >>>spin = ProgressSpin(parentWindow=stdscr)
    >>> # some thing to do
    >>>spin.stop()

    """

    def __init__(self, parentWindow, y=None, x=None, delay=0.1, attr=None):
        """Initialize Spin

        This method only initialize the object.
        This will not call run() method.

        Args:
            parentWindow: A parent window to draw spin.
            y: A y-coordinate to draw spin.if None, upper side of the window.
            x: A x-coordinate to draw spin.if None, left side of the window.
            delay: A delay of alter the character in second.
            attr: A attribute of the spin.

        """
        Thread.__init__(self)
        self.parentWindow = parentWindow

        if x is None:
            self.x = self.parentWindow.getbegyx()[1]
        else:
            self.x = x
        if y is None:
            self.y = self.parentWindow.getbegyx()[0]
        else:
            self.y = y
        self.delay = delay
        self.attr = attr

    def run(self):
        self.running = True
        for ch in self.nextChar():
            if self.attr:
                self.parentWindow.addch(self.y, self.x, ch, attr=self.attr) # Draw
            else:
                self.parentWindow.addch(self.y, self.x, ch) # Draw
            time.sleep( self.delay )
            self.parentWindow.refresh()

    def nextChar(self):
        def infiniteChar():
            while True:
                yield ord("\\")
                yield ord("|")
                yield ord("/")
                yield ord("-")
        for ch in infiniteChar():
            if self.running:
                yield ch
            else:
                return

    def stop(self):
        self.running = False
        self.parentWindow.delch(self.y, self.x) # Clean Char
        self.join()

if __name__=="__main__":
    import curses
    import time
    def f(stdscr):
        win = stdscr
        win.leaveok(True)
        spin = ProgressSpin(
            parentWindow=win,
            y=win.getmaxyx()[0]/2,
            x=win.getmaxyx()[1]/2,
            delay=0.2,
            attr=None,
            )
        spin.start()
        try:
            for i in range(5):
                win.addstr(i,i,"%s" % str(i))
                time.sleep(1)
            spin.stop()
            return 1
        except (KeyboardInterrupt, SystemExit):
            spin.stop()
            return -1
    curses.wrapper(f)
