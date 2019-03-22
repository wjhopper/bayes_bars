from psychopy.visual.rect import Rect


class AdjustableBar(Rect):
    def __init__(self, win, **kwargs):
        # Initialize the rectangle
        super(AdjustableBar, self).__init__(win, **kwargs)
        # Create the "handle" point
        self.handle = Rect(win, pos=(-.75 + self.width, self.pos[1]), width=.015, height=.015 * (win.size[0]/win.size[1]),
                           lineColor="#000000", fillColor="#0000FF", lineWidth=1, autoDraw=True)
        self._focused = True
        self.adjusted = False

    @property
    def focused(self):
        return self._focused

    @focused.setter
    def focused(self, isFocused):
        if isFocused != self._focused:
            self._focused = isFocused
            self.handle.autoDraw = isFocused
