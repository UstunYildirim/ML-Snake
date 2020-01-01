import pickle
import numpy as np
import math
from Game import *

def isObstacle(game, pr, obstacleType = None):
    (i,j) = pr
    if i < 0 or i >= game.m or j < 0 or j >= game.n:
        return 1
    if obstacleType is not None:
        return 1 if game.state[i,j] == obstacleType else 0
    obs = (Game.wall | Game.body)
    if game.state[i,j] & obs:
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

def obstaclesNearHead(game, n=1, obsType = None): # be able to see n steps away
    hi, hj = game.snake[0]
    res = []
    for s in range(1,n+1):
        for i in range(s):
            res.append((hi + i,     hj + (s - i)))
            res.append((hi + (s-i), hj -  i))
            res.append((hi - i, hj - (s - i)))
            res.append((hi - (s-i), hj + i))
    return [(lambda ij: isObstacle(game, ij, obsType))(ij) for ij in res]

def extractFeatures(game):
    return game.state.flatten()/Game.boardRange
    # fi, fj = game.foodCoords
    # hi, hj = game.snake[0]

    # res = game.state.flatten() == Game.body
    # res2 = [hi, hj, fi, fj]

    # # res = [(fi-hi),
    # #         (fj-hj),
    # #         ] + obstaclesNearHead(game, 2, Game.wall) \
    # #             + obstaclesNearHead(game, 2, Game.body)

    # return np.concatenate((res,res2))

def featureLength(game):
    return len(extractFeatures(game))

def changeNumSnakesAndTopP(fileName, newNumS, newNumTopP, newNumNewB, newNumGamesToAve):
    d = readDataFromFile(fileName)

    if newNumS != '-':
        d['numS'] = int(newNumS)

    if newNumTopP != '-': 
        d['numTopP'] = int(newNumTopP)

    if newNumNewB != '-':
        d['numNewB'] = int(newNumNewB)

    if newNumGamesToAve != '-':
        d['numGamesToAve'] = int(newNumGamesToAve)
        
    writeDataToFile(d, fileName)
