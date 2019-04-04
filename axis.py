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
                       lineColor="#00000", lineWidth=3)

    stimlist = [y_axis, x_axis]

    for label, p in zip(y_labels, [bounds[0]-height/4, bounds[2]+height/4]):
        t = TextStim(win, label, pos=(bounds[3]-(height/8), p), height=height/15, color="#00000", wrapWidth=.03)
        stimlist.append(t)

    for i, p in enumerate([bounds[3]] + x_axis_breaks):
        t = TextStim(win, f'{(i / len(x_axis_breaks)) * 100:.0f}%', pos=(p, bounds[2]-.05),
                     height=height/20, color="#00000")
        stimlist.append(t)

    # Determine the bounds of the axis taking into account all labels, ticks, titles, etc.
    # This is to help define a rectangle of the screen to capture
    # By capturing this region instead of the whole screen, we don't have to worry about making sure the axis
    # is drawn first. Otherwise, if it's drawn last (for example) it can occlude other stimuli with "background" pixels\

    # Leave this here for now while I track https://github.com/psychopy/psychopy/issues/2381
    # top = max([max(s.verticesPix[:, 1]) for s in stimlist]) + 2
    # right = max([max(s.verticesPix[:, 0]) for s in stimlist]) + 2
    # bottom = min([min(s.verticesPix[:, 1]) for s in stimlist]) + 2
    # left = min([min(s.verticesPix[:, 0]) for s in stimlist]) + 2
    # capture_rect = [left/win.size[0]/2, top/win.size[1]/2, right/win.size[0]/2, bottom/win.size[1]/2]

    # The capturing rectangle is really really confusing (I think there is an implemenation bug, not just documentation)
    # Basically the docs says you should give a list of edges in [left top right bottom] order in norm coordinates
    # But the order that actually makes it work is [left bottom right top]
    # If you have these edges already you also have to change the sign, to make a "bottom" coordinate into a "top"!
    # Not sure what will happen if both edges start off positive, or both start off negative?
    capture_rect = [bounds[3]-.23, -bounds[2]+.1, bounds[1]+.04, -bounds[0]]

    # The positioning of the screenshot is also borked.
    # Basically the BufferImageStim is specified in pixels units, and never gets re-scaled into the units of the window
    # it's drawn to to. Don't know why not, works fine with ImageStim.
    # To work around this, we have to take our normalized coordinates and divide them by half the screen width
    # That way, when BufferImageStim converts them to pixels (by multiplying by half the screen width) it will leave us
    # with the "desired" norm coordinates. Yikes.
    x = BufferImageStim(win, stim=stimlist, rect=capture_rect,
                        pos=(pos[0]/win.size[0]/2, pos[1]/win.size[1]/2)
                        )
    x.events = y_labels
    x.width = width
    x.height = height
    # These adjustments to the bounds are because the screenshot rectangle is asymmetric around the origin.
    # When the screenshot is centered, the bar positions need to be adjusted by half of the asymmetry in order to begin
    # on the y-axis line. Also we need to add one pixel to the "starting" (left) boundary because of some subpixel
    # misalignment in the screenshot.
    # The drawback to this whole thing is that the axis itself is not centered, but rather the screenshot of the axis
    # (i.e., the axis plus it's labels plus small margin) are centered.
    one_px_proportions = (1/win.size[0], 1/win.size[1])
    x.bounds = [bounds[0]+.05, bounds[1], bounds[2] + .05, bounds[3] + (.23/2) - (.04/2) + 2*one_px_proportions[0]]
    x.autoDraw = True

    return x
