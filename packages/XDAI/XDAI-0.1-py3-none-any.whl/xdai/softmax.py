# importing the dataset
import numpy as np
from urllib.request import urlopen



def predict(W, b, x):
    return softmax(W.dot(x) + b[:, None])


#defind the softmax function:
def softmax(v):
    return np.exp(v)*np.sum(np.exp(v), axis = 0)[None, :]**-1

# make random firts guess arrays for waights and biases

def one_hot(targets):
    """
    One-hot encoding
    See [source] for info
    Author: Hanan Gharayba, 2023
    """
    targets -= targets.min()
    categories = int(targets.max() + 1)

    oh = np.zeros((len(targets), categories), dtype = int)

    for i in range(len(targets)):
        oh[i, int(targets[i])] = 1

    return oh


def cross_entropy(target,prediction):
  """
  Cross entropy loss function

  """
  return - np.sum(target*np.log(prediction))

def total_loss(features,  targets, regressor):
  """
  """
  return cross_entropy(targets, regressor.predict(features.T).T)


class softmax_regressor():
    def __init__(self, dim):
        self.weights = np.random.normal(0,.1, dim)
        self.bias = np.random.normal(0,.1,dim[0])

    def predict(self, features):
        return predict(self.weights, self.bias, features)

def train_regressor(features, targets, regressor, ds = 0.01, T = 100):
    objective_i = total_loss(features, targets, sm)
    for i in range(100000):
        Wi, bi = regressor.weights*1, regressor.bias*1
        regressor.weights += ds*np.random.normal(0,1, regressor.weights.shape)
        regressor.bias += ds*np.random.normal(0,1, regressor.bias.shape)
        objective_i_next = total_loss(features, targets, regressor)
        #print("test")
        if objective_i_next<objective_i:
            # accept move and update regressor
            objective_i = objective_i_next
            #print(objective_i)
        else:
            if np.exp(-(objective_i_next-objective_i)/T)>0.8:

                objective_i = objective_i_next

            else:
                regressor.weights= Wi
                regressor.bias = bi
        if i%1000==0:
            print(objective_i, T)
        T *= 0.999

    return regressor
