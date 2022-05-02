from math import fabs
from re import T
import pygame
import random
from  interperter import *
import sys
from consts import *
import copy

# Colors:
# red = r
# lime = g
# blue = b
# yellow = y
# cyan = c
# purple = p



BLACK = (0, 0, 0)
WHITE = (224, 224, 224)
WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1200
GRID_WIDTH = 10
GRID_HEIGHT = 20
TICKSPERMOVE = 60 # how long before moving the piece down again. This is a const because there is no line clearing in this version

# Stuff for the button
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 40
BUTTON_DARK = (200,200,200)
BUTTON_LIGHT = (100,100,100)
BUTTON_X = WINDOW_WIDTH - BUTTON_WIDTH - 20
BUTTON_Y = WINDOW_HEIGHT - BUTTON_HEIGHT - 20
BUTTON_TEXT_OFFSET = 5
BUTTON_TEXT_COLOR = (255,255,255)

PIECE_DEFAULT_X = 3

def main():
    global SCREEN, CLOCK
    pygame.init()
    smallfont = pygame.font.SysFont('Corbel',35)
    BUTTON_TEXT_SURFACE = smallfont.render("Run brainf*ck",True,BUTTON_TEXT_COLOR)
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("Tetris time!")
    SCREEN.fill(BLACK)

    ticks = 0
    rotation = 0
    current_shape = random.choice(SHAPE_CODE)
    previous_shape = current_shape
    piecex, piecey = PIECE_DEFAULT_X,0

    placedBoard = initBoard()
    current_color = random.choice(COLORS)


    while True:
        mouseDown = False
        board = []
        ticks += 1
        SCREEN.fill(BLACK)
        board = copy.deepcopy(placedBoard)
        board = renderShape(SHAPES[current_shape][rotation], piecex, piecey, current_color, board)
        drawBoard(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rotation = (rotation + 1) % 4
                elif event.key ==  pygame.K_LEFT and checkIfCanGoLeft(placedBoard, SHAPES[current_shape][rotation], piecex, piecey):
                    piecex -= 1
                elif event.key == pygame.K_RIGHT and checkIfCanGoRight(placedBoard, SHAPES[current_shape][rotation], piecex, piecey):
                    piecex += 1
                elif event.key == pygame.K_DOWN and checkIfCanGoDown(placedBoard, SHAPES[current_shape][rotation], piecex, piecey):
                    piecey += 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Left mouse
                    mouseDown = True
        
        drawButton(mouseDown, BUTTON_TEXT_SURFACE)

        if ticks % TICKSPERMOVE == 0 and checkIfCanGoDown(placedBoard, SHAPES[current_shape][rotation], piecex, piecey):
            piecey += 1
        
        

        if not checkIfCanGoDown(placedBoard, SHAPES[current_shape][rotation], piecex, piecey):
            # Reset everything for the next piece
            print("Reset for next piece")
            placedBoard = board.copy()
            current_shape, previous_shape = getNewPiece(previous_shape)
            piecex, piecey = PIECE_DEFAULT_X,0
            current_color = random.choice(COLORS)
            rotation = 0


        pygame.display.flip()
        CLOCK.tick(60)



def drawBoard(board):
    """
    Draws the grid on the screen
    """
    Y_OFFSET = 10 # Offset the grid from the top
    BLOCKSIZE = 50 #Set the size of the grid block
    GRID_PX_WIDTH = (BLOCKSIZE * GRID_WIDTH) /2
    GRID_PX_HEIGHT = (BLOCKSIZE * GRID_HEIGHT) /2
    xindex, yindex = 0, 0
    for x in range(int(WINDOW_WIDTH/2 - GRID_PX_WIDTH), int(WINDOW_WIDTH/2 + GRID_PX_WIDTH), BLOCKSIZE):

        for y in range(int(WINDOW_HEIGHT/2 - GRID_PX_HEIGHT + Y_OFFSET), int(WINDOW_HEIGHT/2 + GRID_PX_HEIGHT + Y_OFFSET), BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            
            color = getColorFromChar(board[yindex][xindex])
            if color != None:
                # Draw the block filled in
                pygame.draw.rect(SCREEN, color, rect)
            # Draw the grid overlay
            pygame.draw.rect(SCREEN, WHITE, rect, 1)
            yindex+=1
        xindex+=1
        yindex=0


def initBoard():
    """
    Initializes the board
    """
    board = []
    for i in range(GRID_HEIGHT):
        board.append([])
        for _ in range(GRID_WIDTH):
            board[i].append(" ")

    return board

def getColorFromChar(char):
    """
    Returns the color of the character
    """
    # Colors to piece mappings here
    if char == "r":
        return ( 211, 47, 47 )
    elif char == "g":
        return ( 46, 125, 50)
    elif char == "b":
        return (48, 63, 159)
    elif char == "y":
        return (253, 216, 53)
    elif char == "c":
        return (3, 169, 244)
    elif char == "p":
        return ( 106, 27, 154 )
    elif char == "o":
        return (  255, 111, 0 )
    else:
        return None

def renderShape(shape, x, y, color, board):
    """
    Renders the shape on the board
    """
    for i in range(len(shape)):
        for j in range(len(shape[i])):
            if shape[i][j] != 0:
                try:
                    board[y + i][x + j] = color
                except IndexError:
                    pass
    return board



def checkIfValidPosition(board, piece, x, y):
    """
    Checks if the piece can go down
    """
    pass

def drawButton(mouseDown, BUTTON_TEXT_SURFACE):
    # Button stuff
    mx, my = pygame.mouse.get_pos()
    if BUTTON_X <= mx <=BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= my <=BUTTON_Y+BUTTON_HEIGHT:
        pygame.draw.rect(SCREEN, BUTTON_DARK,[BUTTON_X,BUTTON_Y,BUTTON_WIDTH,BUTTON_HEIGHT])
        if mouseDown:
            # Run the interperter
            pass
    else:
        pygame.draw.rect(SCREEN, BUTTON_LIGHT,[BUTTON_X,BUTTON_Y,BUTTON_WIDTH,BUTTON_HEIGHT])

    SCREEN.blit(BUTTON_TEXT_SURFACE , (BUTTON_X + BUTTON_TEXT_OFFSET, BUTTON_Y))

def getNewPiece(pervious_shape):
    """
    Returns a new piece but weighted against the previous piece
    """
    new_shape = random.choice(SHAPE_CODE)
    if new_shape == pervious_shape:
        print("Rerolled shape")
        new_shape = random.choice(SHAPE_CODE)
    return new_shape, pervious_shape

if __name__ == "__main__":
    main()