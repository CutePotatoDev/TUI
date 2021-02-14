import curses
import random


class UIElement():
    """ Common class for all interface elements.
    Args:
        y (int, optional): Element y coordinate.
        x (int, optional): Element x coordinate.
        height (int, optional): Element height.
        width (int, optional): Element width.
        color: (ColorPair, optional): Element color pair.
        cursor: (Cursor, optional): Element related cursor.
    """
    def __init__(self, y=0, x=0, height=0, width=0, color=None, cursor=None):
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        self.color = color
        self.cursor = cursor
        self._parent = None

    @property
    def parent(self):
        """ Get parent element.
        Returns:
            UIElemet: Parent element.
        """
        return self._parent

    def _render(self):
        """ Render element cursor."""
        # Set element cursor.
        if self.cursor is not None:
            self.cursor._render(self)  # Render on current element.


class UIContainer(UIElement):
    """ Common class for interface container elements.
    Args:
        *args: Argument list.
        box (bool, optional): Enable container box frame.
        **kwargs: Keyword arguments list. 
    """
    def __init__(self, *args, box=False, **kwargs):
        """ Constructor."""
        super().__init__(*args, **kwargs)

        self._cr = None
        self._key = None
        self._box = box

        self._childs = []

    @property
    def key(self):
        """ Get pressed key value.
        Returns:
            int: Key value.
        """
        return self._key

    @property
    def box(self):
        """ Get container box frame status.
        Returns:
            bool: Frame status.
        """
        return self._box

    @box.setter
    def box(self, val):
        if self._box is False and self.cursor is not None:
            self.cursor.y += 1
            self.cursor.x += 1
    
        self._box = val

    def add(self, elm):
        if isinstance(elm, UIContainer) or not isinstance(elm, UIElement):
            raise ValueError("Expecting element type `UIElement`.")

        elm._parent = self
        self._childs.append(elm)

    def _render(self):
        """ Render container."""
        if self.box:
            self._cr.box()

        for child in self._childs:
            child._render()

        super()._render()


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

    def _render(self, target):
        """ Rendering cursor.
        Args:
            taret (UIElement): Target container element on which cursor be rendered.
        """
        key = target.parent.key
        
        if isinstance(target, UIContainer):
            miny = 0 if target.box is False else 1
            maxy = target.height - 1 if target.box is False else target.height - 2
            minx = 0 if target.box is False else 1
            maxx = target.width - 1 if target.box is False else target.width - 2
        else:
            miny = minx = 0
            maxy = target.height - 1
            maxx = target.width - 1
            
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

        target.parent._cr.move(target.y + self.y, target.x + self.x)
