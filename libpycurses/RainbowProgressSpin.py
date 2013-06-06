#!/usr/bin/env python
# encoding: utf-8

import curses
import time

from base import ProgressSpin

__author__ = "SYA-KE"
__version__ = ""
__date__ = "20130505"

class RainbowProgressSpin(ProgressSpin):
    """
    レインボーおおおおおおスピィィィン！
    ブラボオオオオヽ(`Д´)ﾉ

    >>>if curses.has_color():
    >>>    spin = RainbowProgressSpin(parentWindow=stdscr)
    >>>    spin.start()
    >>>    # some thing to do
    >>>    spin.stop()

    """

    def __init__(self, parentWindow, y=None, x=None, delay=0.2, bgColor=-1):
        """Initialize Spin

        This method only initialize the object.
        This will not call run() method.

        Args:
            parentWindow: A parent window to draw spin.
            y: A y-coordinate to draw spin.if None, upper side of the window.
            x: A x-coordinate to draw spin.if None, left side of the window.
            delay: A delay of alter the character in second.
            bgColor: A color of background of the spin. defaults null.

        """
        ProgressSpin.__init__(self,parentWindow=parentWindow, y=y, x=x, delay=delay)
        self.bgColor = bgColor

    def rainbow_colors(self):
        curses.start_color()
        curses.use_default_colors()
        for i in range(7):
            curses.init_pair(i,i,self.bgColor) # includes white
        while 1:
            for i in range(7):
                yield curses.color_pair(i)

    def run(self):
        self.running = True
        col = self.rainbow_colors()
        for ch in self.nextChar():
            colorPair = col.next()
            self.parentWindow.addch(self.y, self.x, ch, colorPair | curses.A_BOLD) # Draw
            time.sleep( self.delay )
            self.parentWindow.refresh()

if __name__=="__main__":
    import time
    def f(stdscr):
        win = stdscr
        win.leaveok(True)
        spin = RainbowProgressSpin(
            parentWindow=win,
            )
        spin.start()
        try:
            for i in range(5):
                win.addstr(0,3,"%s" % str(i))
                time.sleep(1)
            spin.stop()
            return 1
        except (KeyboardInterrupt, SystemExit):
            spin.stop()
            return -1
    curses.wrapper(f)
