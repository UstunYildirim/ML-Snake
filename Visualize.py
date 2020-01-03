import os, select, sys
import numpy as np
from Agent import *
from Game import *


class Visualize():

    def __init__(s, agent = None, game = None):
        if agent is not None:
            s.agent = agent
            s.game = s.agent.game
        else:
            s.agent = None
            s.game = game
        s.state = s.game.state
        s.playground = Game(s.game.m,s.game.n)
        if agent is not None:
            s.playground.state[s.playground.foodCoords] = Game.empty
            s.playground.state[s.agent.foodCoords[0]] = Game.food
            s.playground.foodCoords = s.agent.foodCoords[0]
    def __letterToMoveConv__(s,l):
        if l == 'h':
            return Game.left
        if l == 'j':
            return Game.down
        if l == 'k':
            return Game.up
        if l == 'l':
            return Game.right
        raise Exception("Letter is not a move")
        
    def goBackNLines(s, N):
        termSize = os.get_terminal_size()
        numTermCols = termSize.columns
        print('\b'*numTermCols*N, end='')

    def playMovie(s):
        moves = [s.__letterToMoveConv__(l) for l in s.agent.seqMoves]
        foods = s.agent.foodCoords
        i = 0 
        j = 0
        while i <= len(moves):
            if i > 0:
                s.goBackNLines(s.game.m+2)
            s.display(s.playground)
            print("Score: ", s.playground.score)
            print("Turns: ", s.playground.numTurns)
            if i == len(moves):
                return 
            inp, out, exc = select.select([sys.stdin],[],[], 0.01+1/len(moves))
            if inp:
                q = sys.stdin.readline().strip()
                if q == 'q':
                    return
                s.goBackNLines(1)


            s.playground.snakeDir = moves[i]
            i += 1
            s.playground.timeStep()
            if foods[j] != s.playground.foodCoords:
                j += 1
                s.playground.state[s.playground.foodCoords] = Game.empty
                s.playground.state[foods[j]] = Game.food
                s.playground.foodCoords = foods[j]

    def display(s,game):
        print(s.prettify(game))

    def replaceEntry(s, entry):
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

    def betterSnakeBody(s, game, charMatrix):
        snake = np.array(game.snake)
        for i in range(1,len(snake)-1):
            ds1 = snake[i] - snake[i-1] # "first" body part
            ds2 = snake[i+1] - snake[i] # "second" body part
            if ds1[0] == 0:
                if ds2[0] == 0: # both body parts are horizontal
                    charMatrix[tuple(snake[i])] = '-'
                elif ds1[1]*ds2[0] > 0: # body is turning
                    charMatrix[tuple(snake[i])] = '\\'
                else:
                    charMatrix[tuple(snake[i])] = '/'
            else:
                if ds2[1] == 0: # both body parts are vertical
                    charMatrix[tuple(snake[i])] = '|'
                elif ds1[0]*ds2[1] > 0: # body is turning
                    charMatrix[tuple(snake[i])] = '\\'
                else:
                    charMatrix[tuple(snake[i])] = '/'
        return charMatrix



    def prettify(s, game):
        re = np.vectorize(s.replaceEntry)
        charMatrix = re(game.state)
        charMatrix = s.betterSnakeBody(game, charMatrix)
        charMatrix[game.snake[0]] = 'o'
                # s.replaceEntry(charMatrix[game.snake[0]])
                # 'o' is simpler but
                # this is more safe in case of change
        st = ["".join(r) for r in charMatrix]
        st = "\n".join(st)
        return st

