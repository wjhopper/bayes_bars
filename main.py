from psychopy import visual, core, event
from axis import AxisStim
from AdjustableBar import AdjustableBar


win = visual.Window([1280, 768])
mouse = event.Mouse(win=win)
event.globalKeys.add(key='q', func=core.quit, name='shutdown')

ax = AxisStim(win)  # autodraws

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
