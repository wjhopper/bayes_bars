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

active_rects = []
activate_new = True
while True:
    # Activate (draw) bars on at a time
    if activate_new and rect_list:
        rect = rect_list.pop(0)
        rect.autoDraw = True
        rect.focused = True
        for r in active_rects:
            r.focused = False
        active_rects.append(rect)
        win.flip()

    activate_new = False
    # Loop looking for mouse clicks
    if mouse.getPressed()[0]:
        pos = mouse.getPos()

        # Focus bars via clicks (focused = draw the handle)
        for i in list(range(len(active_rects))):
            if active_rects[i].contains(pos):
                rect = active_rects[i]
                rect.focused = True
                for j in list(range(len(active_rects))):
                    if j != i:
                        active_rects[j].focused = False
                win.flip()

            if rect.handle.contains(pos) and rect.focused:
                rect.opacity = .2
                while mouse.getPressed()[0]:
                    drag_pos = mouse.getPos()[0]
                    if -.75 < drag_pos < .75:
                        delta = drag_pos - rect.handle.pos[0]
                        rect.handle.pos = (drag_pos, rect.handle.pos[1])
                        rect.width = rect.width + delta
                        rect.pos = (-.75 + rect.width/2, rect.pos[1])
                        win.flip()
                rect.opacity = 1
                activate_new = True
                win.flip()
