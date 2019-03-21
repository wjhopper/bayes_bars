from psychopy.visual import ShapeStim, TextStim, BufferImageStim
from itertools import chain


def AxisStim(win, y_labels=('A', 'B')):

    y_axis = ShapeStim(win, vertices=[[-.75, -.5], [-.75, -.25], [-.775, -.25], [-.75, -.25],
                                      [-.75, .25], [-.775, .25], [-.75, .25], [-.75, .5]],
                       lineColor="#00000", lineWidth=3)

    x_axis_breaks = [round(.75 * (x / 5), 2) for x in range(-4, 6)]
    x_axis_break_vertices = list(zip(chain.from_iterable([[x, x, x] for x in x_axis_breaks]),
                                     [-.5, -.525, -.5] * len(x_axis_breaks))
                                 )
    x_axis = ShapeStim(win, vertices=[(-.75, -.5)] + x_axis_break_vertices + [(.75, -.5)],
                       lineColor="#00000", lineWidth=3, autoDraw=True)

    stimlist = [y_axis, x_axis]

    for label, pos in zip(y_labels, [.25, -.25]):
        t = TextStim(win, label, pos=(-.8, pos), height=.1, color="#00000")
        stimlist.append(t)

    for i, pos in enumerate([-.75] + x_axis_breaks):
        t = TextStim(win, f'{(i / len(x_axis_breaks)) * 100:.0f}%', pos=(pos, -.55), height=.05, color="#00000")
        stimlist.append(t)

    x = BufferImageStim(win, stim=stimlist)
    # Width property will be useful for mapping bar length to probability (i.e., proportion of x axis it takes up)
    x.width= 1.5  # -.75 to .75
    x.height = 1  # -.5 to .5

    x.autoDraw = True
    return x
