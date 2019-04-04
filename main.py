from psychopy import visual, core, event
from axis import AxisStim
from trials import static_trial, dynamic_trial, feedback

win = visual.Window([1280, 768])
event.globalKeys.add(key='q', func=core.quit, name='shutdown')

pA = .2
pB_given_A = .1
pB_given_notA = .95

events = {'A': "Eats Cookies", "notA": "Doesn't Eat Cookies"}
text = ["{pA:.0f}% of people eat cookies.",
        "{pB_given_A:.0f}% of people who eat cookies also eat brownies.",
        "{pB_given_notA:.0f}% of people who do not eat cookies eat brownies",
        "Martina eats brownies. Is Martina more likely to eat cookies, or not eat cookies?"
        ]

trial_type = visual.TextStim(win, text="Static Trial", height=.15)
trial_type.draw()
win.flip()
core.wait(4)

# Be careful, the axis autodraws
ax = AxisStim(win, pos=(0, .05), height=.9, width=1, y_labels=events.values())

responses = static_trial(ax, text, pA=.2, pB_given_A=pB_given_A, pB_given_notA=pB_given_notA)
print("Participant response: {} is {:.1f} more likely".format(responses['more_likely'], responses['times_likely']))
ax.autoDraw = False

trial_type.text = "Dynamic Trial. Use the mouse to adjust the width of the bars"
trial_type.draw()
win.flip()
core.wait(4)

ax.autoDraw = True
responses = dynamic_trial(ax, text, pB_given_A=pB_given_A, pB_given_notA=pB_given_notA)
print("Participant response: {} is {:.1f} more likely".format(responses['more_likely'], responses['times_likely']))
bars_morelikely = responses['joint'].loc['B'].idxmax()
indices = ('A', 'notA') if bars_morelikely == 'A' else ('notA', 'A')
ratio = responses['joint'].loc['B', indices[0]] / responses['joint'].loc['B', indices[1]]
print("Answer based on bars: {} is {:.1f} more likely".format(events[bars_morelikely], ratio))
ax.autoDraw = False

feedback(win, events, pA, pB_given_A, pB_given_notA, joint=responses['joint'])
core.wait(5)
win.close()

