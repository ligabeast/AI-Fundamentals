import math
from time import sleep
import pygame
import random
import copy

# set color with rgb
white, black, red, gray = (255, 255, 255), (0, 0,
                                            0), (255, 0, 0), (100, 100, 100)

boardLength = 8
#prio > initial 
initialPopulation = 100
priorityQueueSize = 50
mutation = 0.3
# higher -> select better parent
selectionFactor = 10
maxIteration = 100
stopScore = 0

screenSize = (800, 800)
# Size of squares
size = 640 / boardLength


class PriorityQueue:
    def __init__(self):
        self.structeredData = list()
        self.contains = set()

    def push(self, data):
        index = 0
        if (tuple(data[1]) in self.contains):
            return
        self.contains.add(tuple(data[1]))
        while (index < len(self.structeredData) and
               self.structeredData[index][0] < data[0]):
            index += 1
        if (index >= len(self.structeredData)):
            self.structeredData.append(data)
        else:
            self.structeredData.insert(index, data)
        if(len(self.structeredData) > priorityQueueSize):
            tmp = self.structeredData.pop(len(self.structeredData)-1)
            self.contains.remove(tuple(tmp[1]))

    def pop(self, index=0):
        if (not self.structeredData):  # empty Queue
            print('Queue is empty!!')
            return None
        else:
            return self.structeredData.pop(index)

    def get(self, index):
        if (not self.structeredData):  # empty Queue
            print('Queue is empty!!')
            return None
        else:
            return self.structeredData[index][1]

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
    def __init__(self, geneticAlgorithm):
        self.board = [[0]*boardLength for i in range(boardLength)]
        self.initialzeFields()
        # True = geneticAlgorithm, False = Backtracking
        self.transitionModel = geneticAlgorithm

    def selectionParent(self):
        randomValue = random.randint(0, self.population.size())
        index = (randomValue ** selectionFactor) * \
            ((self.population.size() - 1)/(self.population.size() ** selectionFactor))
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
        QueensInRaw = {i: 0 for i in range(boardLength)}
        for row in self.queens:
            QueensInRaw[int(row)] += 1

        for value in QueensInRaw.values():
            if (value >= 2):
                counter += (value-1)
        return counter

    def getThreadiningDiagonal(self):
        counter = 0
        rightDiagonal = {i: 0 for i in range(-(boardLength-1), boardLength)}
        leftDiagonal = {i: 0 for i in range((2*boardLength)-1)}
        # right y1-x1 = y2-x2
        for col in range(boardLength):
            row = self.queens[col]
            rightDiagonal[col-row] += 1
        for value in rightDiagonal.values():
            if (value >= 2):
                counter += (value-1)
        # left
        for col in range(boardLength):
            row = self.queens[col]
            leftDiagonal[col+row] += 1
        for value in leftDiagonal.values():
            if (value >= 2):
                counter += (value-1)
        return counter

    # Quantity of Threading Queens
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
        self.population = PriorityQueue()
        for j in range(initialPopulation):
            currentBoard = []
            for i in range(boardLength):
                randomNumber = random.randint(0, boardLength-1)
                currentBoard.append(randomNumber)
            self.setBoard(currentBoard)
            self.population.push((self.fitnessFunction(), currentBoard))
        self.resetBoard()

    def backtracking(self):
        self.solutionCounter = 0
        self.queens = ['X'] * boardLength
        self.markedPositions = [
            [False] * boardLength for i in range(boardLength)]
        self.backtrackingRecursive(0)

    def markPosition(self, row, col):
        for tmpRow in range(boardLength):
            self.markedPositions[tmpRow][col] = True
        for tmpCol in range(boardLength):
            self.markedPositions[row][tmpCol] = True

        resultLeft = row + col
        resultRight = col - row
        for tmpRow in range(boardLength):
            for tmpCol in range(boardLength):
                if (tmpRow + tmpCol == resultLeft):
                    self.markedPositions[tmpRow][tmpCol] = True
                if (tmpCol - tmpRow == resultRight):
                    self.markedPositions[tmpRow][tmpCol] = True

    def backtrackingRecursive(self, col):
        for row in range(boardLength):
            if (not self.markedPositions[row][col]):
                self.board[row][col].setQueen()
                tmpMarkPosition = copy.deepcopy(self.markedPositions)
                self.markPosition(row, col)
                self.queens[col] = row
                self.drawBoard()

                if (self.getNumberOfQueensOnBoard() == boardLength and self.fitnessFunction() == 0):
                    print("Solution: ", self.queens)
                    self.solutionCounter += 1

                if (col + 1 < boardLength):
                    self.backtrackingRecursive(col+1)

                self.board[row][col].disableQueen()
                self.queens[col] = 'X'
                self.markedPositions = tmpMarkPosition

    def getNumberOfQueensOnBoard(self):
        return boardLength - self.queens.count('X')

    def geneticAlgorithm(self):
        self.generateInitialPopulation()
        best = {'value': 99999, 'board': [0 for i in range(boardLength)]}

        for counter in range(maxIteration):
            for i in range(self.population.size()):
                first = self.population.get(self.selectionParent())
                second = self.population.get(self.selectionParent())

                # place border on the left side
                randomBorder = random.randint(1, boardLength-1)
                child = copy.deepcopy(
                    first[0:randomBorder] + second[randomBorder: boardLength])

                mutationsProbability = random.uniform(0, 1)
                if (mutationsProbability <= mutation):
                    child[random.randint(0, boardLength-1)
                          ] = random.randint(0, boardLength-1)

                self.setBoard(child)
                childFitness = self.fitnessFunction()
                if (best['value'] > childFitness):
                    if (childFitness == stopScore):
                        if (self.transitionModel):
                            print("Solution Found after ",
                                  counter, " Iterations")
                        self.drawBoard()
                        return
                    best['value'] = childFitness
                    best['board'] = child

                self.population.push((self.fitnessFunction(), child))

        if (self.transitionModel):
            print("Solution not Found, best Result of Fitness Function:",
                  best['value'])
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
                        if (self.transitionModel):
                            self.geneticAlgorithm()
                        else:
                            self.backtracking()
                            print("Found solutions: ", self.solutionCounter)

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


b = Board(True)
b.main()
