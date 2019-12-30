from NNLayer import *
from DataHandler import *

class Agent():

    def __idn__(s, x):
        return x

    #TODO: create AI_Architecture class
    #      to allow creation and mixture
    #      of different kinds of AI simultaneously
    def __init__(s, game): 
        s.performanceEvaluated = None
        s.game = game
        s.NNLayers = []
        s.NNLayers.append(
                NNLayer(featureLength(game),
                    5,
                    mu = 0,
                    sigma  = 0.1,
                    activation = np.tanh))
        s.NNLayers.append(
                NNLayer(5,
                    5,
                    mu = 0,
                    sigma  = 0.1,
                    activation = np.tanh))
        s.NNLayers.append(
                NNLayer(5,
                    4,
                    mu = 0,
                    sigma  = 0.1,
                    activation = s.__idn__))

        s.seqMoves = ''
        s.foodCoords = [s.game.foodCoords]

    def newGame(s, game):
        s.game = game
        s.seqMoves = ''
        s.foodCoords = [s.game.foodCoords]
        s.performanceEvaluated = None

    def performanceEvaluation(s):
        if s.performanceEvaluated is not None:
            return s.performanceEvaluated

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

        s.performanceEvaluated = totalScore
        return s.performanceEvaluated

    def randomVariation(s, varMagnitude=0.1):
        for layer in s.NNLayers:
            layer.randomVariation(varMagnitude)

    def playSingleTurn(s):
        if s.game.dead or s.game.won:
            return
        inp = extractFeatures(s.game)
        for layer in s.NNLayers:
            inp = layer.forwardPropogate(inp)
        moveIndex = np.argmax(inp)
        s.seqMoves += ("hjkl"[moveIndex])
        s.game.snakeDir = [Game.left,
                            Game.down,
                            Game.up,
                            Game.right][moveIndex]
        s.game.timeStep()

    def finishTheGame(s):
        noFoodLimit = int((s.game.m*s.game.n)/3)
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
        s.performanceEvaluation()
        return s

    def printAgentInfo(s):
        print('Num Turns: ', s.game.numTurns)
        print('Score: ', s.game.score)
        print('Dead: ', s.game.dead)
        print('Won: ', s.game.won)
        print('Performance evaluation: ', s.performanceEvaluation())
