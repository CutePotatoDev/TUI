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
            UIElement: Parent element.
        """
        return self._parent

    def _render(self):
        """ Render element."""


class ElementsMatrix():
    """ Matrix array to contain UIContainer childs elements."""
    def __init__(self):
        self._elements = []  # List of elements.
        self._matrix = [[]]  # Matrix of elements with cursor.

    @property
    def lenY(self):
        """ Get length of y axis.
        Returns:
            int: y axis length.
        """
        return len(self._matrix[0]) - 1

    @property
    def lenX(self):
        """ Get length of x axis.
        Returns:
            int: x axis length.
        """
        return len(self._matrix) - 1

    def _sortY(self, elm):
        """ Y axis sort function.
        Args:
            elm (): Sort element.
        Returns:
            int: Sort value.
        """
        return elm[0]

    def _getColX(self, col):
        """ Get column X coordinate value.
        Args:
            col (list): Matrix column .
        Returns:
            int: X coordinate value.
        """
        try:
            return [e for e in col if len(e) > 1][0][1].x
        except IndexError:
            return -1

    def _sortX(self, elm):
        """ X axis sort function.
        Args:
            elm (list): Sort element.
        Returns:
            int: Sort value.
        """
        return self._getColX(elm)

    def add(self, elm):
        """ Add new element to matrix.
        Args:
            elm (UIElement): Element.
        """
        self._elements.append(elm)

        if elm.cursor is not None:
            # Check or new element x coordinate exist in in matrix.
            # If exists, just append column if not add new.
            for i, col in enumerate(self._matrix):
                if self._getColX(col) == elm.x:
                    x = i
                    break
            else:
                x = -1
                self._matrix.append(list(self._matrix[0]))

            # Equalize columns sizes.
            for i, col in enumerate(self._matrix):
                col.append((elm.y,))

            self._matrix[x][-1] = (elm.y, elm)  # Add element.

            # Sort matrix.
            self._matrix.sort(key=self._sortX)

            for col in self._matrix:
                col.sort(key=self._sortY)

    def getAllElements(self):
        """ Get all elements of matrix.
        Returns:
            list: Elements list.
        """
        return self._elements

    def get(self, y, x):
        """ Get element from matrix.
        Args:
            y (int): Element index on y axis.
            x (int): Element index on x axis.
        Returns:
            UIElement: Matrix element.
        """
        for i, row in enumerate(self._matrix[x]):
            if i == y - 1 and len(row) > 1:
                return row[1]


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
        self._box = False
        self.box = box

        self._cursorl = {"y": 0, "x": 0, "miny": 0, "minx": 0}
        self._childs = ElementsMatrix()

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
        """ Enable container borders box.
        Args:
            val (bool): Status value.
        """
        if self._box is False and self.cursor is not None:
            self.cursor.y += 1
            self.cursor.x += 1

        self._box = val

    def add(self, elm):
        """ Add new element to container.
        Args:
            elm (UIElement): Element to add.
        """
        if isinstance(elm, UIContainer) or not isinstance(elm, UIElement):
            raise ValueError("Expecting element type `UIElement`.")

        elm._parent = self
        self._childs.add(elm)

    def _render(self):
        """ Render container."""
        if self.box:
            self._cr.box()

        for child in self._childs.getAllElements():
            child._render()

        super()._render()

        status = None

        if self._cursorl["y"] == 0:
            # Render container cursor if it exists.
            if self.cursor is not None:
                status = self.cursor._render(self)
            else:
                self._cursorl = {"y": 1, "x": 1, "miny": 1, "minx": 1}
        else:
            if self._childs.lenX > 0:
                # Renders container child's cursors.
                element = self._childs.get(self._cursorl["y"], self._cursorl["x"])
                status = element.cursor._render(element)
            else:
                curses.curs_set(0)  # Or need hide cursor at all ??? And this place not best i guess.

        # Manage matrix coordinates.
        # Coordinates used to render needed cursor.
        if (status == Cursor.OVF_TOP
           and self._cursorl["y"] > self._cursorl["miny"]):
            if self._cursorl["y"] == 1:
                self._cursorl["x"] -= 1
            self._cursorl["y"] -= 1

        elif (status == Cursor.OVF_BOTTOM
              and self._cursorl["y"] < self._childs.lenX):
            if self._cursorl["y"] == 0:
                self._cursorl["x"] += 1
            self._cursorl["y"] += 1

        elif (status == Cursor.OVF_LEFT
              and self._cursorl["x"] > self._cursorl["minx"]):
            if self._cursorl["x"] == 1:
                self._cursorl["y"] = 0
            self._cursorl["x"] -= 1

        elif (status == Cursor.OVF_RIGHT
              and self._cursorl["x"] < self._childs.lenY):
            if self._cursorl["x"] == 0:
                self._cursorl["y"] += 1
            self._cursorl["x"] += 1


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

    # Overflow status. Indicating direction where overflow of cursor movement detected.
    OVF_LEFT = 0
    OVF_TOP = 1
    OVF_RIGHT = 2
    OVF_BOTTOM = 3

    def __init__(self, y=0, x=0, visible=True, mode=LINE):
        """ Constructor."""
        self.y = y
        self.x = x
        self.visible = visible
        self.mode = mode

    def _render(self, target):
        """ Rendering cursor.
        Args:
            target (UIElement): Target container element on which cursor be rendered.
        """
        key = target.parent.key
        status = None

        if self.visible is False:
            return status

        if isinstance(target, UIContainer):
            miny = 0 if target.box is False else 1
            maxy = target.height - 1 if target.box is False else target.height - 2
            minx = 0 if target.box is False else 1
            maxx = target.width - 1 if target.box is False else target.width - 2
        else:
            miny = minx = 0
            maxy = target.height - 1
            maxx = target.width - 1

        if key == curses.KEY_UP:
            if self.y > miny:
                if self.mode in [Cursor.LINE, Cursor.FREE]:
                    self.y -= 1
            else:
                status = Cursor.OVF_TOP
        elif key == curses.KEY_DOWN:
            if self.y < maxy:
                if self.mode in [Cursor.LINE, Cursor.FREE]:
                    self.y += 1
            else:
                status = Cursor.OVF_BOTTOM
        elif key == curses.KEY_LEFT:
            if self.x > minx:
                if self.mode in [Cursor.FREE]:
                    self.x -= 1
            else:
                status = Cursor.OVF_LEFT
        elif key == curses.KEY_RIGHT:
            if self.x < maxx:
                if self.mode in [Cursor.FREE]:
                    self.x += 1
            else:
                status = Cursor.OVF_RIGHT

        target.parent._cr.move(target.y + self.y, target.x + self.x)
        return status
