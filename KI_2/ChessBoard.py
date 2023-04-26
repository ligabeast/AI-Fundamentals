import pygame
import random
import time

# set color with rgb
white, black, red, gray = (255, 255, 255), (0, 0,
                                            0), (255, 0, 0), (100, 100, 100)
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
        self.x = queenPositions
        self.y = queenQuantitys
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

    def resetBoard(self):
        for row in range(8):
            for col in range(8):
                if (self.board[row][col].isQueen()):
                    self.board[row][col].disableQueen()

    def setBoard(self, string):
        self.resetBoard()
        col = 0
        for s in string:
            self.board[col][int(s)].setQueen()
            col += 1

    def geneticAlgorithm(self):
        pass

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
