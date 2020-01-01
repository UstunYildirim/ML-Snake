from DataHandler import changeNumSnakesAndTopP
from copy import deepcopy
from heapq import nlargest
from Visualize import Visualize
from SinglePlayer import SinglePlayer

class ControlHandler():

    def __init__(s, argv):
        s.argv = argv

    def singlePlayer(s):
        #TODO: MVC should be implemented here
        # also visualize class will change!
        m = int(s.argv[2])
        n = int(s.argv[3])
        sp = SinglePlayer(m,n)
        sp.Play()

    def handleNewTrSessArgs(s):
        s.anMode = False
        s.autoSaveEnabled = False
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
        configParams = s.getConfigParams()
        if s.autoSaveEnabled and s.autoSaveFreq == 0:
            s.autoSaveFreq = configParams['autoSaveFreq']

    def newTrainingSession(s):
        s.handleNewTrSessArgs()
        trSess = TrainingSession()
        trSess.newSession(configParams)

    def visualize(s):
        d = readDataFromFile(s.visualizeFN)
        agents = d['agents']
        topAgent = agents[s.snakeNoToVis]
        v = Visualize(topAgent)
        
        if s.visNewGame:
            pass
        else:
            v.playMovie()

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
            elif a == 'auto_save_freq':
                confParams['autoSaveFreq'] = int(b)
        f.close()
        return confParams
