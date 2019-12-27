import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def ReLU(x):
    return np.maximum(x+1,0)

class NNLayer():

    def __init__(s, numInputs, numOutputs, randomize=True, threshold=0.5, valMin=-1, valMax=1, sigmoid = sigmoid):
        s.numInputs = numInputs
        s.numOutputs = numOutputs
        s.threshold = threshold
        s.sigmoid = sigmoid
        if randomize:
            rng = valMax - valMin
            avg = 0.5*(valMax+valMin)
            s.theta = np.matrix((np.random.rand(s.numInputs+1,s.numOutputs)*rng)-avg)
        else:
            s.theta = np.matrix(np.zeros((s.numInputs+1,s.numOutputs)))

    def augInp(s, inp):
        return np.concatenate((np.array([1]),inp))

    def forwardPropogate(s, inp):
        augInp = s.augInp(inp)
        z = augInp * s.theta
        return np.array(s.sigmoid(z)).flatten()

    def predict (s, inp):
        return s.forwardPropogate(inp)>=s.threshold
    
    def randomVariation(s, varMagnitude=1):
        deltaTheta = (np.random.rand(s.numInputs+1,s.numOutputs)*2)-1
        deltaTheta = np.matrix(deltaTheta*varMagnitude)
        s.theta += deltaTheta
        
