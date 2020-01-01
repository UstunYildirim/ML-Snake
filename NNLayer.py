import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def ReLU(x):
    return np.maximum(x,0)

def identity(x):
    return x

class NNLayer():

    def __init__(s, numInputs, numOutputs, randomize=True, threshold=0.5, mu=0, sigma=1, activation = sigmoid):
        s.numInputs = numInputs
        s.numOutputs = numOutputs
        s.threshold = threshold
        s.activation = activation
        if randomize:
            s.theta = np.random.randn(s.numOutputs, s.numInputs)*sigma+mu
            s.bias = np.zeros((s.numOutputs, 1))
        else:
            s.theta = np.zeros((s.numOutputs, s.numInputs))
            s.bias = np.zeros((s.numOutputs, 1))

    def forwardPropogate(s, inp):
        inp = inp.reshape(s.numInputs,1)
        z = np.dot(s.theta,inp)+s.bias
        return np.array(s.activation(z)).flatten()

    def predict (s, inp):
        return s.forwardPropogate(inp)>=s.threshold
    
    def randomVariation(s, varMagnitude=0.01):
        deltaTheta = np.random.randn(s.numOutputs,s.numInputs)
        deltaTheta = deltaTheta*varMagnitude
        deltaBias = np.random.randn(s.numOutputs, 1)*varMagnitude
        s.theta += deltaTheta
        s.bias += deltaBias
        
