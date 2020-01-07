from Agent import *
from heapq import nlargest
from copy import deepcopy

class EvolutionSession():

    def newSession(s, params):
        s.m = params['m']
        s.n = params['n']
        s.numS = params['numS']
        s.numTopP = params['numTopP']
        s.numNewB = params['numNewB']
        s.numGamesToAve = params['numGamesToAve']
        s.NNString = params['NNString']
        s.NNStructure = params['NNStructure']
        s.genNo = 0
        s.agents = s.createNewAgents(s.m,s.n,s.numS,s.NNStructure)
        s.topAgents = []
        s.topPerfs = []
        s.stats = {}
        s.bestAgent = None
        s.bestAgentPerf = -10**10

    def createNewAgents(s,m,n,k,NNStr):
        newAgents = []
        for i in range(k):
            newAgents.append(Agent(m,n, NNStr))
        return newAgents

    def simulateOneGeneration(s):
        s.genNo += 1
        avePerformances = []
        maxPerformances = []
        minPerformances = []
        rngPerformances = []
        for a in s.agents:
            agentPerformance = []
            for i in range(s.numGamesToAve):
                a.newGame()
                a.playTheGame(5 + s.genNo) #HyperParam
                p = a.performanceEvaluation()
                agentPerformance.append(p)
                if s.bestAgentPerf < p:
                    s.bestAgent = deepcopy(a)
                    s.bestAgentPerf = p
                    #s.bestAgentGameInfo = deepcopy(a.seqMoves, a.foodCoords)
            aveP = sum(agentPerformance)/s.numGamesToAve
            maxP = max(agentPerformance)
            minP = min(agentPerformance)
            rngP = maxP-minP
            avePerformances.append(aveP)
            maxPerformances.append(maxP)
            minPerformances.append(minP)
            rngPerformances.append(rngP)
        s.stats['last'] = {
                'ave': avePerformances,
                'max': maxPerformances,
                'min': minPerformances,
                'rng': rngPerformances
                }

        aveAve = sum(avePerformances)/len(avePerformances)
        aveMax = sum(maxPerformances)/len(maxPerformances)
        aveMin = sum(minPerformances)/len(minPerformances)
        aveRng = sum(rngPerformances)/len(rngPerformances)
        s.stats[s.genNo] = {
                'ave': aveAve,
                'max': aveMax,
                'min': aveMin,
                'rng': aveRng 
                }

    def pickTopAgents(s):
        s.topAgents = []
        s.topPerfs = []
        topAgentPerfPairs = nlargest(
                s.numTopP,
                zip(
                    s.agents,
                    s.stats['last']['ave'],
                    s.stats['last']['max'],
                    s.stats['last']['min'],
                    s.stats['last']['rng']
                    ),
                key=lambda a: a[1]) #HyperParam ave seems to be the best choice
        for a in topAgentPerfPairs:
            s.topAgents.append(a[0])
            s.topPerfs.append(a[1:])

    def purgeAndMultiply(s):
        s.agents = s.topAgents

        s.agents += s.createNewAgents(s.m, s.n, s.numNewB, s.NNStructure)

        i = 0
        while len(s.agents) < s.numS:
            a = Agent(s.m,s.n, s.NNStructure)
            a.NNLayers = deepcopy(s.agents[i].NNLayers)
            a.randomVariation()
            s.agents.append(a)
            i = (i+1)%s.numTopP

