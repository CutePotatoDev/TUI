import curses
import time
import random


class Color():
    BLACK = curses.COLOR_BLACK
    RED = curses.COLOR_RED
    GREEN = curses.COLOR_GREEN
    YELLOW = curses.COLOR_YELLOW
    BLUE = curses.COLOR_BLUE
    MAGENTA = curses.COLOR_MAGENTA
    CYAN = curses.COLOR_CYAN
    WHITE = curses.COLOR_WHITE


class ColorPair():
    """ Hold UI color pair.
    Keyword arguments:
        fg -- Foreground color.
        bg -- Background color.
    """
    _TAKENIDS = []

    def __new__(cls, *args, **kwargs):
        # Create unique color pair name related with color pair object.
        if len(cls._TAKENIDS) >= 63:
            raise RuntimeError("Can't create more than 64 different color objects.")

        obj = object.__new__(cls)

        while True:
            obj._number = random.randint(1, 63)
            if obj._number not in cls._TAKENIDS:
                cls._TAKENIDS.append(obj._number)
                break

        return obj

    def __del__(self):
        ColorPair._TAKENIDS.remove(self._number)

    def __init__(self, fg=0, bg=0):
        self.fg = fg
        self.bg = bg


class UIElement():
    """ Common class for all interface elements. """
    def __init__(self, y=0, x=0, height=0, width=0, color=None):
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        self.color = color


class TUI(UIElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        curses.wrapper(self._run)

    def _run(self, scr):
        # Colors init area.
        if self.color is not None:
            curses.init_pair(self.color._number, self.color.fg, self.color.bg)
            scr.bkgd(curses.color_pair(self.color._number))

        scr.nodelay(True)

        scr.refresh()
        key = None
        while(key != ord("q")):
            # Read key input.
            key = scr.getch()

            if key != curses.ERR:
                pass
            time.sleep(0.05)


if __name__ == "__main__":
    tui = TUI(color=ColorPair(Color.MAGENTA, Color.BLUE))
    tui.run()
