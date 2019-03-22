from psychopy import visual, core, event
from axis import AxisStim
from AdjustableBar import AdjustableBar


win = visual.Window([1280, 768])
mouse = event.Mouse(win=win)
event.globalKeys.add(key='q', func=core.quit, name='shutdown')

ax = AxisStim(win)  # autodraws

bars = {"A_major": AdjustableBar(win, bounds=(-.75, .75), pos=(-.75 + .75 / 2, .25), width=.75, height=.25,
                                 lineColor="#000000", fillColor="#000000", lineWidth=3,
                                 name="A_major", focused=False),
        "B_major": AdjustableBar(win, bounds=(-.75, .75), pos=(-.75 + .75/2, -.25), width=.75, height=.25,
                                 lineColor="#000000", fillColor="#0000FF", lineWidth=3,
                                 name="B_major", focused=False),
        "A_minor": AdjustableBar(win, bounds=(-.75, 0), pos=(-.75 + .75/4, .25), width=.75/2, height=.25,
                                 lineColor="#000000", fillColor="#f9f50c", lineWidth=3,
                                 name="A_minor", focused=False),
        "B_minor": AdjustableBar(win, bounds=(-.75, 0), pos=(-.75 + .75 / 4, -.25), width=.75/2, height=.25,
                                 lineColor="#000000", fillColor="#FF0000", lineWidth=3,
                                 name="B_minor", focused=False)
        }
names = list(bars.keys())  # use this to keep track of what bars we need to add
rect = bars[names[0]]
names = names[1:]
rect.autoDraw = True
rect.focused = True  # Needs to be set after autodraw to make sure handle is drawn on top of bar
active_rects = [rect]
win.flip()

while True:
    # Activate (draw) bars one at a time
    if all([x.adjusted for x in active_rects]) and names:
        rect = bars[names[0]]
        names = names[1:]
        rect.autoDraw = True
        rect.focused = True # Needs to be set after autodraw to make sure handle is drawn on top of bar
        for r in active_rects:
            r.focused = False
        active_rects.append(rect)
        win.flip()

    # Loop looking for mouse clicks
    if mouse.getPressed()[0]:
        pos = mouse.getPos()

        # Focus bars via clicks as long as no handles are clicked (focused = draw the handle)
        clicked_handles = [x for x in active_rects if x.handle.contains(pos) and x.focused]
        if any(clicked_handles):
            clicked_bars = []
        else:
            clicked_bars = [x for x in active_rects if x.contains(pos)]

        if len(clicked_bars) == 1:
            rect = clicked_bars[0]
        elif len(clicked_bars) > 1:
            rect = clicked_bars[-1]

        if clicked_bars:
            rect.focused = True
            for j in active_rects:
                if j is not rect:
                    j.focused = False
            win.flip()

        if rect.handle.contains(pos) and rect.focused:
            rect.opacity = .2
            rect.adjusted = True
            prefix = rect.name.split("_")[0]
            while mouse.getPressed()[0]:
                drag_pos = mouse.getPos()[0]
                if rect.bounds[0] < drag_pos < rect.bounds[1]:
                    delta = drag_pos - rect.handle.pos[0]
                    rect.handle.pos = (drag_pos, rect.handle.pos[1])
                    rect.width = rect.width + delta
                    rect.pos = (-.75 + rect.width/2, rect.pos[1])
                    win.flip()

            rect.opacity = 1
            win.flip()

            if "major" in rect.name:
                minor_bar = bars[prefix + "_minor"]
                minor_bar.bounds = (-.75, rect.pos[0] + rect.width / 2)
                if minor_bar not in active_rects:
                    minor_bar.width = rect.width / 2 # width must be updated before pos! pos triggers moving of handle
                    minor_bar.pos = (-.75 + rect.width / 4, minor_bar.pos[1])
            if "minor" in rect.name:
                bars[prefix + "_major"].bounds = (rect.pos[0] + rect.width / 2, .75)
