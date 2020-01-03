from Agent import *
from heapq import nlargest

class TrainingSession():

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
                a.playTheGame(2*s.genNo) #TODO choose maxTurn param
                agentPerformance.append(
                        a.performanceEvaluation())
            aveP = sum(agentPerformance)/s.numGamesToAve
            maxP = max(agentPerformance)
            minP = min(agentPerformance)
            rngP = maxP-minP
            avePerformances.append(aveP)
            maxPerformances.append(maxP)
            minPerformances.append(minP)
            rngPerformances.append(rngP)
        s.stats[s.genNo] = {
                'ave': avePerformances,
                'max': maxPerformances,
                'min': minPerformances,
                'rng': rngPerformances
                }

    def pickTopAgents(s):
        s.topAgents = []
        s.topPerfs = []
        topAgentPerfPairs = nlargest(
                s.numTopP,
                zip(
                    s.agents,
                    s.stats[s.genNo]['ave'],
                    s.stats[s.genNo]['max'],
                    s.stats[s.genNo]['min'],
                    s.stats[s.genNo]['rng']
                    ),
                key=lambda a: a[3])
        for a in topAgentPerfPairs:
            s.topAgents.append(a[0])
            s.topPerfs.append(a[1:])

