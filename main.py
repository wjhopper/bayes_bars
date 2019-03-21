from psychopy import visual, core, event
from itertools import chain
from AdjustableBar import AdjustableBar
win = visual.Window([1280, 768])
mouse = event.Mouse(win=win)
event.globalKeys.add(key='q', func=core.quit, name='shutdown')

y_axis = visual.ShapeStim(win, vertices=[[-.75, -.5], [-.75, -.25], [-.775, -.25], [-.75, -.25],
                                         [-.75, .25], [-.775, .25], [-.75, .25], [-.75, .5]],
                          lineColor="#00000", lineWidth=3, autoDraw=True)

x_axis_breaks = [round(.75*(x/5), 2) for x in range(-4, 6)]
x_axis_break_vertices = list(zip(chain.from_iterable([[x, x, x] for x in x_axis_breaks]),
                                 [-.5, -.525, -.5]*len(x_axis_breaks))
                             )
x_axis = visual.ShapeStim(win, vertices=[(-.75, -.5)] + x_axis_break_vertices + [(.75, -.5)],
                          lineColor="#00000", lineWidth=3, autoDraw=True)

for label, pos in zip(['A', 'B'], [.25, -.25]):
    t = visual.TextStim(win, label, pos=(-.8, pos), height=.1, color="#00000")
    t.autoDraw = True

for i, pos in enumerate([-.75] + x_axis_breaks):
    t = visual.TextStim(win, f'{(i/len(x_axis_breaks))*100:.0f}%', pos=(pos, -.55), height=.05, color="#00000")
    t.autoDraw = True


rect = AdjustableBar(win, pos=(-.75 + .75/2, .25), width=.75, height=.25,
                     lineColor="#000000", fillColor="#FF0000", lineWidth=3, autoDraw=True)

win.flip()

while True:
    if mouse.isPressedIn(rect.handle):
        rect.opacity = .2
        while mouse.getPressed()[0]:
            pos = mouse.getPos()[0]
            if -.75 < pos < .75:
                delta = pos - rect.handle.pos[0]
                rect.handle.pos = (pos, rect.handle.pos[1])
                rect.width = rect.width + delta
                rect.pos = (-.75 + rect.width/2, .25)
                win.flip()
        rect.opacity = 1
        win.flip()
