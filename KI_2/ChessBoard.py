import pygame
import random
import time

# set color with rgb
white, black, red, gray = (255, 255, 255), (0, 0, 0), (255, 0, 0), (100, 100, 100)
boardLength = 8
screenSize = (800, 800)
# Size of squares
size = 80


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
        for row in self.positions:
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
            row = int(self.positions[col])
            rightDiagonal[col-row] += 1
        for value in rightDiagonal.values():
            if(value >= 2):
                counter += (value-1)
        #left
        for col in range(boardLength):
            row = int(self.positions[col])
            leftDiagonal[col+row] += 1
        for value in leftDiagonal.values():
            if(value >= 2):
                counter += (value-1)

        return counter

                

    #Quantity of Threading Queens
    def heuristicFunction(self): 
        return self.getThreadiningDiagonal() + self.getThreadiningRow()

    def resetBoard(self):
        for row in range(boardLength):
            for col in range(boardLength):
                if (self.board[row][col].isQueen()):
                    self.board[row][col].disableQueen()

    def setBoard(self, board):
        self.resetBoard()
        self.positions = board
        col = 0
        for s in board:
            self.board[col][int(s)].setQueen()
            col += 1

    def geneticAlgorithm(self):
        self.generatedBoard = []
        best = 28
        bestPostion = ""

        while (len(self.generatedBoard) < 100):
            for j in range(2):
                currentBoard = ""
                for i in range(boardLength):
                    randomNumber = random.randint(0, 7)
                    currentBoard += str(randomNumber)
                self.generatedBoard.append(currentBoard)
                self.setBoard(currentBoard)
                self.drawBoard()
                currentThreading = self.heuristicFunction()
                if(currentThreading < best):
                    best = currentThreading
                    bestPostion = currentBoard
            # place border on the left side
            randomNumber = random.randint(1, 7)
            child = self.generatedBoard[-2][0:randomNumber] + \
                self.generatedBoard[-1][randomNumber:
                                        len(self.generatedBoard[-1])]
            self.generatedBoard.append(child)
            self.setBoard(child)
            self.drawBoard()
            if(currentThreading < best):
                best = currentThreading
                bestPostion = currentBoard
        print(best)
        self.setBoard(bestPostion)
        self.drawBoard()

    def main(self):
        pygame.init()

        # set display
        self.gameDisplay = pygame.display.set_mode((800, 800))

        # caption
        pygame.display.set_caption("ChessBoard")

        # beginning of logic
        gameExit = False

        # Size of squares
        size = 80

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
