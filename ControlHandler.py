import numpy as np
import select, pickle
from NNLayer import ReLU, sigmoid, identity
from copy import deepcopy
from heapq import nlargest
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

    def handleNewTrSessArgs(s):
        argv = s.argv
        s.anMode = False
        s.autoSaveEnabled = False
        s.configFile = 'snake.conf'
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
            else:
                raise Exception("Invalid arguments")
            i += 1
        s.configParams = s.getConfigParams()
        if s.autoSaveEnabled and s.autoSaveFreq == 0:
            s.autoSaveFreq = s.configParams['autoSaveFreq']

    def newTrainingSession(s):
        s.handleNewTrSessArgs()
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
                confParams['NNString'] = b
                confParams['NNStructure'] = s.__parseNNStr__(b)
            elif a == 'auto_save_freq':
                confParams['autoSaveFreq'] = int(b)
        f.close()
        return confParams

    def __parseNNStr__(s, txt):
        txt = txt.replace('t', 'np.tanh')
        txt = txt.replace('s', 'sigmoid')
        txt = txt.replace('r', 'ReLU')
        txt = txt.replace('i', 'identity')
        return eval(txt)

    def getNumTurnsToSimulate(s):
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
        while True:
            N = s.getNumTurnsToSimulate()
            if N < 1:
                break
            N -= 1
            trSess.genNo += 1

    def __shortenNNString__(s, NNStr):
        t = 't'
        s = 's'
        r = 'r'
        i = 'i'
        return ''.join(map(lambda p:str(p[0])+p[1], eval(NNStr)))

    def saveTrainingSession(s,
            trSess,
            folder='trained',
            fileNamePrefix='agents'):
        strNNStr = s.__shortenNNString__(trSess.NNString)
        s.writeDataToFile(trSess,
                '{}/{}_{}x{}_{}_{}_{}_{}_{}.dat'.format(
                    folder,
                    fileNamePrefix,
                    trSess.m,
                    trSess.n,
                    trSess.numS,
                    trSess.numTopP,
                    trSess.numNewB,
                    trSess.numGamesToAve,
                    strNNStr))


    def endTrainingSession(s, trSess):
        s.saveTrainingSession(trSess)

    def visualize(s):
        d = readDataFromFile(s.visualizeFN)
        agents = d['agents']
        topAgent = agents[s.snakeNoToVis]
        v = Visualize(topAgent)
        
        if s.visNewGame:
            pass
        else:
            v.playMovie()

    def writeDataToFile(s, data, fileName):
        f = open(fileName, 'wb')
        pickle.dump(data, f)
        f.close()

    def readDataFromFile(s, fileName):
        f = open(fileName, 'rb')
        new_d = pickle.load(f)
        f.close()
        return new_d
