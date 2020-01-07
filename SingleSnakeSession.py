from Agent import *
import numpy as np 
from heapq import nlargest
from copy import deepcopy

class SingleSnakeSession():

    def newSession(s, params):
        s.m = params['m']
        s.n = params['n']
        s.NNString = params['NNString']
        s.NNStructure = params['NNStructure']
        s.turnNo = 0
        s.agent = s.createNewAgent(s.m,s.n,s.NNStructure)
        s.newGame()
        s.stats = {}

    def createNewAgent(s,m,n,NNStr):
        return Agent(m,n, NNStr)

    def newGame(s):
        s.agent.newGame()

    def fourCopies(s, agent):
        return [deepcopy(agent) for _ in range(4)]

    def trainOneTurn(s):
        s.turnNo += 1
        agents = s.fourCopies(s.agent)
        perfs = []
        for i, a in enumerate(agents):
            a.playForcedMove(i)
            perfs.append(a.performanceEvaluation())
        s.agent.playSingleTurn()

        sugMove = s.suggestedMove(perfs)
        s.agent.shouldHaveDecided(sugMove)

        pE = s.agent.performanceEvaluation()
        if 'topPerf' not in s.stats or s.stats['topPerf'] < pE:
            s.stats['topPerf'] = pE
            s.stats['bestAgent'] = deepcopy(s.agent)
        if s.agent.game.dead or s.agent.game.won:
            s.stats['lastPerf'] = pE
            s.stats['lastNumTurn'] = s.agent.game.numTurns
            return 1
        return 0

    def suggestedMove(s, perfs):
        mx = max(perfs)
        Y = np.array(perfs)
        Y = Y.reshape(4,1)
        Y = (Y == mx).astype(int)
        return Y
        
