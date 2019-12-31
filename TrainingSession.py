

class TrainingSession():


    def newSession(s, params):
        s.m = params['m']
        s.n = params['n']
        s.numS = params['numS']
        s.numTopP = params['numTopP']
        s.numNewB = params['numNewB']
        s.numGamesToAve = params['numGamesToAve']
        s.NNStructure = params['NNStructure']
        s.genNo = params['genNo']
        s.agents = params['agents']


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

    def saveSession(s):
        pass

    def trainingSessionMain(s):
        pass

    def createBrandNewSnakes(s,m,n,k):
        for i in range(k):
            s.agents.append(Agent(Game(m,n)))


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

    def newTrainingSession(s):
        print("Creating a new training set based on " + s.configFile)
        s.readConfigFile()
        s.agents = []
        s.genNo = 0
        s.createBrandNewSnakes(s.m,s.n,s.numS)

    def simulationMain(s):
        try:
            if s.anMode:
                N = 1
            else:
                N = int(input("Enter the number of generations to simulate\n"))
        except:
            N = 1
        while True:
            s.genNo += 1
            s.simulateGenerationAndPurge()
            print('\nTop Scores of Gen ', s.genNo, ': ', [a.performanceEvaluation() for a in s.agents[0:s.numTopP]])
            N -= 1
            if s.anAutoSave != 0:
                if s.genNo % s.anAutoSave == 0:
                    s.saveData()
                    print("All data saved")
            if N == 0:
                try:
                    if s.anMode:
                        N = 1
                        inp, out, exc = select.select([sys.stdin],[],[], 0.001)
                        if inp:
                            N = int(sys.stdin.readline().strip())
                    else:
                        N = int(input("How many generation to simulate?\n"))
                except:
                    N = -1
                if N == -1:
                    print("\nTop Agents of Gen ", s.genNo, ":")
                    for a in s.agents[0:s.numTopP]:
                        a.printAgentInfo()
                    s.saveData()
                    exit()
            s.evolveAndMultiply()
