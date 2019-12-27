import numpy as np
import random
import math

class Game ():
    empty = 0
    wall = 1
    body = 2
    head = 4
    tail = 8
    food = 16

    up = (-1,0)
    down = (1,0)
    left = (0,-1)
    right = (0,1)

    def __init__(s,m,n):
        """
        This is the main game class.
        It takes two inputs (m and n) and creates a game board.
        m and n both have to be at least 5.

        state is a matrix representing the game.
        0 : empty space
        1 : wall
        2 : body of the snake
        3 : head of the snake (unique)
        4 : tail of the snake (unique)
        5 : food
        """
        try:
            assert(m>4)
            assert(n>4)
        except:
            raise Exception("Board dimensions should be at least 5x5")

        s.m = m # number of rows
        s.n = n # number of columns
        s.score = 0
        s.dead = 0
        s.won = 0
        s.numTurns = 0
        s.state = np.zeros((m,n),dtype=int)
        for i in range(m):
            s.state[i,0] = Game.wall
            s.state[i,n-1] = Game.wall
        for j in range(1,n-1):
            s.state[0,j] = Game.wall
            s.state[m-1,j] = Game.wall

        i = math.floor(m/3)
        j = math.floor(n/2)
        s.state[i,j] = Game.food
        s.foodCoords = (i,j)

        s.state[m-1-i,n-1-j] = Game.head
        s.state[m-1-i,n-1-j-1] = Game.tail
        s.snake = [(m-1-i,n-1-j),
                (m-1-i,n-1-j-1)]
        s.snakeDir = Game.right

    def isColliding(s, idx):
        if s.state[idx] == Game.wall \
            or s.state[idx] == Game.body:
                return True
        if len(s.snake) == 2 and s.state[idx] == Game.tail:
            return True
        return False

    def isEating(s, idx):
        if s.state[idx] == Game.food:
            return True
        return False

    def timeStep(s):
        (hi,hj) = s.snake[0]
        (di,dj) = s.snakeDir
        newHead = (hi+di,hj+dj)
        if s.isColliding(newHead):
            s.gameOver()
        s.snake.insert(0,newHead)
        if s.isEating(newHead):
            s.score += 1
            r = s.addNewFood()
            if r == -1:
                s.youWin()
        else:
            oldTail = s.snake.pop()
            s.state[oldTail] = Game.empty
        s.state[s.snake[0]] = Game.head
        s.state[s.snake[1]] = Game.body
        s.state[s.snake[-1]] = Game.tail
        s.numTurns += 1
    
    def gameOver(s):
        s.dead = 1
    
    def youWin(s):
        s.won = 1
    
    def addNewFood(s):
        empties = s.state == Game.empty
        (rows, cols) = empties.nonzero()
        l = len(rows)
        if l == 0:
            return -1 # no empty spaces left!
        newFood = random.randint(0,l-1)
        coords = (rows[newFood], cols[newFood])
        s.foodCoords = coords
        s.state[coords] = Game.food
