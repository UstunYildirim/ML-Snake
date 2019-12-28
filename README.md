# ML-Snake

This is a pretty standard Snake game with Machine Learning added.
You may find a [demo video](https://raw.githubusercontent.com/UstunYildirim/ML-Snake/master/Screen%20Capture/Screen%20Recording.mp4) in "Screen Capture" directory of a 2 layer NN playing the game.
Currently, the AI is supplied with a very limited amount of information about its surroundings.
(It can only see 2 squares away from where its head is and the location of the food relative to its head.)
So it is not very clever.

## What can this package do?

* You may play in the single player mode (this is mainly to test if things are okay).
* Train AI to play the snake game (at the end of the training it will automatically save the training data).
* Load saved training data and continue training.
* There is an '-an' (All-Nighter) mode which makes the training run without any input from you. (It stops when you type q and press enter.)
  For example, 
  > python3 Main.py -an -N 
  
  creates a new training session and runs it until you type q and press enter .
* It can visualize the training data (like in the demo video).

Just run Main.py, it will tell you what to do.
