from psychopy import visual, core, event
from axis import AxisStim
from AdjustableBar import AdjustableBar
from trials import static_trial, dynamic_trial

win = visual.Window([1280, 768])
event.globalKeys.add(key='q', func=core.quit, name='shutdown')

pA = .2
pB_given_A=.1
pB_given_notA = .95

text = ["- {pA:.0f}% of people eat cookies.",
        "- {pB_given_A:.0f}% of people who eat cookies also eat brownies.",
        "- {pB_given_notA:.0f}% of people who do not eat cookies eat brownies"
        ]

ax = AxisStim(win, pos=(0, .125), height=1, width=1, y_labels=('Eats\nCookies', "Doesn't Eat\nCookies"))  # autodraws
responses = static_trial(ax, text, pA=.2, pB_given_A=pB_given_A, pB_given_notA=pB_given_notA)
print(responses)

responses = dynamic_trial(ax, text, pB_given_A=pB_given_A, pB_given_notA=pB_given_notA)
print(responses)

win.close()
