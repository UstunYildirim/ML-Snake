#! /usr/bin/python3
import os, select, sys
from Agent import *
from DataHandler import changeNumSnakesAndTopP
from copy import deepcopy
from heapq import nlargest
from sys import argv
from Visualize import Visualize
from SinglePlayer import SinglePlayer

# create S random snakes
# make them play the game
# pick the top K that performed the best
# replace them with random "small" variations of them (each gets replaced by about S/K snakes)
# run a generation, return statistics and ask user if they want to continue

man = """Example Usage:
To try single player mode
    python3 Main.py -SP 7 10

To start new session based on default config file:
    python3 Main.py -N

To start new session with all-nighter mode and autosaving:
    python3 Main.py -an+ -N

To start a new session with given config file:
    python3 Main.py -c snake.conf

To continue from saved data with all-nighter mode enabled:
    python3 Main.py -l trained/agents_20x40.dat -an

To change parameters of a saved data:
    python3 Main.py -CP trained/agents_20x40.dat 100 20 4 2
    This will make the following change:
        number_of_snakes: 100
        number_of_top_performers: 20
        number_of_new_borns: 4
        number_of_games_to_average: 2

To omit some of these changes use -:
    python3 Main.py -CP trained/agents_20x40.dat - 20 - -

To see the top performer's game play:
    python3 Main.py -V trained/agents_20x40.dat

To see the third top performer's game play:
    python3 Main.py -V trained/agents_20x40.dat 3"""


class Main():

    def readConfigFile(s):
        s.numS = 100
        s.numTopP = 10
        s.m = 10
        s.n = 10
        f = open(s.configFile, 'r')
        for l in f:
            if not ':' in l:
                continue
            (a,b) = l.split(':')
            a = a.strip()
            b = b.strip()
            if a == 'board_height':
                s.m = int(b)
            elif a == 'board_width':
                s.n = int(b)
            elif a == 'number_of_snakes':
                s.numS = int(b)
            elif a == 'number_of_top_performers':
                s.numTopP = int(b)
            elif a == 'number_of_new_borns':
                s.numNewBorns = int(b)
            elif a == 'number_of_games_to_average':
                s.numGamesToAve = int(b)
        f.close()

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

        s.createBrandNewSnakes(s.m,s.n,s.numNewBorns)

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
    
    def readArgs(s, argv):
        s.anMode = False # all-nighter mode
        s.anAutoSave = 0
        s.configFile = 'snake.conf'
        s.loadAndContFromFile = None
        s.visualizeFN = None
        s.singlePlayer = False
        s.visNewGame = False 
        s.snakeNoToVis = 0

        try:
            if len(argv) == 1:
                raise Exception()
            i = 1
            while i < len(argv):
                if argv[i] == '-N':
                    return
                elif argv[i] == '-c':
                    s.configFile = argv[i+1]
                    i += 2
                    continue
                elif argv[i] == '-l':
                    s.loadAndContFromFile = argv[i+1]
                    i += 2
                    continue
                elif argv[i] == '-an': # all-nighter mode
                    s.anMode = True
                    i += 1
                    continue
                elif argv[i] == '-an+': # all-nighter mode with auto-save
                    s.anMode = True
                    s.anAutoSave = 40
                    i += 1
                    continue
                elif argv[i] == '-CP':
                    changeNumSnakesAndTopP(argv[i+1], argv[i+2], argv[i+3], argv[i+4], argv[i+5])
                    exit() # we can generalize this condition but it is currently safer to quit
                    i += 4
                    continue
                elif argv[i] == '-V':
                    s.visualizeFN = argv[i+1]
                    if i+4 == len(argv): # both the rank and 'R' option are given
                        s.snakeNoToVis = int(argv[i+2]) - 1
                        if argv[i+3] == 'R':
                            s.visNewGame = True #TODO
                    if i+3 == len(argv):
                        if argv[i+2] == 'R':
                            s.visNewGame = True
                        else:
                            s.snakeNoToVis = int(argv[i+2]) - 1
                    return
                elif argv[i] == '-SP':
                    s.singlePlayer = True
                    s.m = int(argv[i+1])
                    s.n = int(argv[i+2])
                    return
                else:
                    break
        except Exception:
            print(man)
            exit()

    def visualize(s):
        d = readDataFromFile(s.visualizeFN)
        agents = d['agents']
        topAgent = agents[s.snakeNoToVis]
        v = Visualize(topAgent)
        
        if s.visNewGame:
            pass
        else:
            v.playMovie()

    def saveData(s):
        d = {}
        d['m'] = s.m
        d['n'] = s.n
        d['numS'] = s.numS
        d['numTopP'] = s.numTopP
        d['numNewBorns'] = s.numNewBorns
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
        s.numNewBorns = d['numNewBorns']
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

    def main(s,argv):
        s.readArgs(argv)
        if s.loadAndContFromFile is not None:
            s.loadAndContinue()
        elif s.visualizeFN is not None:
            s.visualize()
            exit()
        elif s.singlePlayer:
            sp = SinglePlayer(s.m, s.n)
            sp.Play()
            exit()
        else:
            s.newTrainingSession()
        s.simulationMain()


if __name__ == '__main__':
    m = Main()
    m.main(argv)
