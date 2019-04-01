from psychopy.visual.rect import Rect
from psychopy.visual.ratingscale import RatingScale
from psychopy.visual.slider import Slider
from psychopy.visual.text import TextStim
from psychopy import event


def static_trial(axis, problem_text, pA=0.5, pB_given_A=0.5, pB_given_notA=0.5):

    for p in [pA, pB_given_A, pB_given_notA]:
        if not 0 <= p <= 1:
            raise ValueError("All probabilities parameters must be between 0 and 1")

    win = axis.win
    problem_textstim = TextStim(win, text="\n".join(problem_text).format(pA=pA,
                                                                         pB_given_A=pB_given_A,
                                                                         pB_given_notA=pB_given_notA
                                                                         ),
                                pos=(0, .85), height=.075, wrapWidth=1.5)
    problem_textstim.autoDraw = True

    bars = {"A_major": Rect(win,
                            pos=(axis.bounds[3] + axis.width / 4, axis.bounds[0] - axis.height / 4),
                            width=axis.width * pA, height=axis.height / 4,
                            lineColor="#000000", fillColor="#000000", lineWidth=3,
                            name="A_major", autoDraw=True),
            "notA_major": Rect(win,
                               pos=(axis.bounds[3] + axis.width / 4, axis.bounds[2] + axis.height / 4),
                               width=axis.width * (1 - pA), height=axis.height / 4,
                               lineColor="#000000", fillColor="#0000FF", lineWidth=3,
                               name="B_major", autoDraw=True),
            "A_minor": Rect(win,
                            pos=(axis.bounds[3] + axis.width / 8, axis.bounds[0] - axis.height / 4),
                            width=axis.width * pA * pB_given_A, height=axis.height / 4,
                            lineColor="#000000", fillColor="#f9f50c", lineWidth=3,
                            name="A_minor", autoDraw=True),
            "notA_minor": Rect(win,
                               pos=(axis.bounds[3] + axis.width / 8, axis.bounds[2] + axis.height / 4),
                               width=axis.width * (1 - pA) * pB_given_notA, height=axis.height / 4,
                               lineColor="#000000", fillColor="#FF0000", lineWidth=3,
                               name="B_minor", autoDraw=True)
            }

    more_likely_prompt = TextStim(win, pos=(-.6, -.6), text="Which is more likely?", height=.06, color='#FFFFFF')
    more_likely_prompt.autoDraw = True
    more_likely_scale = RatingScale(win, pos=(-.6, -.7), choices=['Eats Cookies', "Doesn't Eat Cookies"],
                                    markerStart=0.5, textSize=1.25, size=.6,
                                    textColor='#FFFFFF', lineColor="#000000", showAccept=False
                                    )

    times_likely_prompt = TextStim(win, pos=(.3, -.6), text="How many times more likely?", height=.06, color='#FFFFFF')
    times_likely_prompt.autoDraw = True
    times_likely_scale = Slider(win, pos=(.3, -.7), ticks=[1] + list(range(5, 51, 5)),
                                granularity=.1, style="marker")
    times_likely_scale.markerPos = 1
    times_likely_scale.rating = 1
    times_likely_scale.marker.size = (times_likely_scale._tickL / 5,
                                      times_likely_scale._tickL / 5 * (win.size[0] / win.size[1])
                                      )
    times_likely_resp = TextStim(win, pos=(.3, -.8), text="1x", height=.06, color='#FFFFFF')
    times_likely_resp.autoDraw = True

    accept_box = Rect(win, pos=(0, -.9), height=.1, width=.25, autoDraw=True, lineColor="DarkGray")
    accept_text = TextStim(win, text="Accept", pos=(0, -.9), height=.06, color="DarkGray")

    mouse = event.Mouse()
    while True:
        if more_likely_scale.markerPlacedBySubject and accept_box.lineColor == "DarkGray":
            accept_box.lineColor = "#FFFFFF"
            accept_text.color = "#FFFFFF"
        if mouse.isPressedIn(accept_box) and more_likely_scale.markerPlacedBySubject:
            break
        more_likely_scale.draw()
        times_likely_scale.draw()
        times_likely_resp.text = str(times_likely_scale.markerPos) + "x"
        accept_text.draw()
        win.flip()

    problem_textstim.autoDraw = False
    more_likely_prompt.autoDraw = False
    times_likely_prompt.autoDraw = False
    times_likely_resp.autoDraw = False
    accept_box.autoDraw = False
    for b in bars.values():
        b.autoDraw=False

    return [more_likely_scale.getRating(), times_likely_scale.getRating()]
