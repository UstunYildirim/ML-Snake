import numpy as np 
from DataExtraction import *
from Game import *

g = Game(5,6)

def replaceEntry(entry):
    if entry == Game.empty:
        return ' '
    if entry == Game.wall:
        return '#'
    if entry == Game.head:
        return 'o'
    if entry == Game.tail:
        return '*'
    if entry == Game.body:
        return '+'
    if entry == Game.food:
        return 'x'


def prettify(state):
    re = np.vectorize(replaceEntry)
    charMatrix = re(state)
    st = ["".join(r) for r in charMatrix]
    st = "\n".join(st)
    return st

while True:
    print(prettify(g.state),'\n')
    print("Score, Dead, Won", g.score, g.dead, g.won)
    if g.dead == 1 or g.won == 1:
        exit()

    i = input("dir:")
    if i == 'j':
        g.snakeDir = g.down
    elif i == 'k':
        g.snakeDir = g.up
    elif i == 'h':
        g.snakeDir = g.left
    elif i == 'l':
        g.snakeDir = g.right
    elif i == 'q':
        fs = extractFeatures(g)
        writeDataToFile(fs ,'game.dat')
        print(fs)
        print('Bye!')
        exit()
    g.timeStep()
