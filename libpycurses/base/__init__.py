#!/usr/bin/env python
# encoding: utf-8

import time
import curses
import curses.panel
import threading

__all__ = ["Panel", "ProgressSpin", "ProgressRotate"]

class Panel:
    """
    Panel is Window with 'Depth'
    Keep in mind you need to hold this object
    not this to be garbage collected.
    """
    def __init__(self,parentWindow):
        self = curses.panel.new_panel(parentWindow)

class ProgressSpin(threading.Thread):
    """

    >>>spin = ProgressSpin(parentWindow=stdscr)
    >>> # some thing to do
    >>>spin.stop()

    """

    def __init__(self, parentWindow,  y=None, x=None, chars=["|","/","-","\\"], delay=0.1, attr=None):
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
        self.chars=chars

    def run(self):
        self.running = True
        for ch in self.nextChar():
            if self.attr:
                self.parentWindow.addch(self.y, self.x, ch, self.attr) # Draw
            else:
                self.parentWindow.addch(self.y, self.x, ch) # Draw
            time.sleep( self.delay )
            self.parentWindow.refresh()

    def _infiniteChar(self):
        while True:
            for ch in self.chars:
                yield(ord(ch))

    def nextChar(self):
        for ch in self._infiniteChar():
            if self.running:
                yield ch
            else:
                return

    def stop(self):
        self.running = False
        self.parentWindow.addch(self.y, self.x, ord(" ")) # Clean Char
        self.parentWindow.refresh()
        self.join()

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

