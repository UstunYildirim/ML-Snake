import numpy as np
from NNLayer import *
from Game import *

class Agent():

    def __init__(s, m, n, NNStructure): 
        s.m = m
        s.n = n
        s.NNLayers = []
        NNStructure = [(s.featureLength(),None)] + \
                NNStructure + \
                [(4,sigmoid)]
        for i in range(1,len(NNStructure)):
            s.NNLayers.append(
                    NNLayer(NNStructure[i-1][0],
                        NNStructure[i][0],
                        activation = NNStructure[i][1]))

    # def extractFeatures(s, game):
    #     return game.state.flatten()/Game.boardRange
    # 
    # def featureLength(s):
    #     return s.m*s.n
    # 
    def extractFeatures(s, game):
        res = s.normFoodCoords(game)-s.normHeadCoords(game)
        res = np.concatenate((res, s.obstaclesNearHead(game, 4)))
        return res
    def featureLength(s):
        return 42

    def __isObstacle__(s, game, pr, obstacleType = None):
        (i,j) = pr
        if i < 0 or i >= game.m or j < 0 or j >= game.n:
            return 1
        if obstacleType is not None:
            return 1 if game.state[i,j] == obstacleType else 0
        if game.state[i,j] & Game.wall or game.state[i,j] & Game.body:
            return 1
        return 0

    def normFoodCoords(s, game):
        [x,y] = game.foodCoords
        return np.array([x/game.m, y/game.n])

    def normHeadCoords(s, game):
        [x,y] = game.snake[0]
        return np.array([x/game.m, y/game.n])

    def obstaclesNearHead(s, game, n=1, obsType = None): # be able to see n steps away
        hi, hj = game.snake[0]
        res = []
        for sm in range(1,n+1):
            for i in range(sm):
                res.append((hi + i,     hj + (sm - i)))
                res.append((hi + (sm-i), hj -  i))
                res.append((hi - i, hj - (sm - i)))
                res.append((hi - (sm-i), hj + i))
        return [(lambda ij: s.__isObstacle__(game, ij, obsType))(ij) for ij in res]


    def newGame(s):
        s.game = Game(s.m, s.n)
        assert(s.featureLength() == len(s.extractFeatures(s.game)))
        s.seqMoves = ''
        s.foodCoords = [s.game.foodCoords]

    def performanceEvaluation(s):
        baseNo = s.game.m*s.game.n
        totalScore = 5*baseNo

        #totalScore -= np.sqrt(s.game.numTurns)
        totalScore += baseNo * s.game.score
        totalScore -= 1.5*baseNo * s.game.dead
        totalScore += 20*baseNo * s.game.won

        hi, hj = s.game.snake[0]
        fi, fj = s.game.foodCoords
        totalScore -= np.abs(fi-hi)
        totalScore -= np.abs(fj-hj)

        return totalScore

    def randomVariation(s, varMagnitude=0.01):
        for layer in s.NNLayers:
            layer.randomVariation(varMagnitude)

    def playForcedMove(s, moveIndex):
        if s.game.dead or s.game.won:
            return
        s.seqMoves += ("hjkl"[moveIndex])
        s.game.snakeDir = [Game.left,
                            Game.down,
                            Game.up,
                            Game.right][moveIndex]
        s.game.timeStep()

    def shouldHaveDecided(s, Y):
        a = s.lastActivation*0.99+0.005 # to avoid overflow
        dA = -(np.divide(Y,a)-np.divide(1-Y,1-a))
        for layer in reversed(s.NNLayers):
            dA = layer.backwardPropogate(dA)
        for layer in s.NNLayers:
            layer.updateParams(learningRate=0.0001,lambd=0.0001)


    def playSingleTurn(s):
        if s.game.dead or s.game.won:
            return
        inp = s.extractFeatures(s.game)
        for layer in s.NNLayers:
            inp = layer.forwardPropogate(inp)
        s.lastActivation = inp.reshape(4,1)
        moveIndex = np.argmax(s.lastActivation)
        s.seqMoves += ("hjkl"[moveIndex])
        s.game.snakeDir = [Game.left,
                            Game.down,
                            Game.up,
                            Game.right][moveIndex]
        s.game.timeStep()

    def playTheGame(s, maxTurns = 0):
        maxTurns = int(maxTurns)
        noFoodLimit = s.game.m + s.game.n + len(s.game.snake)
        lastScore = 0 
        i = 0
        while not (s.game.dead or s.game.won):
            s.playSingleTurn()
            i += 1
            if lastScore != s.game.score:
                s.foodCoords.append(s.game.foodCoords)
                lastScore = s.game.score
                i = 0
            if i == noFoodLimit:
                break
            if s.game.numTurns == maxTurns:
                break

