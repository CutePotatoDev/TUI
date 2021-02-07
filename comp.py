import curses
import random


class Color():
    """ Predefined TUI colors list."""
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
    Args:
        fg (int, optional): Foreground color id, defaults to 0.
        bg (int, optional): Background color id, defaults to 0.
    """
    _TAKENIDS = []

    def __new__(cls, *args, **kwargs):
        """ On object creation generate unique id which be used as name of color pair.
        Returns:
            Created object instance.
        Raises:
            RuntimeError: If amount of created objects exceeds allowed amount.
        """
        # Create unique color pair name related with color pair object.
        if len(cls._TAKENIDS) >= 63:
            raise RuntimeError(
                "Can't create more than 64 different color objects.")

        obj = object.__new__(cls)

        while True:
            obj._number = random.randint(1, 63)
            if obj._number not in cls._TAKENIDS:
                cls._TAKENIDS.append(obj._number)
                break

        return obj

    def __del__(self):
        """ Remove color number from list on object destruction."""
        ColorPair._TAKENIDS.remove(self._number)

    def __init__(self, fg=0, bg=0):
        """ Constructor."""
        self.fg = fg
        self.bg = bg


class Cursor():
    """ Cursor object.
    Args:
        y (int, optional): Cursor y coordinate, defaults to 0.
        x (int, optional): Cursor x coordinate, defaults to 0.
        visible (int, optional): Cursor visibility, defaults to True.
        mode (Cursor, optional): Cursor display mode, defaults to Cursor.LINE.
    """
    LINE = 0
    FREE = 1
    POINT = 2

    def __init__(self, y=0, x=0, visible=True, mode=LINE):
        """ Constructor."""
        self.y = y
        self.x = x
        self.visible = visible
        self.mode = mode

    def _render(self, target, key):
        """ Rendering cursor.
        Args:
            target (UIElement): Target element on which cursor be rendered.
            key (int): Keyboard key value.
        """

        miny = 0 if target.box is False else 1
        maxy = target.height - 1 if target.box is False else target.height - 2
        minx = 0 if target.box is False else 1
        maxx = target.width - 1 if target.box is False else target.width - 2

        if key == curses.KEY_UP and self.y > miny:
            if self.mode in [Cursor.LINE, Cursor.FREE]:
                self.y -= 1
        elif key == curses.KEY_DOWN and self.y < maxy:
            if self.mode in [Cursor.LINE, Cursor.FREE]:
                self.y += 1
        elif key == curses.KEY_LEFT and self.x > minx:
            if self.mode in [Cursor.FREE]:
                self.x -= 1
        elif key == curses.KEY_RIGHT and self.x < maxx:
            if self.mode in [Cursor.FREE]:
                self.x += 1

        target._ce.move(target.y + self.y, target.x + self.x)
