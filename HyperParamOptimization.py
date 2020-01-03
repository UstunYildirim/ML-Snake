from TrainingSession import *

class HyperParamOptimization():

    def __init__(s, m, n numSs, ratioTopPs, ratioNewBs, numGamesToAves, NNStructures):
        s.m = m # the board size is not an hyper parameter!
        s.n = n # the board size is not an hyper parameter!
        s.numSs = numSs
        s.ratioTopPs = ratioTopPs # ratio to numS (e.g. 0.1 = 10% of numS)
        s.ratioNewBs = ratioNewBs # ratio to numS (e.g. 0.1 = 10% of numS)
        s.numGamesToAves = numGamesToAves
        s.NNStructures = NNStructures # This is a list of pairs (hidden_layer_size, activation_function)
        # The last layer always ends with the identity function and 4 outputs

    def runItAll(s, mins):
        for numS in s.numSs:
            for ratioTopP in s.ratioTopPs:
                for ratioNewB in s.ratioNewBs:
                    for numGamesToAve in s.numGamesToAves:
                        for NNStructure in s.NNStructures:
                            params = {}
                            params['m'] = s.m
                            params['n'] = s.n
                            params['numS'] = numS
                            params['numTopP'] = int(numS*ratioTopP)
                            params['numNewB'] = int(numS*ratioNewB)
                            params['numGamesToAve'] = numGamesToAve
                            params['NNStructure'] = NNStructure
                            s.runSingleTrSessHyperParams(params, mins)

    def runSingleTrSessHyperParams(s, params, mins):
        trainingSession = TrainingSession(s, params)
