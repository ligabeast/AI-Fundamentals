import math
import pygame
import random

# set color with rgb
white, black, red, gray = (255, 255, 255), (0, 0, 0), (255, 0, 0), (100, 100, 100)

# Best Settings
# boardLength = 8
# initialPopulation = 500
# mutation = 0.3
# selectionFactor = 10 #higher -> select better parent
# maxIteration = 100
# prioritySize = 250

boardLength = 8
initialPopulation = 500
mutation = 0.3
selectionFactor = 10 #higher -> select better parent
maxIteration = 100
prioritySize = 250

screenSize = (boardLength * 100, boardLength * 100)
# Size of squares
size = 80

class PriorityQueue:
    def __init__(self, max):
        self.structeredData = list()
        self.max = max

    def push(self, data):
        index = 0
        if(self.contains(data)):
            return
        while (index < len(self.structeredData) and 
               self.structeredData[index][0] < data[0]):
            index += 1
        if (index >= len(self.structeredData)):
            self.structeredData.append(data)
        else:
            self.structeredData.insert(index, data)
        if(len(self.structeredData) > self.max):
            self.structeredData.pop()

    def pop(self,index = 0):
        if (not self.structeredData):  # empty Queue
            print('Queue is empty!!')
            return None
        else:
            return self.structeredData.pop(index)
    def get(self,index):
        if (not self.structeredData):  # empty Queue
            print('Queue is empty!!')
            return None
        else:
            return self.structeredData[index]
        
    def size(self):
        return len(self.structeredData)

    def empty(self):
        return (not self.structeredData)

    def contains(self, val):
        return val in self.structeredData

class Field:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = white
        self.queen = False

    def setBlack(self):
        self.color = black

    def setWhite(self):
        self.color = white

    def setQueen(self):
        self.queen = True

    def disableQueen(self):
        self.queen = False

    def isWhite(self):
        return self.color == white

    def isBlack(self):
        return self.color == black

    def isQueen(self):
        return self.queen

class Board:
    def __init__(self, queenPositions, queenQuantitys):
        self.board = [[0]*boardLength for i in range(boardLength)]
        self.initialzeFields()

    def selectionParent(self):
        randomValue = random.randint(0,prioritySize)
        index = (randomValue ** selectionFactor) * ((prioritySize - 1)/(prioritySize ** selectionFactor))
        return int(index)

    def initialzeFields(self):
        # board length, must be even
        cnt = 0
        for row in range(boardLength):
            for col in range(boardLength):
                self.board[row][col] = Field(row, col)
                if cnt % 2 == 0:
                    self.board[row][col].setBlack()
                cnt += 1
            # since theres an even number of squares go back one value
            cnt -= 1

    def getThreadiningRow(self):
        counter = 0
        QueensInRaw = {i : 0 for i in range(boardLength)}
        for row in self.queens:
            QueensInRaw[int(row)] += 1

        for value in QueensInRaw.values():
            if(value >= 2):
                counter += (value-1)
        return counter

    def getThreadiningDiagonal(self):
        counter = 0
        rightDiagonal = {i:0 for i in range(-(boardLength-1),boardLength)}
        leftDiagonal = {i:0 for i in range((2*boardLength)-1)}
        #right y1-x1 = y2-x2
        for col in range(boardLength):
            row = self.queens[col]
            rightDiagonal[col-row] += 1
        for value in rightDiagonal.values():
            if(value >= 2):
                counter += (value-1)
        #left
        for col in range(boardLength):
            row = self.queens[col]
            leftDiagonal[col+row] += 1
        for value in leftDiagonal.values():
            if(value >= 2):
                counter += (value-1)
        return counter

    #Quantity of Threading Queens
    def fitnessFunction(self): 
        return self.getThreadiningDiagonal() + self.getThreadiningRow()

    def resetBoard(self):
        for row in range(boardLength):
            for col in range(boardLength):
                if (self.board[row][col].isQueen()):
                    self.board[row][col].disableQueen()

    def setBoard(self, board):
        self.resetBoard()
        self.queens = board
        col = 0
        for s in board:
            self.board[col][s].setQueen()
            col += 1

    def generateInitialPopulation(self):
        self.population = PriorityQueue(prioritySize)
        for j in range(initialPopulation):
            currentBoard = []
            for i in range(boardLength):
                randomNumber = random.randint(0, boardLength-1)
                currentBoard.append(randomNumber)
            self.setBoard(currentBoard)
            self.population.push((self.fitnessFunction(),currentBoard))
        self.resetBoard()

    def geneticAlgorithm(self):
        self.generateInitialPopulation()
        best = {'value' : 99999, 'board' : [0 for i in range(boardLength)]}

        for counter in range(maxIteration):
            for i in range(self.population.size()):
                first = self.population.get(self.selectionParent())[1]
                second = self.population.get(self.selectionParent())[1]

                # place border on the left side
                randomBorder = random.randint(1, boardLength-1)
                child = first[0:randomBorder] + second[randomBorder: boardLength]

                mutationsProbability = random.uniform(0,1)
                if(mutationsProbability <= mutation):
                    child[random.randint(0,boardLength-1)] = random.randint(0,boardLength-1)

                self.setBoard(child)
                childFitness = self.fitnessFunction()
                if(best['value'] > childFitness):
                    if(childFitness == 0):
                        print("Solution Found after ",counter," Iterations")
                        self.drawBoard()
                        return
                    best['value'] = childFitness
                    best['board'] = child
                
                self.population.push((self.fitnessFunction(), child))

        print("Solution not Found, best Result of Fitness Function:",best['value'])
        self.setBoard(best['board'])
        self.drawBoard()

    def main(self):
        pygame.init()

        # set display
        self.gameDisplay = pygame.display.set_mode(screenSize)

        # caption
        pygame.display.set_caption("ChessBoard")

        # beginning of logic
        gameExit = False

        # Image of the Queen
        self.queenImg = pygame.image.load('KI_2/QueenImage.png')

        boardLength = 8
        self.gameDisplay.fill(white)

        while not gameExit:
            self.drawBoard()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.geneticAlgorithm()

        # quit from pygame & python
        pygame.quit()
        quit()

    def drawBoard(self):
        for row in range(boardLength):
            for col in range(boardLength):
                # check if current loop value is even
                if (self.board[row][col].isWhite()):
                    pygame.draw.rect(self.gameDisplay, white, [
                                     size*(row + 1), size*(col + 1), size, size])
                else:
                    pygame.draw.rect(self.gameDisplay, gray, [
                                     size*(row + 1), size*(col + 1), size, size])
                if (self.board[row][col].isQueen()):
                    self.gameDisplay.blit(
                        self.queenImg, (size*(row + 1), size*(col + 1)))

        # border
        pygame.draw.rect(self.gameDisplay, black, [
                         size, size, boardLength*size, boardLength*size], 2)
        pygame.draw.rect(self.gameDisplay, black, [
                         size-10, size-10, boardLength*size + 20, boardLength*size + 20], 2)
        pygame.display.update()

    def drawQueen(gameDisplay, queenImg):
        gameDisplay.blit(queenImg, (500, 500))


b = Board(0, 0)
b.main()
