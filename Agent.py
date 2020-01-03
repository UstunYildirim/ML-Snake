from NNLayer import *
from DataHandler import *

class Agent():

    def __init__(s, m, n, NNStructure): 
        s.m = m
        s.n = n
        s.NNLayers = []
        NNStructure = [(s.featureLength(),None)] + \
                NNStructure + \
                [(4,identity)]
        for i in range(1,len(NNStructure)):
            s.NNLayers.append(
                    NNLayer(NNStructure[i-1][0],
                        NNStructure[i][0],
                        mu = 0,
                        sigma = 0.3,
                        activation = NNStructure[i][1]))

    def extractFeatures(s, game):
        return game.state.flatten()/Game.boardRange

    def featureLength(s):
        return s.m*s.n

    def newGame(s):
        s.game = Game(s.m, s.n)
        s.seqMoves = ''
        s.foodCoords = [s.game.foodCoords]

    def performanceEvaluation(s):
        baseNo = s.game.m*s.game.n
        totalScore = 5*baseNo

        totalScore -= np.sqrt(s.game.numTurns)
        totalScore += baseNo * s.game.score
        totalScore -= 1.5*baseNo * s.game.dead
        totalScore += 20*baseNo * s.game.won

        hi, hj = s.game.snake[0]
        fi, fj = s.game.foodCoords
        totalScore -= np.abs(fi-hi)
        totalScore -= np.abs(fj-hj)

        return totalScore

    def randomVariation(s, varMagnitude=0.1):
        for layer in s.NNLayers:
            layer.randomVariation(varMagnitude)

    def playSingleTurn(s):
        if s.game.dead or s.game.won:
            return
        inp = s.extractFeatures(s.game)
        for layer in s.NNLayers:
            inp = layer.forwardPropogate(inp)
        moveIndex = np.argmax(inp)
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

