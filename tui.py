import curses
from comp import Color, ColorPair, Cursor


class UIElement():
    """ Common class for all interface elements. """
    def __init__(self, y=0, x=0, height=0, width=0, color=None, cursor=None, box=False):
        self._ce = None
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        self.color = color
        self.cursor = cursor
        self._box = box

    @property
    def box(self):
        return self._box

    @box.setter
    def box(self, val):
        if self._box is False and self.cursor is not None:
            self.cursor.y += 1
            self.cursor.x += 1

        self._box = val

    def _render(self, key):
        if self.box:
            self._ce.box()

        # Set current element cursor.
        if self.cursor is not None:
            self.cursor._render(self, key)  # Render on current element.
        else:
            curses.curs_set(0)  # Hide cursor.


class TUI(UIElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        curses.wrapper(self._run)

    def _run(self, scr):
        self._ce = scr
        self.height, self.width = scr.getmaxyx()

        # Colors init area.
        if self.color is not None:
            curses.init_pair(self.color._number, self.color.fg, self.color.bg)
            self._ce.bkgd(curses.color_pair(self.color._number))

        self._ce.nodelay(True)
        self._ce.timeout(100)    # Key read timeout.

        key = None
        # i = 0
        while(key != ord("q")):
            # Read key input.
            key = self._ce.getch()

            if key != curses.ERR:
                pass

            # self._ce.addstr(self.height - 3, 1, str(i))
            # self._ce.addstr(self.height - 2, 1, str(key))

            self._render(key)
            # i += 1
            # scr.noutrefresh()
            # curses.doupdate()
            # scr.refresh()


if __name__ == "__main__":
    tui = TUI(color=ColorPair(Color.BLACK, Color.BLUE),
              cursor=Cursor(mode=Cursor.FREE))
    tui.run()
