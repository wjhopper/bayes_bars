## Bayes Bars
The Bayes Bars repository is a collection of [Python](https://www.python.org/) scripts which support developing [PsychoPy](https://www.psychopy.org/index.html) experiments on visual guides to Bayesian reasoning.

These scripts are intended to be packaged in the source code of an experiment.

## Functions
There are 4 important user-facing functions:

- `AxisStim`
- `static_trial`
- `dynamic_trial`
- `feedback`

#### AxisStim
The `AxisStim` function implements an xy axis using a [PsychoPy BufferImageStim](https://www.psychopy.org/api/visual/bufferimagestim.html#psychopy.visual.BufferImageStim). The axis has with a continuous x axis ranging from 0% to 100% and a binary y axis. You can set the width, height and center of the axis, as well as the labels on the y axis.

#### static_trial
The `static_trial` function describes the reasoning problem, displays the bars representing the marginal and conditional probabilities described in the problem, and two rating scales for responding:

1. Which event is more likely?
2. How much more likely is the event?

The function requires an `AxisStim` object (where the bars are drawn to scale), the text describing the problem, and the 3 given probability values p(A), p(B|A) and p(B|A̅)

#### dynamic_trial
The `dynamic_trial` function is similar to the `static_trial` function, but instead of displaying bars on the axis representing the marginal and conditional probabilities described in the problem, it displays *adjustable* bars which can be re-sized using the mouse cursor (much like shapes in PowerPoint slide decks).

One the participant is satisfied they have re-sized the bars to accurately represent the marginal and conditional probabilities described in the problem, they may move on to giving the same likelihood ratings as in the `static_trial`.


#### feedback
This function displays the bars which correctly describe the joint distribution above the bars the participant has drawn (on two separate axis), along with the precise odds of the more likely event.

To compute the widths of the participants bars, you must pass in the 2x2 contingency table that is output from the `dynamic_trial` function, which can be found in the `joint` element of the dictionary object returned by the `dynamic_trial` function.

## Demo
A demonstration of each these functions can be seen in the `main.py` file