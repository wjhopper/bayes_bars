from psychopy import visual, core, event
from axis import AxisStim
from AdjustableBar import AdjustableBar


win = visual.Window([1280, 768])
mouse = event.Mouse(win=win)
event.globalKeys.add(key='q', func=core.quit, name='shutdown')

ax = AxisStim(win)  # autodraws

rect_list = []
for x in zip([.75, .75, .75/2, .75/2], [.25, -.25, .25, -.25], ["#000000", "#0000FF", "#f9f50c", "#FF0000"]):
    rect = AdjustableBar(win, pos=(-.75 + x[0]/2, x[1]), width=x[0], height=.25,
                         lineColor="#000000", fillColor=x[2], lineWidth=3)
    rect.focused = False
    rect_list.append(rect)

win.flip()

rect = rect_list.pop(0)
rect.autoDraw = True
rect.focused = True
active_rects = [rect]
win.flip()

while True:
    # Activate (draw) bars one at a time
    if all([x.adjusted for x in active_rects]) and rect_list:
        rect = rect_list.pop(0)
        rect.autoDraw = True
        rect.focused = True
        for r in active_rects:
            r.focused = False
        active_rects.append(rect)
        win.flip()

    # Loop looking for mouse clicks
    if mouse.getPressed()[0]:
        pos = mouse.getPos()

        # Focus bars via clicks (focused = draw the handle)
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
            while mouse.getPressed()[0]:
                drag_pos = mouse.getPos()[0]
                if -.75 < drag_pos < .75:
                    delta = drag_pos - rect.handle.pos[0]
                    rect.handle.pos = (drag_pos, rect.handle.pos[1])
                    rect.width = rect.width + delta
                    rect.pos = (-.75 + rect.width/2, rect.pos[1])
                    win.flip()
            rect.opacity = 1
            win.flip()
