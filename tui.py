import curses
from comp import Color, ColorPair, Cursor, UIElement, UIContainer


class Label(UIElement):
    """ Text label.
    Args:
        text (str): Label text.
        *args: Argument list.
        **kwargs: Keyword argument list.
    """
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._text = None
        self.text = text

    @property
    def text(self):
        """ Get label text.
        Returns:
            str: Label text.
        """
        return self._text

    @text.setter
    def text(self, text):
        """ Set label text.
        Args:
            text (str): Label text.
        """
        self._text = text

        # Calculate label element size from suplied text.
        self.width = len(max(text.splitlines(keepends=True)))
        self.height = len(text.splitlines(keepends=True))

    def _render(self):
        """ Render label text.
        If text is multiline split it into separate lines and render with incremental y position.
        """
        for i, st in enumerate(self.text.splitlines(keepends=True)): 
            self._parent._cr.addstr(self.y + i, self.x, st)

        super()._render()


class TUI(UIContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        curses.wrapper(self._run)

    def _run(self, scr):
        self._cr = scr
        self.height, self.width = scr.getmaxyx()
        
        # Colors init area.
        if self.color is not None:
            curses.init_pair(self.color._number, self.color.fg, self.color.bg)
            self._cr.bkgd(curses.color_pair(self.color._number))

        self._cr.nodelay(True)
        self._cr.timeout(100)    # Key read timeout.

        # i = 0
        while(self._key != ord("q")):
            # Read key input.
            self._key = self._cr.getch()

            if self._key != curses.ERR:
                pass

            # self._ce.addstr(self.height - 3, 1, str(i))
            # self._ce.addstr(self.height - 2, 1, str(key))

            self._render()
            # i += 1
            # scr.noutrefresh()
            # curses.doupdate()
            # scr.refresh()


if __name__ == "__main__":
    tui = TUI(color=ColorPair(Color.BLACK, Color.BLUE), box=True)
    tui.add(Label("Short line.", y=5, x=8, cursor=Cursor(mode=Cursor.FREE)))
    tui.add(Label("Multiline\nhere.", y=7, x=8, cursor=Cursor(mode=Cursor.FREE)))
    tui.run()
