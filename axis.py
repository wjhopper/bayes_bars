from psychopy.visual import ShapeStim, TextStim, BufferImageStim
from itertools import chain


def AxisStim(win, pos=(0, 0), width=1.5, height=1, y_labels=("A", "B")):

    # Boundaries in top, right, bottom, left order (like HTML/CSS)
    bounds = (pos[1]+height/2, pos[0]+width/2, pos[1]-height/2, pos[0]-width/2)

    y_axis = ShapeStim(win, vertices=[[bounds[3], bounds[2]], [bounds[3], bounds[2]+height/4],
                                      [bounds[3]-.025, bounds[2]+height/4], [bounds[3], bounds[2]+height/4],
                                      [bounds[3], bounds[0]-height/4], [bounds[3]-.025, bounds[0]-height/4],
                                      [bounds[3], bounds[0]-height/4], [bounds[3], bounds[0]]],
                       lineColor="#00000", lineWidth=3)

    x_axis_breaks = [round(bounds[3] + width * (x/10), 2) for x in range(1,11)]
    x_axis_break_vertices = list(zip(chain.from_iterable([[x, x, x] for x in x_axis_breaks]),
                                     [bounds[2], bounds[2]-.025, bounds[2]] * len(x_axis_breaks))
                                 )
    x_axis = ShapeStim(win, vertices=[(bounds[3], bounds[2])] + x_axis_break_vertices + [(bounds[1], bounds[2])],
                       lineColor="#00000", lineWidth=3, autoDraw=True)

    stimlist = [y_axis, x_axis]

    for label, pos in zip(y_labels, [bounds[0]-height/4, bounds[2]+height/4]):
        t = TextStim(win, label, pos=(bounds[3]-(.085*width), pos), height=height/15, color="#00000")
        stimlist.append(t)

    for i, pos in enumerate([bounds[3]] + x_axis_breaks):
        t = TextStim(win, f'{(i / len(x_axis_breaks)) * 100:.0f}%', pos=(pos, bounds[2]-.05), height=height/20, color="#00000")
        stimlist.append(t)

    x = BufferImageStim(win, stim=stimlist)
    # Width property will be useful for mapping bar length to probability (i.e., proportion of x axis it takes up)
    x.width = width
    x.height = height
    x.bounds = bounds
    x.autoDraw = True

    return x
