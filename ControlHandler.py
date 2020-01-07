import sys, select, pickle
from NNLayer import ReLU, sigmoid, identity
from Visualize import Visualize
from SinglePlayer import SinglePlayer
from EvolutionSession import *
from SingleSnakeSession import *


class ControlHandler():

    evolutionSess = 'evolution'
    singleSnakeSess = 'singleSnake'

    def __init__(s, argv):
        s.argv = argv

    def singlePlayer(s):
        #TODO: MVC should be reconsidered here
        # also visualize class will change!
        m = int(s.argv[2])
        n = int(s.argv[3])
        sp = SinglePlayer(m,n)
        sp.Play()

    def handleSessArgs(s):
        argv = s.argv
        s.anMode = False
        s.autoSaveEnabled = False
        s.configFile = 'snake.conf'
        s.sessFilePath = ''
        i = 2 
        while i < len(argv):
            if argv[i] == '-c':
                s.configFile = argv[i+1]
                i += 1
            elif argv[i] == '-an':
                s.anMode = True
            elif argv[i] == '-an+':
                s.anMode = True
                s.autoSaveEnabled = True
                s.autoSaveFreq = 0
            elif argv[i][:4] == '-an+':
                s.anMode = True
                s.autoSaveEnabled = True
                s.autoSaveFreq = int(argv[i][4:])
            elif s.sessFilePath == '':
                s.sessFilePath = argv[i]
            else:
                raise Exception("Invalid arguments")
            i += 1

        s.configParams = s.getConfigParams()
        configParams = s.configParams
        if s.sessType == '':
            s.sessType = configParams['sessType']
        if s.sessType not in [
                ControlHandler.evolutionSess,
                ControlHandler.singleSnakeSess
                ]:
            raise Exception('Session Type Error')
        if s.sessFilePath == '':
            if s.sessType == ControlHandler.evolutionSess:
                s.sessFilePath = ('trained/agents_{}x{}' + \
                        '_{}_{}_{}_{}_{}.dat').format(
                        configParams['m'],
                        configParams['n'],
                        configParams['numS'],
                        configParams['numTopP'],
                        configParams['numNewB'],
                        configParams['numGamesToAve'],
                        configParams['NNString'])
            elif s.sessType == ControlHandler.singleSnakeSess:
                s.sessFilePath = ('trained/agents_{}x{}' + \
                        '_{}.dat').format(
                        configParams['m'],
                        configParams['n'],
                        configParams['NNString'])
        if s.autoSaveEnabled and s.autoSaveFreq == 0:
            s.autoSaveFreq = s.configParams['autoSaveFreq']

    def newEvolutionSession(s):
        s.sessType = ControlHandler.evolutionSess
        s.handleSessArgs()
        evSess = EvolutionSession()
        evSess.newSession(s.configParams)
        s.runEvolutionSession(evSess)
        s.endEvolutionSession(evSess)

    def newSSsession(s):
        s.sessType = ControlHandler.singleSnakeSess
        s.handleSessArgs()
        ssSess = SingleSnakeSession()
        ssSess.newSession(s.configParams)
        s.runSSsession(ssSess)
        s.endSSsession(ssSess)

    def getConfigParams(s):
        confParams = {}
        f = open(s.configFile, 'r')
        for l in f:
            l = l.split('#')[0].strip()
            if ':' not in l:
                continue
            (a,b) = l.split(':')
            a = a.strip()
            b = b.strip()
            if a == 'board_height':
                confParams['m'] = int(b)
            elif a == 'board_width':
                confParams['n'] = int(b)
            elif a == 'number_of_snakes':
                confParams['numS'] = int(b)
            elif a == 'number_of_top_performers':
                confParams['numTopP'] = int(b)
            elif a == 'number_of_new_borns':
                confParams['numNewB'] = int(b)
            elif a == 'number_of_games_to_average':
                confParams['numGamesToAve'] = int(b)
            elif a == 'neural_network_structure':
                confParams['NNString'] = s.__shortenNNString__(b)
                confParams['NNStructure'] = s.__parseNNStr__(b)
            elif a == 'auto_save_freq':
                confParams['autoSaveFreq'] = int(b)
            elif a == 'number_of_top_snakes_to_print':
                confParams['numTopSnaToPrint'] = int(b)
            elif a == 'session_type':
                confParams['sessType'] = b
        f.close()
        return confParams

    def __parseNNStr__(s, txt):#FIXME: these may replace each other!
        t = np.tanh
        i = identity
        s = sigmoid
        r = ReLU
        return eval(txt)

    def __shortenNNString__(s, NNStr):
        t = 't'
        s = 's'
        r = 'r'
        i = 'i'
        return ''.join(map(lambda p:str(p[0])+p[1], eval(NNStr)))

    def getNumGensToSimulate(s):
        if not s.anMode:
            N = input("How many generation to simulate?\n")
            try:
                N = int(N)
                if type(N) is not int or N < 0:
                    raise Exception()
            except:
                N = -1
        else: # anMode
            N = 1
            inp, out, exc = select.select([sys.stdin],[],[], 0.001)
            if inp:
                N = sys.stdin.readline().strip()
            try:
                N = int(N)
                if type(N) is not int or N < 0:
                    raise Exception()
            except:
                N = -1
        return N

    def runEvolutionSession(s, evSess):
        N = s.getNumGensToSimulate()
        while N > 0:
            while N > 0:
                evSess.simulateOneGeneration()
                evSess.pickTopAgents()
                evSess.purgeAndMultiply()

                s.printEvSessStats(evSess)
                N -= 1
                if s.autoSaveEnabled and (evSess.genNo % s.autoSaveFreq == 0):
                    s.saveEvolutionSession(evSess)
                    print('Auto-saved')
            N = s.getNumGensToSimulate()

    def getNumTurnsToMove(s):
        if not s.anMode:
            N = input("How many turns to simulate?\n")
            try:
                N = int(N)
                if type(N) is not int or N < 0:
                    raise Exception()
            except:
                N = -1
        else: # anMode
            N = 1
            inp, out, exc = select.select([sys.stdin],[],[], 0.001)
            if inp:
                N = sys.stdin.readline().strip()
            try:
                N = int(N)
                if type(N) is not int or N < 0:
                    raise Exception()
            except:
                N = -1
        return N

    def runSSsession(s, ssSess):
        N = s.getNumTurnsToMove()
        while N > 0:
            while N > 0:
                gameOver = ssSess.trainOneTurn()
                if gameOver:
                    s.printSSsessStats(ssSess)
                    ssSess.newGame()
                N -= 1
                if s.autoSaveEnabled and (ssSess.turnNo % s.autoSaveFreq == 0):
                    s.saveEvolutionSession(ssSess)
                    print('Auto-saved')
            N = s.getNumTurnsToMove()

    def printSSsessStats(s, ssSess):
        print ('\nTurn #{}'.format(ssSess.turnNo))
        print ('Last performance is {:.2f}, game over at turn #{}, game score: {}'.format(
            ssSess.stats['lastPerf'],
            ssSess.stats['lastNumTurn'],
            ssSess.stats['lastScore']))
        print ('So far the best performance is {:.2f}'.format(ssSess.stats['topPerf']))

    def printEvSessStats(s, evSess):
        print ('\nGen #{}'.format(evSess.genNo))
        for a in evSess.topPerfs[:s.configParams['numTopSnaToPrint']]:
            s.printAgentStats(a)
        print ('So far the best performance is {}'.format(evSess.bestAgentPerf))

    def printAgentStats(s, a):
        print(
                'ave {:.2f}, max {:.2f}, min {:.2f}, rng {:.2f}'.format(
                    *a)
                )

    def saveSSsession(s, ssSess):
        d = {'type': ControlHandler.singleSnakeSess, ControlHandler.singleSnakeSess: ssSess}
        s.writeDataToFile(d, s.sessFilePath)

    def saveEvolutionSession(s, evSess):
        d = {'type': ControlHandler.evolutionSess, ControlHandler.evolutionSess: evSess}
        s.writeDataToFile(d, s.sessFilePath)

    def loadSession(s, filePath):
        return s.readDataFromFile(filePath)

    def contSession(s):
        s.sessType = ''
        s.handleSessArgs()
        sess = s.loadSession(s.sessFilePath)
        if sess['type'] == ControlHandler.evolutionSess:
            s.contEvolutionSession(
                    sess[ControlHandler.evolutionSess])
        elif sess['type'] == ControlHandler.singleSnakeSess:
            s.contSingleSnakeSess(
                    sess[ControlHandler.singleSnakeSess])

    def contEvolutionSession(s, evSess):
        s.runEvolutionSession(evSess)
        s.endEvolutionSession(evSess)

    def endSSsession(s, ssSess):
        s.saveSSsession(ssSess)

    def endEvolutionSession(s, evSess):
        s.saveEvolutionSession(evSess)

    def contSingleSnakeSess(s, ssSess):
        s.runSSsession(ssSess)
        s.endSSsession(ssSess)

    def visualize(s):
        s.handleVisualizeArgs()
        evSess = s.loadSession(s.sessFilePath)
        raise Exception(
                "Different possible sessions are not implemented!")
        if s.visAgentRank == -1:
            agentToVis = evSess.bestAgent
        else:
            agentToVis = evSess.agents[s.visAgentRank]

        v = Visualize(agentToVis)
        
        if s.visNewGame:
            print("Not implemented yet.")
        else:
            v.playMovie()

    def handleVisualizeArgs(s):
        argv = s.argv
        s.visAgentRank = 0
        s.visNewGame = False
        # -1 means top rank across all generations,
        # 0 is top in the last generation

        s.configFile = 'snake.conf'
        s.sessFilePath = ''
        i = 2 
        while i < len(argv):
            if argv[i] == '-c':
                s.configFile = argv[i+1]
                i += 1
            elif argv[i].isdigit():
                s.visAgentRank = int(argv[i]) - 1
            elif argv[i] == 'n':
                s.visNewGame = True
            elif s.sessFilePath == '':
                s.sessFilePath = argv[i]
            else:
                raise Exception("Invalid arguments")
            i += 1

        s.configParams = s.getConfigParams()
        configParams = s.configParams
        if s.sessFilePath == '':
            s.sessFilePath = ('trained/agents_{}x{}' + \
                    '_{}_{}_{}_{}_{}.dat').format(
                    configParams['m'],
                    configParams['n'],
                    configParams['numS'],
                    configParams['numTopP'],
                    configParams['numNewB'],
                    configParams['numGamesToAve'],
                    configParams['NNString'])

    def changeParams(s):
        prms = s.handleCPargs()
        s.changeNumSnakesAndTopP(*prms)

    def handleCPargs(s):
        argv = s.argv
        s.configFile = 'snake.conf'
        s.sessFilePath = ''
        i = 2 
        while i < len(argv):
            if argv[i] == '-c':
                s.configFile = argv[i+1]
                i += 1
            elif argv[i].isdigit() or argv[i] == '-':
                newNumS = argv[i]
                newNumTopP = argv[i+1]
                newNumNewB = argv[i+2]
                newNumGamesToAve = argv[i+3]
                i += 3
            elif s.sessFilePath == '':
                s.sessFilePath = argv[i]
            else:
                raise Exception("Invalid arguments")
            i += 1

        s.configParams = s.getConfigParams()
        configParams = s.configParams
        if s.sessFilePath == '':
            s.sessFilePath = ('trained/agents_{}x{}' + \
                    '_{}_{}_{}_{}_{}.dat').format(
                    configParams['m'],
                    configParams['n'],
                    configParams['numS'],
                    configParams['numTopP'],
                    configParams['numNewB'],
                    configParams['numGamesToAve'],
                    configParams['NNString'])
        return (s.sessFilePath, newNumS, newNumTopP, newNumNewB, newNumGamesToAve)

    def changeNumSnakesAndTopP(s, fileName, newNumS, newNumTopP, newNumNewB, newNumGamesToAve):
        evSess = s.loadSession(fileName)
        if newNumS != '-':
            evSess.numS = int(newNumS)
        if newNumTopP != '-': 
            evSess.numTopP = int(newNumTopP)
        if newNumNewB != '-':
            evSess.numNewB = int(newNumNewB)
        if newNumGamesToAve != '-':
            evSess.numGamesToAve = int(newNumGamesToAve)
        s.saveEvolutionSession(evSess)

    def hpo(s): #HyperParameter Optimization
        pass

    def writeDataToFile(s, data, filePath):
        f = open(filePath, 'wb')
        pickle.dump(data, f)
        f.close()

    def readDataFromFile(s, filePath):
        f = open(filePath, 'rb')
        new_d = pickle.load(f)
        f.close()
        return new_d
