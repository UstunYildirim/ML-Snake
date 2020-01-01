from Agent import *

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

    def createNewAgents(s,m,n,k,NNStr):
        newAgents = []
        for i in range(k):
            newAgents.append(Agent(Game(m,n), NNStr))
        return newAgents

    def loadSession(s, params):
        s.m = params['m']
        s.n = params['n']
        s.numS = params['numS']
        s.numTopP = params['numTopP']
        s.numNewB = params['numNewB']
        s.numGamesToAve = params['numGamesToAve']
        s.NNStructure = params['NNStructure']
        s.genNo = params['genNo']
        s.agents = params['agents']

    def saveSession(s, folder = 'trained', fileNamePrefix = 'agents_'):
        pass

    def trainingSessionMain(s):
        pass

    def getPerformance(s, a):
        p = 0
        a.finishTheGame()
        p += a.performanceEvaluation()
        for i in range(s.numGamesToAve-1):
            a.newGame(Game(s.m,s.n))
            a.finishTheGame()
            p += a.performanceEvaluation()
        av = p/s.numGamesToAve
        a.performanceEvaluated = av
        return av

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

    def saveData(s):
        d = {}
        d['m'] = s.m
        d['n'] = s.n
        d['numS'] = s.numS
        d['numTopP'] = s.numTopP
        d['numNewB'] = s.numNewB
        d['numGamesToAve'] = s.numGamesToAve
        d['genNo'] = s.genNo
        d['agents'] = s.agents
        writeDataToFile(d,
                'trained/agents_' +\
                str(s.m) +\
                'x' + str(s.n) +\
                '.dat')

    def loadAndContinue(s):
        d = readDataFromFile(s.loadAndContFromFile)
        s.m = d['m']
        s.n = d['n']
        s.numS = d['numS']
        s.numTopP = d['numTopP']
        s.numNewB= d['numNewB']
        s.numGamesToAve = d['numGamesToAve']
        s.genNo = d['genNo']
        s.agents = d['agents']
        numAgents = len(s.agents)
        i = 0
        while len(s.agents) < s.numTopP: # this might happen if numTopP is increased externally
            a = deepcopy(s.agents[i])
            a.randomVariation()
            s.agents.append(a)
            i += 1
        s.evolveAndMultiply()
