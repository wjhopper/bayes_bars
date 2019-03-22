from psychopy.visual.rect import Rect


class AdjustableBar(Rect):
    def __init__(self, win, bounds=(-1, 1), **kwargs):
        # Initialize the rectangle
        super(AdjustableBar, self).__init__(win, **kwargs)
        # Create the "handle" point
        self.handle = Rect(win, pos=(-.75 + self.width, self.pos[1]), width=.015, height=.015 * (win.size[0]/win.size[1]),
                           lineColor="#000000", fillColor="#0000FF", lineWidth=1, autoDraw=True)
        self._focused = True
        self.adjusted = False
        self._bounds = bounds

    @property
    def focused(self):
        return self._focused

    @focused.setter
    def focused(self, isFocused):
        if isFocused != self._focused:
            self._focused = isFocused
            self.handle.autoDraw = isFocused

    @property
    def bounds(self):
        return self._bounds

    @bounds.setter
    def bounds(self, new_bounds):

        if len(new_bounds) != 2:
            raise ValueError("AdjustableBar boundaries must have 2 values")

        for x in new_bounds:
            if not isinstance(x, (int, float)):
                raise ValueError("AdjustableBar boundaries must be a list or tuple of numeric values")

        if isinstance(new_bounds, list):
            new_bounds = tuple(new_bounds)

        self._bounds = new_bounds
