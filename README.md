# ML-Snake

This is a pretty standard Snake game with Machine Learning added.
You may find a [demo video](https://raw.githubusercontent.com/UstunYildirim/ML-Snake/master/Screen%20Capture/Screen%20Recording.mp4) in "Screen Capture" directory of a 2 layer NN playing the game.
Currently, the AI is supplied with a very limited amount of information about its surroundings.
(The version in the video can only see 2 squares away from where its head is and the location of the food relative to its head.)
So it is not very clever.

## What can this package do?

* You may play in the single player mode.
  > python3 Main.py -SP 7 10 # to play on a 7x10 board, key bindings are vim-like [hjkl]
* Train AI to play the snake game (at the end of the training it will automatically save the training data).
* Load saved training data and continue training.
* There is an '-an' (All-Nighter) mode which makes the training run without any input from you. (It stops when you type q and press enter.)
  For example, 
  > python3 Main.py -an -Ne
  
  creates a new training session and runs it until you type q and press enter .
* It can visualize the training data (like in the demo video).

Just run Main.py, it will tell you what to do.

## To be implemented soon

* Technically, there are two modes of learning, one of them is creation of a whole generation of snakes, selecting the top performers and replicating them with small modifications in the next generation. The other mode is called a single snake session. In this mode a single snake plays games over and over again, learning at each turn what to do based on a performance evaluation metric. This learning mode is not complete at the moment.
* We will implement CNNs and make the AI see the whole board as a single picture.
