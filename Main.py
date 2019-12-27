#! /usr/bin/python
import os, select, sys
from Agent import *
from DataHandler import changeNumSnakesAndTopP
from copy import deepcopy
from heapq import nlargest
from sys import argv

# create S random snakes
# make them play the game
# pick the top K that performed the best
# replace them with random "small" variations of them (each gets replaced by about S/K snakes)
# run a generation, return statistics and ask user if they want to continue

man = """Example Usage:
For new session based on default config file:
    Main.py -N
For a new session with given config file:
    Main.py -c snake.conf
To continue from saved data with all-nighter mode enabled:
    Main.py -l trained/agents_20x40.dat -an
To change parameters of a saved data:
    Main.py -CP trained/agents_20x40.dat 100 20"""

class Main():

    def readConfigFile(s, fileName = 'snake.conf'):
        s.numS = 100
        s.numTopP = 10
        s.m = 10
        s.n = 10
        f = open(fileName, 'r')
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
        f.close()

    def createBrandNewSnakes(s,m,n,k):
        s.genNo = 0
        for i in range(k):
            s.agents.append(Agent(Game(m,n,1),-20,20))

    def simHelper(s,a):
        return a.finishTheGame()

    def simulateGenerationAndPurge(s):
        for a in s.agents:
            a.finishTheGame() 
        s.agents = nlargest(s.numTopP,
                s.agents,
                key = lambda a: a.performanceEvaluation())

    def evolveAndMultiply(s):
        topPerfs = [a.performanceEvaluation() for a in s.agents]
        for a in s.agents:
            a.newGame(Game(s.m,s.n,1))

        s.createBrandNewSnakes(s.m,s.n,int(s.numTopP/2))

        numSpotsToBeFilled = s.numS-len(s.agents)
        perfSum = np.sum(topPerfs)
        #NOT SUPER CLEAN
        for i in range(s.numTopP):
            numCopies = int(topPerfs[i]/perfSum*numSpotsToBeFilled)
            newA = [deepcopy(s.agents[i]) for x in range(numCopies)]
            for a in newA:
                a.randomVariation(i/s.numTopP + 0.01)
            s.agents += newA

        i = 0
        while len(s.agents) < s.numS:
            a = deepcopy(s.agents[i])
            a.randomVariation()
            s.agents.append(a)
            i = (i+1)%s.numTopP
    
    def readArgs(s, argv):
        s.anMode = False # all-nighter mode
        s.configFile = 'snake.conf'
        s.loadAndContFromFile = None
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
                elif argv[i] == '-CP':
                    changeNumSnakesAndTopP(argv[i+1], int(argv[i+2]), int(argv[i+3]))
                    exit() # we can generalize this condition but it is currently safer to quit
                    i += 4
                    continue
                else:
                    break
        except Exception:
            print(man)
            exit()


    def saveData(s):
        d = {}
        d['m'] = s.m
        d['n'] = s.n
        d['numS'] = s.numS
        d['numTopP'] = s.numTopP
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
        s.readConfigFile(s.configFile)
        s.agents = []
        s.createBrandNewSnakes(s.m,s.n,s.numS)

    def simulationMain(s):
        try:
            N = int(input("Enter the number of generations to simulate\n"))
        except:
            N = 1
        while True:
            s.genNo += 1
            s.simulateGenerationAndPurge()
            print('\n\n Top Scores of Gen ', s.genNo, ': ', [a.performanceEvaluation() for a in s.agents[0:s.numTopP]], '\n')
            N -= 1
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
                    print("\n\nTop Agents of Gen ", s.genNo, ":\n\n")
                    for a in s.agents[0:s.numTopP]:
                        a.printAgentInfo()
                    s.saveData()
                    exit()
            s.evolveAndMultiply()

    def main(s,argv):
        s.readArgs(argv)
        if s.loadAndContFromFile != None:
            s.loadAndContinue()
        else:
            s.newTrainingSession()
        s.simulationMain()


if __name__ == '__main__':
    m = Main()
    m.main(argv)
