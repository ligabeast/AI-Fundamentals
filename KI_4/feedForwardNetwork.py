import math
import matplotlib.pyplot as plt
import numpy as np
from keras.datasets import mnist
import random
import perceptron
import time

class FeedFowardNetwork:
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate, trainingsamples):
        self.input_nodes = inputnodes
        self.hidden_nodes = hiddennodes
        self.output_nodes = outputnodes
        self.learning_rate = learningrate
        self.training_samples = trainingsamples

        #loading the dataset
        #x array, y = number
        (train_X, train_Y), (self.test_X, self.test_Y) = mnist.load_data()

        self.train_Y = []
        self.train_X = []
        for i in range(self.training_samples):
            self.train_X.append(self.imageConverter(np.array(train_X[i],dtype=np.float64).flatten()))
            tmp = np.array([0.01 for i in range(self.output_nodes)], dtype=np.float64)
            tmp[train_Y[i]] = 0.99
            self.train_Y.append(tmp)

        self.train_X = np.array(self.train_X)
        self.train_Y = np.array(self.train_Y)

        self.Wih = np.random.rand(self.input_nodes,self.hidden_nodes)
        self.Who = np.random.rand(self.hidden_nodes,self.output_nodes)

    def sigmoid(self,gamma):
        if gamma < 0:
            return 1.0 - 1.0/(1.0 + np.exp(gamma))
        else:
            return 1.0/(1.0 + np.exp(-gamma))
    
    def sigmoid_derivative(self,x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))
    
    def think(self,inputs):
        H = np.dot(inputs,self.Wih)
        H = np.vectorize(self.sigmoid)(H)
        O = np.dot(H,self.Who)
        O = np.vectorize(self.sigmoid)(O)
        return O, H

    def userMode(self):
        while True:
            for i in range(60000):
                image = np.array(self.test_X[i]).flatten()
                input_vec = self.imageConverter(image)
                self.printImage(image)
                o,h = self.think([input_vec])
                print("Output: ",np.argmax(o))
                input()

    def scorecard(self, it):
        fail = 0
        for i in range(it):
            image = np.array(self.test_X[i]).flatten()
            input_vec = self.imageConverter(np.array(self.test_X[i]).flatten())
            o,h = self.think([input_vec])
            if(np.argmax(o) != self.test_Y[i]):
                fail += 1
        print("After "+str(it)+" Iterations: "+str(1 - fail/it)+"% right decisions")


    def imageConverter(self, image):
        input = np.zeros(len(image),dtype=np.float64)

        divider = 0.99 / 254
        for i in range(len(image)):
            if(image[i] == np.uint8(0)):
                input[i] = 0.01
            else:
                input[i] = image[i] * divider
        return input

    def train(self, N):
        for i in range(N): 

            nn_result, hidden = self.think(self.train_X)

            e_out = self.train_Y - nn_result

            e_hidden = np.dot(e_out,np.transpose(self.Who))

            a = np.vectorize(self.sigmoid_derivative)(nn_result)

            d_who = np.dot(np.transpose(hidden),e_out * np.vectorize(self.sigmoid_derivative)(nn_result))

            self.Who += self.learning_rate * d_who

            d_wih = np.dot(np.transpose(self.train_X),e_hidden * np.vectorize(self.sigmoid_derivative)(hidden))
        
            self.Wih += self.learning_rate * d_wih

    def printImage(self, n):
        image_array = np.asfarray(n).reshape((28,28))
        plt.imshow(image_array,cmap='Greys', interpolation='None')
        plt.show(block = False)


if __name__ == "__main__":
    input_nodes = 784 #28*28 pixel
    hidden_nodes = 200 #voodoo magic number
    output_nodes = 10 #numbers from [0:9]
    training_samples = 1000

    learning_rate = 0.15 #feel free to play around with

    obj = FeedFowardNetwork(input_nodes,hidden_nodes,output_nodes, learning_rate, training_samples)
    obj.train(2000)
    obj.scorecard(1000)
    #obj.userMode()