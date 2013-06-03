import curses.panel

class Panel:
    """
    Panel is Window with 'Depth'
    Keep in mind you need to hold this object
    not this to be garbage collected.
    """
    X = 0
    Y = 0
    def __init__(self,parentWindow):
        self = curses.panel.new_panel(parentWindow)

if __name__ == "__main__":
    pass
