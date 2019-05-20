from psychopy.visual.window import Window
from psychopy.visual.rect import Rect
from psychopy.visual.ratingscale import RatingScale
from psychopy.visual.slider import Slider
from psychopy.visual.text import TextStim
from psychopy import event
from AdjustableBar import AdjustableBar
from pandas import DataFrame
from axis import AxisStim


def static_trial(axis, problem_text, pA=0.5, pB_given_A=0.5, pB_given_notA=0.5):
    """
    Barplot showing the implied joint probability distribution of two discrete events. Participant must respond with
    whether an event A or not-A is more likely, and rate how many times more likely the chosen event is.

    :param axis: The xy axis where the bars are drawn. Created with AxisStim function.
    :param problem_text: A list of 3 string objects. Each string object should contain 1 str.format code where a
      floating point number is to be inserted
    :type problem_text: list of str
    :param pA: The probability of an event A
    :type pA: float
    :param pB_given_A: The probability of an event B given event A is observed
    :type pB_given_A: float
    :param pB_given_notA: The probability of an event B given the converse of event A has been observed.
    :type pB_given_notA: float
    :return: A dict with two elements holding the ratings given by the participant. The 'more_likely' element gives the
      name of the event  rated more likely by the participant. The 'times_likely' element gives the odds ratio in favor
      of the event rated more likely.
    :rtype: dict[str, float]
    """
    validate_probabilities(pA, pB_given_A, pB_given_notA)

    win = axis.win
    problem_textstim = create_problem_textstim(win, problem_text, pA, pB_given_A, pB_given_notA)

    bars = {"A_major": Rect(win,
                            pos=(axis.bounds[3] + axis.width * pA / 2,
                                 axis.bounds[0] - axis.height / 4),
                            width=axis.width * pA, height=axis.height / 4,
                            lineColor="#000000", fillColor="#000000", lineWidth=3,
                            name="A_major", autoDraw=True),
            "notA_major": Rect(win,
                               pos=(axis.bounds[3] + axis.width * (1-pA) / 2,
                                    axis.bounds[2] + axis.height / 4),
                               width=axis.width * (1 - pA), height=axis.height / 4,
                               lineColor="#000000", fillColor="#0000FF", lineWidth=3,
                               name="B_major", autoDraw=True),
            "A_minor": Rect(win,
                            pos=(axis.bounds[3] + (axis.width * pA * pB_given_A) / 2,
                                 axis.bounds[0] - axis.height / 4),
                            width=axis.width * pA * pB_given_A, height=axis.height / 4,
                            lineColor="#000000", fillColor="#f9f50c", lineWidth=3,
                            name="A_minor", autoDraw=True),
            "notA_minor": Rect(win,
                               pos=(axis.bounds[3] + (axis.width * (1-pA) * pB_given_notA) / 2,
                                    axis.bounds[2] + axis.height / 4),
                               width=axis.width * (1 - pA) * pB_given_notA, height=axis.height / 4,
                               lineColor="#000000", fillColor="#f9f50c", lineWidth=3,
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
                                granularity=.5, style="marker")
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
        b.autoDraw = False

    return {'more_likely': more_likely_scale.getRating(),
            'times_likely': times_likely_scale.getRating()
            }


def dynamic_trial(axis, problem_text, pA=0.5, pB_given_A=0.5, pB_given_notA=0.5):
    """
    Barplot that the participant may adjust with the mouse to show the implied joint probability distribution of two
    discrete events. Participant must respond with whether an event A or not-A is more likely, and rate how many
    times more likely the chosen event is.

    :param axis: The xy axis where the bars are drawn. Created with AxisStim function.
    :param list[str] problem_text: A list of 3 string objects. Each string object should contain 1 str.format code where a
      floating point number is to be inserted
    :param float pA: The probability of an event A
    :param float pB_given_A: The probability of an event B given event A is observed
    :param float pB_given_notA: The probability of an event B given the converse of event A has been observed.
    :return: A dictionary object with 3 elements holding the ratings given by the participant and the joint distribution
      implied by the bars they drew. The 'more_likely' element gives the name of the event rated more likely by the
      participant. The 'times_likely' element gives the odds ratio in favor of the event rated more likely. The 'joint'
      element holds the joint distribution as a 2x2 contingency table. The A event is along the rows, the B event is
      along the columns
    :rtype: dict[str, DataFrame, float]
    """
    validate_probabilities(pA, pB_given_A, pB_given_notA)

    win = axis.win
    problem_textstim = create_problem_textstim(win, problem_text, pA, pB_given_A, pB_given_notA)

    bars = {"A_major": AdjustableBar(win,
                                     bounds=(axis.bounds[3], axis.bounds[1]),
                                     pos=(axis.bounds[3] + axis.width / 4, axis.bounds[0] - axis.height / 4),
                                     width=axis.width / 2, height=axis.height / 4,
                                     lineColor="#000000", fillColor="#000000", lineWidth=3,
                                     name="A_major", focused=False),
            "notA_major": AdjustableBar(win,
                                        bounds=(axis.bounds[3], axis.bounds[1]),
                                        pos=(axis.bounds[3] + axis.width / 4, axis.bounds[2] + axis.height / 4),
                                        width=axis.width / 2, height=axis.height / 4,
                                        lineColor="#000000", fillColor="#0000FF", lineWidth=3,
                                        name="notA_major", focused=False),
            "A_minor": AdjustableBar(win,
                                     bounds=(axis.bounds[3], axis.bounds[3] + axis.width / 2),
                                     pos=(axis.bounds[3] + axis.width / 8, axis.bounds[0] - axis.height / 4),
                                     width=axis.width / 4, height=axis.height / 4,
                                     lineColor="#000000", fillColor="#f9f50c", lineWidth=3,
                                     name="A_minor", focused=False),
            "notA_minor": AdjustableBar(win,
                                        bounds=(axis.bounds[3], axis.bounds[3] + axis.width / 2),
                                        pos=(axis.bounds[3] + axis.width / 8, axis.bounds[2] + axis.height / 4),
                                        width=axis.width / 4, height=axis.height / 4,
                                        lineColor="#000000", fillColor="#f9f50c", lineWidth=3,
                                        name="notA_minor", focused=False)
            }

    names = list(bars.keys())  # use this to keep track of what bars we need to add
    rect = bars[names[0]]
    names = names[1:]
    rect.autoDraw = True
    rect.focused = True  # Needs to be set after autodraw to make sure handle is drawn on top of bar
    active_rects = [rect]
    win.flip()

    prompt = TextStim(win, text="Press Enter to finalize the bars", height=.075, pos=(0, -.85), wrapWidth=1.5)
    # prompt.autoDraw = False is implied, but has to be explicitly set before it can be used in an equality comparison
    # because of shennanigans with the attributeSetter wrapper around this property
    prompt.autoDraw = False

    mouse = event.Mouse()

    while True:
        # Activate (draw) bars one at a time
        if all([x.adjusted for x in active_rects]) and names:
            rect = bars[names[0]]
            names.pop(0)
            rect.autoDraw = True
            rect.focused = True  # Needs to be set after autodraw to make sure handle is drawn on top of bar
            for r in active_rects:
                r.focused = False
            active_rects.append(rect)
            win.flip()

        if prompt.autoDraw:
            if event.getKeys(keyList=['return']):
                break

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
                    if drag_pos <= rect.bounds[0]:
                        rect.handle.pos = (rect.bounds[0], rect.handle.pos[1])
                        rect.width = max(.0075, rect.bounds[0] - axis.bounds[3] + .0075)
                        rect.pos = (axis.bounds[3] + rect.width / 2, rect.pos[1])
                    elif rect.bounds[0] < drag_pos < rect.bounds[1]:
                        delta = drag_pos - rect.handle.pos[0]
                        rect.handle.pos = (drag_pos, rect.handle.pos[1])
                        rect.width = rect.width + delta
                        rect.pos = (axis.bounds[3] + rect.width / 2, rect.pos[1])
                    elif rect.bounds[1] <= drag_pos:
                        rect.handle.pos = (rect.bounds[1], rect.handle.pos[1])
                        rect.width = rect.bounds[1] - axis.bounds[3] - .0075
                        rect.pos = (axis.bounds[3] + rect.width / 2, rect.pos[1])
                    win.flip()

                rect.opacity = 1
                win.flip()

                if "major" in rect.name:
                    minor_bar = bars[prefix + "_minor"]
                    minor_bar.bounds = (axis.bounds[3], rect.pos[0] + rect.width / 2)
                    if minor_bar not in active_rects:
                        # .width must be updated before .pos! setting .pos triggers handle positioning update, which
                        # relies on .width being accurate
                        minor_bar.width = rect.width / 2
                        minor_bar.pos = (axis.bounds[3] + rect.width / 4, minor_bar.pos[1])
                if "minor" in rect.name:
                    bars[prefix + "_major"].bounds = (rect.pos[0] + rect.width / 2, axis.bounds[1])

                # Names is empty after all bars have been activated, so at this point show the prompt
                if not names and not prompt.autoDraw:
                    prompt.autoDraw = True
                    win.flip()

    prompt.autoDraw = False

    more_likely_prompt = TextStim(win, pos=(-.6, -.6), text="Which is more likely?", height=.06, color='#FFFFFF')
    more_likely_prompt.autoDraw = True
    more_likely_scale = RatingScale(win, pos=(-.6, -.7), choices=['Eats Cookies', "Doesn't Eat Cookies"],
                                    markerStart=0.5, textSize=1.25, size=.6,
                                    textColor='#FFFFFF', lineColor="#000000", showAccept=False
                                    )

    times_likely_prompt = TextStim(win, pos=(.3, -.6), text="How many times more likely?", height=.06, color='#FFFFFF')
    times_likely_prompt.autoDraw = True
    times_likely_scale = Slider(win, pos=(.3, -.7), ticks=[1] + list(range(5, 51, 5)),
                                granularity=.5, style="marker")
    times_likely_scale.markerPos = 1
    times_likely_scale.rating = 1
    times_likely_scale.marker.size = (times_likely_scale._tickL / 5,
                                      times_likely_scale._tickL / 5 * (win.size[0] / win.size[1])
                                      )
    times_likely_resp = TextStim(win, pos=(.3, -.8), text="1x", height=.06, color='#FFFFFF')
    times_likely_resp.autoDraw = True

    accept_box = Rect(win, pos=(0, -.9), height=.1, width=.25, autoDraw=True, lineColor="DarkGray")
    accept_text = TextStim(win, text="Accept", pos=(0, -.9), height=.06, color="DarkGray")

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
        b.autoDraw = False
        b.handle.autoDraw = False

    # Compute the implied joint distribution
    est_pA = bars['A_major'].width / axis.width
    est_pnotA = bars['notA_major'].width / axis.width
    est_pA_B = bars['A_minor'].width / axis.width
    est_pnotA_B = bars['notA_minor'].width / axis.width
    est_pA_notB = est_pA - est_pA_B
    est_pnotA_notB = est_pnotA - est_pnotA_B
    joint = DataFrame({'A': [est_pA_B, est_pA_notB],
                       'notA': [est_pnotA_B, est_pnotA_notB]
                       },
                      index=['B', 'notB']
                      )

    return {'more_likely': more_likely_scale.getRating(),
            'times_likely': times_likely_scale.getRating(),
            'joint': joint
            }


def validate_probabilities(*args):

    for p in args:
        if not 0 <= p <= 1:
            raise ValueError("All probabilities parameters must be between 0 and 1")


def create_problem_textstim(win, problem_text, pA, pB_given_A, pB_given_notA):
    txt = TextStim(win, text="\n".join(problem_text).format(pA=pA * 100,
                                                            pB_given_A=pB_given_A * 100,
                                                            pB_given_notA=pB_given_notA * 100
                                                            ),
                   pos=(0, .8), height=.07, wrapWidth=1.5)
    txt.autoDraw = True
    return txt


def feedback(win, events, pA, pB_given_A, pB_given_notA, joint):
    """
    Give visual feedback about how well the bars adjusted by the participant match the target, correct set of bars.

    
    :param psychopy.visual.window.Window win: A PsychoPy window object
    :param dict[str] events: A dictionary with 2 string objects that describe an event 'A' (e.g., Eats Cookies) and its
      complement 'notA' (e.g., Doesn't Eat Cookies).
    :param float pA: The probability of an event A. This should correspond to the probability of the event described in
      events['A']
    :param float pB_given_A: The probability of an event B given event A is observed
    :param float pB_given_notA: The probability of an event B given the converse of event A has been observed.
    :param DataFrame joint: A 2x2 pandas DataFrame describing a joint probability distribution. Requires column keys 'A'
       and 'notA' and row indices 'B' and 'notB'. This DataFrame is intended to be obtained from the output of the
       dynamic_trial function.
    :rtype: None
    """
    correct_axis = AxisStim(win, height=.75, width=1, pos=(0, .5), y_labels=(events['A'], events['notA']))
    correct_axis.autoDraw = False
    correct_title = TextStim(win, pos=(0, .9), height=.06, text="Correct Bars")

    correct_bars = {"A_major": Rect(win,
                                    pos=(correct_axis.bounds[3] + correct_axis.width * pA / 2,
                                         correct_axis.bounds[0] - correct_axis.height / 4),
                                    width=correct_axis.width * pA, height=correct_axis.height / 4,
                                    lineColor="#000000", fillColor="#000000", lineWidth=3,
                                    name="A_major"),
                    "notA_major": Rect(win,
                                       pos=(correct_axis.bounds[3] + correct_axis.width * (1-pA) / 2,
                                            correct_axis.bounds[2] + correct_axis.height / 4),
                                       width=correct_axis.width * (1 - pA), height=correct_axis.height / 4,
                                       lineColor="#000000", fillColor="#0000FF", lineWidth=3,
                                       name="B_major"),
                    "A_minor": Rect(win,
                                    pos=(correct_axis.bounds[3] + (correct_axis.width * pA * pB_given_A) / 2,
                                         correct_axis.bounds[0] - correct_axis.height / 4),
                                    width=correct_axis.width * pA * pB_given_A, height=correct_axis.height / 4,
                                    lineColor="#000000", fillColor="#f9f50c", lineWidth=3,
                                    name="A_minor"),
                    "notA_minor": Rect(win,
                                       pos=(correct_axis.bounds[3] + (correct_axis.width * (1-pA) * pB_given_notA) / 2,
                                            correct_axis.bounds[2] + correct_axis.height / 4),
                                       width=correct_axis.width * (1 - pA) * pB_given_notA, height=correct_axis.height / 4,
                                       lineColor="#000000", fillColor="#FF0000", lineWidth=3,
                                       name="B_minor")
                    }

    est_axis = AxisStim(win, height=.75, width=1, pos=(0, -.4), y_labels=events.values())
    est_axis.autoDraw = False
    est_title = TextStim(win, pos=(0, 0), height=.06, text="Your Bars")

    est_pA = joint.loc[:, 'A'].sum()
    est_pB_given_A = joint.loc['B', 'A'] / est_pA
    est_pB_given_notA = joint.loc['B', 'notA'] / (1 - est_pA)

    est_bars = {"A_major": Rect(win,
                                pos=(est_axis.bounds[3] + est_axis.width * est_pA / 2,
                                     est_axis.bounds[0] - est_axis.height / 4),
                                width=est_axis.width * est_pA, height=est_axis.height / 4,
                                lineColor="#000000", fillColor="#000000", lineWidth=3,
                                name="A_major"),
                "notA_major": Rect(win,
                                   pos=(est_axis.bounds[3] + est_axis.width * (1 - est_pA) / 2,
                                        est_axis.bounds[2] + est_axis.height / 4),
                                   width=est_axis.width * (1 - est_pA), height=est_axis.height / 4,
                                   lineColor="#000000", fillColor="#0000FF", lineWidth=3,
                                   name="B_major"),
                "A_minor": Rect(win,
                                pos=(est_axis.bounds[3] + (est_axis.width * est_pA * est_pB_given_A) / 2,
                                     est_axis.bounds[0] - est_axis.height / 4),
                                width=est_axis.width * est_pA * est_pB_given_A, height=est_axis.height / 4,
                                lineColor="#000000", fillColor="#f9f50c", lineWidth=3,
                                name="A_minor"),
                "notA_minor": Rect(win,
                                   pos=(est_axis.bounds[3] + (est_axis.width * (1 - est_pA) * est_pB_given_notA) / 2,
                                        est_axis.bounds[2] + est_axis.height / 4),
                                   width=est_axis.width * (1 - est_pA) * est_pB_given_notA, height=est_axis.height / 4,
                                   lineColor="#000000", fillColor="#FF0000", lineWidth=3,
                                   name="B_minor")
                }

    odds = (pA * pB_given_A)/((1-pA) * pB_given_notA)
    if odds > 1:
        more_likely = events['A']
        times_likely = odds
    else:
        more_likely = events['notA']
        times_likely = 1/odds

    correct_answer = TextStim(win, pos=(0, -.9), height=.07,
                              text="{:s} is {:.1f} times more likely".format(more_likely, times_likely))

    est_axis.draw()
    correct_axis.draw()
    est_title.draw()
    correct_title.draw()
    correct_answer.draw()
    for _, bar in correct_bars.items():
        bar.draw()
    for _, bar in est_bars.items():
        bar.draw()

    next_box = Rect(win, pos=(.8, -.9), height=.1, width=.25)
    next_text = TextStim(win, pos=(.8, -.9), height=.075, text="Continue")
    next_box.draw()
    next_text.draw()

    win.flip()

    mouse = event.Mouse()
    while True:
        if mouse.isPressedIn(next_box):
            break
