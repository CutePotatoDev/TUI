import curses
import threading
from comp import UIElement, UIContainer


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
        self.width = len(max(text.splitlines(keepends=True), key=len))
        self.height = len(text.splitlines(keepends=True))

    def _render(self):
        """ Render label text.
        If text is multiline split it into separate lines and render with incremental y position.
        """
        for i, st in enumerate(self.text.splitlines(keepends=True)):
            self._parent._cr.addstr(self.y + i, self.x, st)

        return super()._render()


class TUI(UIContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._eventloops = []
        
    def loop(self, fun, *args):
        thr = threading.Thread(target=fun, args=args, daemon=True)
        self._eventloops.append(thr)

    def run(self):
        curses.wrapper(self._run)

    @property
    def initialized(self):
        return self._cr is not None

    def _run(self, scr):
        self.height, self.width = scr.getmaxyx()
        self._cr = scr
        self._parent = self

        for loop in self._eventloops:
            loop.start()

        # Colors init area.
        if self.color is not None:
            curses.init_pair(self.color._number, self.color.fg, self.color.bg)
            self._cr.bkgd(curses.color_pair(self.color._number))

        self._cr.nodelay(True)
        self._cr.timeout(100)    # Key read timeout.

        while(self._key != ord("q")):
            # Read key input.
            self._key = self._cr.getch()

            if self._key != curses.ERR:
                pass

            super()._render()
            # scr.noutrefresh()
            # curses.doupdate()
            # scr.refresh()
