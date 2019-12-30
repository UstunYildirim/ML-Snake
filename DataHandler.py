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

def obstaclesNearHead(game, n=1): # be able to see n steps away
    hi, hj = game.snake[0]
    res = []
    for s in range(1,n+1):
        for i in range(s):
            res.append((hi + i,     hj + (s - i)))
            res.append((hi + (s-i), hj -  i))
            res.append((hi - i, hj - (s - i)))
            res.append((hi - (s-i), hj + i))
    return [(lambda ij: isObstacle(game, ij))(ij) for ij in res]

def extractFeatures(game):
    fi, fj = game.foodCoords
    hi, hj = game.snake[0]
    di, dj = game.snakeDir
            
    res = [(fi-hi),
            (fj-hj),
            ] + obstaclesNearHead(game, 2)

    return np.array(res).flatten()

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

def changeNumSnakesAndTopP(fileName, newNumS, newNumTopP, newNumNewBorns, newNumGamesToAve):
    d = readDataFromFile(fileName)

    if newNumS != '-':
        d['numS'] = int(newNumS)

    if newNumTopP != '-': 
        d['numTopP'] = int(newNumTopP)

    if newNumNewBorns != '-':
        d['numNewBorns'] = int(newNumNewBorns)

    if newNumGamesToAve != '-':
        d['numGamesToAve'] = int(newNumGamesToAve)
        
    writeDataToFile(d, fileName)
