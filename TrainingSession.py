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

    def createNewAgents(s,m,n,k,NNStr):
        newAgents = []
        for i in range(k):
            newAgents.append(Agent(m,n, NNStr))
        return newAgents

    def simulateOneGeneration(s):
        s.genNo += 1
        s.performances = []
        for a in s.agents:
            agentPerformance = []
            for i in range(s.numGamesToAve):
                a.newGame()
                a.playTheGame() #TODO choose maxTurn param
                agentPerformance.append(
                        a.performanceEvaluation())
            agAvPerf = sum(agentPerformance)/s.numGamesToAve
            s.performances.append(agAvPerf)

    def pickTopAgents(s):
        s.topAgents = nlargest(
                s.numTopP,
                zip(s.agents,s.performances),
                key=lambda a: a[1])


    def simulateGenerationAndPurge(s):
        s.agents = nlargest(s.numTopP,
                s.agents,
                key = s.getPerformance)

    def evolveAndMultiply(s):
        topPerfs = [a.performanceEvaluation() for a in s.agents]
        for a in s.agents:
            a.newGame(Game(s.m,s.n))

        s.createBrandNewSnakes(s.m,s.n,s.numNewB)

        numSpotsToBeFilled = s.numS-len(s.agents)
        perfSum = np.sum(topPerfs)
        #NOT SUPER CLEAN
        for i in range(s.numTopP):
            numCopies = int(topPerfs[i]/perfSum*numSpotsToBeFilled)
            newA = []
            for j in range(numCopies):
                newA.append(deepcopy(s.agents[i]))
            for a in newA:
                a.randomVariation()
            s.agents += newA

        i = 0
        while len(s.agents) < s.numS:
            a = deepcopy(s.agents[i])
            a.randomVariation()
            s.agents.append(a)
            i = (i+1)%s.numTopP

