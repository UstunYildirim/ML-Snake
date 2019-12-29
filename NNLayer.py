import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def ReLU(x):
    return np.maximum(x+1,0)

class NNLayer():

    def __init__(s, numInputs, numOutputs, randomize=True, threshold=0.5, valMin=-1, valMax=1, activation = np.tanh):
        s.numInputs = numInputs
        s.numOutputs = numOutputs
        s.threshold = threshold
        s.activation = activation
        if randomize:
            rng = valMax - valMin
            avg = 0.5*(valMax+valMin)
            s.theta = (np.random.rand(s.numInputs,s.numOutputs)*rng)-avg
            s.bias = np.random.rand()
        else:
            s.theta = np.zeros((s.numInputs,s.numOutputs))
            s.bias = 0

    def forwardPropogate(s, inp):
        z = np.dot(inp, s.theta)+s.bias
        return np.array(s.activation(z)).flatten()

    def predict (s, inp):
        return s.forwardPropogate(inp)>=s.threshold
    
    def randomVariation(s, varMagnitude=1):
        deltaTheta = (np.random.rand(s.numInputs,s.numOutputs)*2)-1
        deltaTheta = deltaTheta*varMagnitude
        deltaBias = np.random.rand()*2-1
        deltaBias = deltaBias*varMagnitude
        s.theta += deltaTheta
        s.bias += deltaBias
        
