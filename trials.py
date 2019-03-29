from psychopy.visual.rect import Rect
from psychopy.visual.ratingscale import RatingScale
from psychopy.visual.text import TextStim


def static_trial(axis, pA=0.5, pB_given_A=0.5, pB_given_notA=0.5):

    for p in [pA, pB_given_A, pB_given_notA]:
        if not 0 <= p <= 1:
            raise ValueError("All probabilities parameters must be between 0 and 1")

    win = axis.win
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

    prompt = TextStim(win, pos=(0, -.6), text = "Which is more likely?", height=.05)
    prompt.autoDraw = True
    rating_scale = RatingScale(win, pos=(0, -.7), choices=['Eats Cookies', "Doesn't Eat Cookies"],
                               markerStart=0.5, singleClick=True, textSize=.75)
    while rating_scale.noResponse:
        rating_scale.draw()
        win.flip()
    return bars
