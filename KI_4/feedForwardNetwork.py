import math
import matplotlib.pyplot as plt
import numpy as np
from keras.datasets import mnist
import random
import perceptron
import time

class FeedFowardNetwork:
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        self.input_nodes = inputnodes
        self.hidden_nodes = hiddennodes
        self.output_nodes = outputnodes
        self.learning_rate = learningrate

        #loading the dataset
        #x array, y = number
        (self.train_X, self.train_Y), (self.test_X, self.test_Y) = mnist.load_data()

        self.Wih = np.array([[random.random() for e in range(self.input_nodes)] for e in range(self.hidden_nodes)])
        self.Who = np.array([[random.random() for e in range(self.hidden_nodes)] for e in range(self.output_nodes)])

    def sigmoid(self,x):
        return 1 / (1 + math.exp(-x))
    
    def sigmoid_derivative(self,x):
        sigmoid_output = np.zeros(len(x))
        for i in range(len(x)):
            sigmoid_output[i] = self.sigmoid(x[i]) * (1 - self.sigmoid(x[i]))
        return sigmoid_output
    
    def think(self,input):
        self.H = self.Wih.dot(input)
        for i in range(len(self.H)):
            self.H[i] = self.sigmoid(self.H[i])
        self.O = self.Who.dot(self.H)
        for i in range(len(self.O)):
            self.O[i] = self.sigmoid(self.O[i])
        return self.O

    def userMode(self):
        while True:
            for i in range(60000):
                image = np.array(self.test_X[i]).flatten()
                print("Output: ", max(self.think(image)))
                time.sleep(3)

    def train(self, N):
        for i in range(N):
            image = np.array(self.train_X[i]).flatten()

            result = self.train_Y[i]
            result_vec = np.zeros(self.output_nodes)
            result_vec[result] = 1

            nn_result_vec = self.think(image)
            nn_result = max(nn_result_vec)

            e_out = np.zeros(self.output_nodes)
            for i in range(self.output_nodes):
                e_out[i] = result_vec[i] - nn_result_vec[i]

            e_hidden = np.dot(np.transpose(self.Who),e_out)

            d_who = np.dot(np.dot(e_out, self.sigmoid_derivative(nn_result_vec)), np.transpose(self.H))

            for o in range(self.output_nodes):
                for h in range(self.hidden_nodes):
                    self.Who[o][h] += self.learning_rate * d_who[h]

            d_wih = (np.dot(e_hidden, self.sigmoid_derivative(self.H)), np.transpose(image))
            
            for h in range(self.hidden_nodes):
                for i in range(self.input_nodes):
                    self.Wih[h][i] += self.learning_rate * d_wih[1][i]

    def printImage(self, n):
        image_array = np.asfarray(n).reshape((28,28))
        plt.imshow(image_array,cmap='Greys', interpolation='None')
        plt.show(block = False)


if __name__ == "__main__":
    input_nodes = 784 #28*28 pixel
    hidden_nodes = 200 #voodoo magic number
    output_nodes = 10 #numbers from [0:9]

    learning_rate = 0.1 #feel free to play around with

    obj = FeedFowardNetwork(input_nodes,hidden_nodes,output_nodes, learning_rate)
    print("HEY")
    obj.train(100)
    obj.userMode()