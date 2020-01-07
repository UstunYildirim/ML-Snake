import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def ReLU(x):
    return np.maximum(x,0)

def identity(x):
    return x

class NNLayer():

    def __init__(s, numInputs, numOutputs, randomize=True, activation = sigmoid):
        s.numInputs = numInputs
        s.numOutputs = numOutputs
        s.activation = activation
        if randomize:
            s.W = np.random.randn(s.numOutputs, s.numInputs)*np.sqrt(2/s.numInputs)
            s.bias = np.zeros((s.numOutputs, 1))
        else:
            s.W = np.zeros((s.numOutputs, s.numInputs))
            s.bias = np.zeros((s.numOutputs, 1))
        s.cache = {}

    def forwardPropogate(s, inp):
        inp = inp.reshape(s.numInputs,1)
        z = np.dot(s.W,inp)+s.bias
        s.cache['Aprev'] = inp
        s.cache['Z'] = z
        a = s.activation(z)
        s.cache['A'] = a
        return np.array(a).flatten()

    def backwardPropogate(s, dA):
        z = s.cache['Z']
        if s.activation == identity:
            gpz = z
        elif s.activation == sigmoid:
            a = s.cache['A']
            gpz = np.multiply(np.square(a),np.exp(-z))
        elif s.activation == ReLU:
            gpz = (z>0).astype(int)
        elif s.activation == np.tanh:
            gpz = np.square(2/(np.exp(z)+np.exp(-z)))
        else:
            raise Exception('Not implemented')
        dZ = np.multiply(gpz, dA)
        aPrev = s.cache['Aprev']
        dW = np.dot(dZ, aPrev.T)
        db = np.copy(dZ)
        dAprev = np.dot(s.W.T,dZ)
        s.cache['dW'] = dW
        s.cache['db'] = db
        return dAprev

    def updateParams(s, learningRate = 0.001):
        s.W    = s.W    - learningRate * s.cache['dW']
        s.bias = s.bias - learningRate * s.cache['db']
    
    def randomVariation(s, varMagnitude=0.01):
        deltaW = np.random.randn(s.numOutputs,s.numInputs)
        deltaW = deltaW*varMagnitude
        deltaBias = np.random.randn(s.numOutputs, 1)*varMagnitude
        s.W += deltaW
        s.bias += deltaBias
        
