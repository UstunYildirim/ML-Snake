#! /usr/bin/python3
import os, sys
from ControlHandler import *

man = """Example Usage:
To try single player mode on a 7 by 10 board
    Main.py -SP 7 10

To start new single snake learning session (this mode is work in progress) based on default config file:
    Main.py -Nss

To start new evolution session based on default config file:
    Main.py -Ne

To start new evolution session with all-nighter mode and autosaving every 30 turns:
    Main.py -Ne -an+30

To start a new evolution session with given config file:
    Main.py -Ne -c snake.conf

To continue from saved data with all-nighter mode enabled:
    Main.py -L trained/agents_20x40.dat -an

To change parameters of a saved data:
    Main.py -CP trained/agents_20x40.dat 100 20 4 2
    This will make the following change:
        number_of_snakes: 100
        number_of_top_performers: 20
        number_of_new_borns: 4
        number_of_games_to_average: 2

To omit some of these changes use -:
    python3 Main.py -CP trained/agents_20x40.dat - 20 - -

To see the top performer's (of the last generation) game play:
    python3 Main.py -V trained/agents_20x40.dat

To see the third top performer (of the last generation) play a new game:
    python3 Main.py -V trained/agents_20x40.dat 3 n

To see the top performer's (across all generations) game play :
    python3 Main.py -V trained/agents_20x40.dat 0"""


class Main():

    singPlayerMode    = 1
    newEvSessMode     = 2
    contSessMode      = 3
    visualizeMode     = 4
    changeParamsMode  = 5
    hyperParamOptMode = 6
    newSSsessMode     = 7
            

    def readArgs(s, argv):
        try:
            if len(argv) == 1:
                raise Exception()
            elif argv[1] == '-h' or \
                argv[1] == '--help':
                    raise Exception()
            elif argv[1] == '-SP':
                s.mode = Main.singPlayerMode
            elif argv[1] == '-Ne':
                s.mode = Main.newEvSessMode
            elif argv[1] == '-Nss':
                s.mode = Main.newSSsessMode
            elif argv[1] == '-L':
                s.mode = Main.contSessMode
            elif argv[1] == '-V':
                s.mode = Main.visualizeMode
            elif argv[1] == '-CP':
                s.mode = Main.changeParamsMode
            elif argv[1] == '-HPO':
                s.mode = Main.hyperParamOptMode
            else:
                raise Exception()
        except Exception:
            s.invalidArguments()

    def invalidArguments(s):
        print(man)
        exit()

    def main(s,argv):
        controlHandler = ControlHandler(argv)
        s.readArgs(argv)
        if s.mode == Main.singPlayerMode:
            controlHandler.singlePlayer()
        elif s.mode == Main.newEvSessMode:
            controlHandler.newEvolutionSession()
        elif s.mode == Main.newSSsessMode:
            controlHandler.newSSsession()
        elif s.mode == Main.contSessMode:
            controlHandler.contSession()
        elif s.mode == Main.visualizeMode:
            controlHandler.visualize()
        elif s.mode == Main.changeParamsMode:
            controlHandler.changeParams()
        elif s.mode == Main.hyperParamOptMode:
            controlHandler.hpo()
        else:
            s.invalidArguments()

        

if __name__ == '__main__':
    Main().main(sys.argv)

