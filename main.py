from psychopy import visual, core, event
from axis import AxisStim
from AdjustableBar import AdjustableBar
from trials import static_trial, dynamic_trial

win = visual.Window([1280, 768])
event.globalKeys.add(key='q', func=core.quit, name='shutdown')

# pA = .2
# pB_given_A=.1
# pB_given_notA = .95

text = ["- {pA}% of people eat cookies.",
        "- {pB_given_A}% of people who eat cookies also eat brownies.",
        "- {pB_given_notA}% of people who do not eat cookies eat brownies"
        ]

ax = AxisStim(win, pos=(0, .125), height=1, width=1, y_labels=('Eats\nCookies', "Doesn't Eat\nCookies"))  # autodraws
responses = static_trial(ax, text)
print(responses)

responses = dynamic_trial(ax, text)
print(responses)

win.close()
