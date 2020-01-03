import sys, select, pickle
from NNLayer import ReLU, sigmoid, identity
from Visualize import Visualize
from SinglePlayer import SinglePlayer
from TrainingSession import *


class ControlHandler():

    def __init__(s, argv):
        s.argv = argv

    def singlePlayer(s):
        #TODO: MVC should be reconsidered here
        # also visualize class will change!
        m = int(s.argv[2])
        n = int(s.argv[3])
        sp = SinglePlayer(m,n)
        sp.Play()

    def handleTrSessArgs(s):
        argv = s.argv
        s.anMode = False
        s.autoSaveEnabled = False
        s.configFile = 'snake.conf'
        s.trSessFilePath = ''
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
            elif s.trSessFilePath == '':
                s.trSessFilePath = argv[i]
            else:
                raise Exception("Invalid arguments")
            i += 1

        s.configParams = s.getConfigParams()
        configParams = s.configParams
        if s.trSessFilePath == '':
            s.trSessFilePath = ('trained/agents_{}x{}' + \
                    '_{}_{}_{}_{}_{}.dat').format(
                    configParams['m'],
                    configParams['n'],
                    configParams['numS'],
                    configParams['numTopP'],
                    configParams['numNewB'],
                    configParams['numGamesToAve'],
                    configParams['NNString'])
        if s.autoSaveEnabled and s.autoSaveFreq == 0:
            s.autoSaveFreq = s.configParams['autoSaveFreq']

    def newTrainingSession(s):
        s.handleTrSessArgs()
        trSess = TrainingSession()
        trSess.newSession(s.configParams)
        s.runTrainingSession(trSess)
        s.endTrainingSession(trSess)

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
        f.close()
        return confParams

    def __parseNNStr__(s, txt):
        txt = txt.replace('t', 'np.tanh')
        txt = txt.replace('s', 'sigmoid')
        txt = txt.replace('r', 'ReLU')
        txt = txt.replace('i', 'identity')
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

    def runTrainingSession(s, trSess):
        N = s.getNumGensToSimulate()
        while N > 0:
            while N > 0:
                trSess.simulateOneGeneration()
                trSess.pickTopAgents()
                trSess.purgeAndMultiply()

                s.printTrSessStats(trSess)
                N -= 1
                if s.autoSaveEnabled and (trSess.genNo % s.autoSaveFreq == 0):
                    s.saveTrainingSession(trSess)
                    print('Auto-saved')
            N = s.getNumGensToSimulate()

    def printTrSessStats(s, trSess):
        print ('\nGen #{}'.format(trSess.genNo))
        for a in trSess.topPerfs[:s.configParams['numTopSnaToPrint']]:
            s.printAgentStats(a)
        print ('So far the best performance is {}'.format(trSess.bestAgentPerf))

    def printAgentStats(s, a):
        print(
                'ave {:.2f}, max {:.2f}, min {:.2f}, rng {:.2f}'.format(
                    *a)
                )

    def saveTrainingSession(s, trSess):
        s.writeDataToFile(trSess, s.trSessFilePath)

    def loadTrainingSession(s, filePath):
        return s.readDataFromFile(filePath)

    def contTrainingSession(s):
        s.handleTrSessArgs()
        trSess = s.loadTrainingSession(s.trSessFilePath)
        s.runTrainingSession(trSess)
        s.endTrainingSession(trSess)

    def endTrainingSession(s, trSess):
        s.saveTrainingSession(trSess)

    def visualize(s):
        s.handleVisualizeArgs()
        trSess = s.loadTrainingSession(s.trSessFilePath)
        if s.visAgentRank == -1:
            agentToVis = trSess.bestAgent
        else:
            agentToVis = trSess.agents[s.visAgentRank]

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
        s.trSessFilePath = ''
        i = 2 
        while i < len(argv):
            if argv[i] == '-c':
                s.configFile = argv[i+1]
                i += 1
            elif argv[i].isdigit():
                s.visAgentRank = int(argv[i]) - 1
            elif argv[i] == 'n':
                s.visNewGame = True
            elif s.trSessFilePath == '':
                s.trSessFilePath = argv[i]
            else:
                raise Exception("Invalid arguments")
            i += 1

        s.configParams = s.getConfigParams()
        configParams = s.configParams
        if s.trSessFilePath == '':
            s.trSessFilePath = ('trained/agents_{}x{}' + \
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
        s.trSessFilePath = ''
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
            elif s.trSessFilePath == '':
                s.trSessFilePath = argv[i]
            else:
                raise Exception("Invalid arguments")
            i += 1

        s.configParams = s.getConfigParams()
        configParams = s.configParams
        if s.trSessFilePath == '':
            s.trSessFilePath = ('trained/agents_{}x{}' + \
                    '_{}_{}_{}_{}_{}.dat').format(
                    configParams['m'],
                    configParams['n'],
                    configParams['numS'],
                    configParams['numTopP'],
                    configParams['numNewB'],
                    configParams['numGamesToAve'],
                    configParams['NNString'])
        return (s.trSessFilePath, newNumS, newNumTopP, newNumNewB, newNumGamesToAve)

    def changeNumSnakesAndTopP(s, fileName, newNumS, newNumTopP, newNumNewB, newNumGamesToAve):
        trSess = s.loadTrainingSession(fileName)
        if newNumS != '-':
            trSess.numS = int(newNumS)
        if newNumTopP != '-': 
            trSess.numTopP = int(newNumTopP)
        if newNumNewB != '-':
            trSess.numNewB = int(newNumNewB)
        if newNumGamesToAve != '-':
            trSess.numGamesToAve = int(newNumGamesToAve)
        s.saveTrainingSession(trSess)

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
