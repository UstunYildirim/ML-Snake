import pickle
import numpy as np
import math
from Game import *

def isObstacle(game, pr):
    # Hardcoded for efficiency
    # if entry == Game.wall \
    # or entry == Game.body:
    (i,j) = pr
    if i < 0 or i >= game.m or j < 0 or j >= game.n:
        return 1
    if game.state[i,j] & 3:
        return 1
    return 0

def normFoodCoords(game):
    [x,y] = game.foodCoords
    return np.array([x/game.m, y/game.n])

def normHeadCoords(game):
    [x,y] = game.snake[0]
    return np.array([x/game.m, y/game.n])

def normTailCoords(game):
    [x,y] = game.snake[-1]
    return np.array([x/game.m, y/game.n])

def obstaclesNearHead(game):
    # Hardcoded for efficiency
    hi, hj = game.snake[0]
    res = [
            (hi-1, hj  ), #up
            (hi  , hj+1), #right
            (hi+1, hj  ), #down
            (hi  , hj-1), #left
            (hi-2, hj  ),
            (hi  , hj+2),
            (hi+2, hj  ),
            (hi  , hj-2),
            (hi-1, hj-1),
            (hi-1, hj+1),
            (hi+1, hj+1),
            (hi+1, hj-1)
        ]
    return [(lambda ij: isObstacle(game, ij))(ij) for ij in res]

def extractFeatures(game):
    fi, fj = game.foodCoords
    hi, hj = game.snake[0]
    di, dj = game.snakeDir
            
    res = [(fi-hi),
            (fj-hj),
            ] + obstaclesNearHead(game)

    return res

def featureLength(game):
    return len(extractFeatures(game))

def writeDataToFile(data, fileName):
    f = open(fileName, 'wb')
    pickle.dump(data, f)
    f.close()

def readDataFromFile(fileName):
    f = open(fileName, 'rb')
    new_d = pickle.load(f)
    f.close()
    return new_d

def changeNumSnakesAndTopP(fileName, newNumS, newNumTopP):
    d = readDataFromFile(fileName)
    d['numS'] = newNumS
    d['numTopP'] = newNumTopP
    writeDataToFile(d, fileName)
