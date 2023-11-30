import math
import numpy
import random

class perceptron:
    def __init__(self,inputs,outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.N = len(inputs)
        self.M = len(inputs[0])
        # zeilen N , spalten M

        self.weights = numpy.array([random.randint(-10,10) for i in range(self.M)])

    def sigmoid(self,x):
        return 1 / (1 + math.exp(-x))
    def sigmoid_derivative(self,x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))
    def think(self,input):
        result = numpy.dot(input,self.weights)
        return self.sigmoid(result)
    def userMode(self):
        test = numpy.zeros(self.M)
        while True:
            for i in range(self.M):
                test[i] = input("I"+ str(i+1) +": ")
            print("Output: ", self.think(test))
    def train(self, N):
        # O = S (I x W)
        index  = 0
        for iteration in range(N):
            for input in self.inputs:
                output = self.think(input)
                error = self.outputs[index] - output
                derived_sigmoid = self.sigmoid_derivative(output) 
                dW = numpy.dot(error * derived_sigmoid, input)
                self.weights = numpy.add(self.weights, dW)
                index += 1
            index = 0
        print('Weights: ')
        for i in self.weights:
            print(i)


if __name__ == "__main__":
    obj = perceptron(
        numpy.array([[0,0,1],
                     [1,1,1],
                     [1,0,0],
                     [0,1,1]]),
                    numpy.array([0,1,1,0])
                    )
    obj.train(1000000)
    obj.userMode()