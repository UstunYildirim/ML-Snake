import numpy as np 
from Game import *
from Visualize import *

class SinglePlayer():
    
    def __init__(s, m,n):
        s.m = m
        s.n = n
        s.game = Game(m,n)

    def Play(s):
        g = s.game
        vsr = Visualize(game=g)
        while True:
            vsr.display(g)
            print("Score", g.score)
            print("Turns", g.numTurns)
            if g.dead == 1:
                print("Game over!")
                return
            if g.won == 1:
                print("You win!")
                return

            i = input("")
            if i == 'j':
                g.snakeDir = g.down
            elif i == 'k':
                g.snakeDir = g.up
            elif i == 'h':
                g.snakeDir = g.left
            elif i == 'l':
                g.snakeDir = g.right
            elif i == 'q':
                print('Bye!')
                return
            g.timeStep()
            vsr.goBackNLines(s.m+3)
