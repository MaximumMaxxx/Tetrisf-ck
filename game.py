import os
import pygame
import random
from interperter import *
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
TICKSPERMOVE = 60  # how long before moving the piece down again. This is a const because there is no line clearing in this version

# Stuff for the button
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 40
BUTTON_DARK = (200, 200, 200)
BUTTON_LIGHT = (100, 100, 100)
BUTTON_X = WINDOW_WIDTH - BUTTON_WIDTH - 20
BUTTON_Y = WINDOW_HEIGHT - BUTTON_HEIGHT - 20
BUTTON_TEXT_OFFSET = 5
BUTTON_TEXT_COLOR = (255, 255, 255)
BOAD_EMPTY = " "


PIECE_DEFAULT_X = 3


def main():
    global SCREEN, CLOCK
    pygame.init()
    smallfont = pygame.font.SysFont('Corbel', 25)
    largerFont = pygame.font.SysFont('Courier New', 25) # The only monospaced font that comes with windows
    BUTTON_TEXT_SURFACE = smallfont.render(
        "Run brainf*ck", True, BUTTON_TEXT_COLOR)
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("Tetris time!")
    SCREEN.fill(BLACK)

    ticks = 0
    rotation = 0
    current_shape = random.choice(SHAPE_CODE)
    piecex, piecey = PIECE_DEFAULT_X, 0

    placedBoard = initBoard()
    current_color = random.choice(COLORS)
    running = True

    while running:
        wantsToMoveDown = False
        mouseDown = False
        board = []
        ticks += 1
        SCREEN.fill(BLACK)
        board = copy.deepcopy(placedBoard)
        board = renderShape(
            SHAPES[current_shape][rotation], piecex, piecey, current_color, board)
        drawBoard(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    temprotation = (rotation + 1) % 4
                    if checkIfValidPosition(placedBoard, SHAPES[current_shape][temprotation], piecex, piecey):
                        rotation = temprotation

                elif event.key == pygame.K_LEFT and checkIfValidPosition(placedBoard, SHAPES[current_shape][rotation], piecex-1, piecey):
                    piecex -= 1
                elif event.key == pygame.K_RIGHT and checkIfValidPosition(placedBoard, SHAPES[current_shape][rotation], piecex+1, piecey):
                    piecex += 1
                elif event.key == pygame.K_DOWN and checkIfValidPosition(placedBoard, SHAPES[current_shape][rotation], piecex, piecey + 1):
                    wantsToMoveDown = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Left mouse
                    mouseDown = True

        drawButton(mouseDown, BUTTON_TEXT_SURFACE, placedBoard)
        DrawHintText(SCREEN, smallfont, largerFont)

        if (ticks % TICKSPERMOVE == 0 or wantsToMoveDown) and checkIfValidPosition(placedBoard, SHAPES[current_shape][rotation], piecex, piecey + 1):
            print("Moved down")
            piecey += 1

        # Reset everything for the next piece
        if not checkIfValidPosition(placedBoard, SHAPES[current_shape][rotation], piecex, piecey+1):
            print("Reset for next piece")
            print(f"Debuge stuff")
            print(current_shape)
            print(piecex, piecey)
            print(rotation)
            for row in placedBoard:
                print(row)

            print()
            placedBoard = renderShape(
                SHAPES[current_shape][rotation], piecex, piecey, current_color, placedBoard)
            for row in placedBoard:
                print(row)

            current_shape = getNewPiece(current_shape)
            piecex, piecey = PIECE_DEFAULT_X, 0
            current_color = random.choice(COLORS)
            rotation = 0

            # Check if lines(s) need to be cleared
            for y in range(len(placedBoard)):
                if not " " in placedBoard[y]:
                    print("Cleared line")
                    placedBoard.pop(y)
                    placedBoard.insert(0, [])
                    for _ in range(GRID_WIDTH):
                        placedBoard[0].append(BOAD_EMPTY)


            # Check if game is over
            # Do the board overlay stuff with the next piece
            if not checkIfValidPosition(placedBoard, SHAPES[current_shape][rotation], piecex, piecey):
                # Red gameover font
                font = pygame.font.SysFont('Corbel', 100)
                text = font.render("Game Over", True, (255, 0, 0))
                SCREEN.blit(text, (WINDOW_WIDTH / 2 - text.get_width() / 2, WINDOW_HEIGHT / 2 - text.get_height() / 2))
                pygame.display.update()
                pygame.time.wait(1000)
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        CLOCK.tick(60)


def drawBoard(board):
    """
    Draws the grid on the screen
    """
    Y_OFFSET = 10  # Offset the grid from the top
    BLOCKSIZE = 50  # Set the size of the grid block
    GRID_PX_WIDTH = (BLOCKSIZE * GRID_WIDTH) / 2
    GRID_PX_HEIGHT = (BLOCKSIZE * GRID_HEIGHT) / 2
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
            yindex += 1
        xindex += 1
        yindex = 0


def initBoard():
    """
    Initializes the board
    """
    board = []
    for i in range(GRID_HEIGHT):
        board.append([])
        for _ in range(GRID_WIDTH):
            board[i].append(BOAD_EMPTY)

    return board


def getColorFromChar(char):
    """
    Returns the color of the character
    """
    # Colors to piece mappings here
    if char == "r":
        return (211, 47, 47)
    elif char == "g":
        return (46, 125, 50)
    elif char == "b":
        return (48, 63, 159)
    elif char == "y":
        return (255, 160, 0)
    elif char == "c":
        return (3, 169, 244)
    elif char == "p":
        return (106, 27, 154)
    elif char == "o":
        return (255, 111, 0)
    elif char == "P":
        return (233, 30, 99)
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
                except IndexError:  # Just ignore any cells outside the board since they are just empty anyways
                    pass
    return board


def checkIfValidPosition(board, piece, x, y):
    """
    Checks if the passed position is valid, A bit of a slower way of doing this than 
    a dedicated function for down or rotation check but it's way easier to do it this way
    """

    # Calculate the grid offset ie. for many rows below the bottom of the piece are empty
    offset = 0
    for i in range(len(piece)):
        if 1 in piece[i] and i > 0:
            offset += 1

    if y + offset > GRID_HEIGHT -1:
        return False

    # Check if the piece is too far left or right
    for row in piece:
        for ci, col in enumerate(row):
            if col != 0 and (x + ci < 0 or x + ci > GRID_WIDTH - 1):
                return False

    checkAgaist = renderShape(
        piece, x, y, ".", copy.deepcopy(board))  # Render the piece in a color that isn't otherwise used
    for li, line in enumerate(checkAgaist):
        for ci, cell in enumerate(line):
            if cell == '.' and board[li][ci] != ' ':
                print("That is not a valid position")
                return False
    return True


def drawButton(mouseDown, BUTTON_TEXT_SURFACE, board):
    """
    Draws the button and handles running the interpreter
    """
    
    mx, my = pygame.mouse.get_pos()
    if BUTTON_X <= mx <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= my <= BUTTON_Y+BUTTON_HEIGHT:
        pygame.draw.rect(SCREEN, BUTTON_DARK, [
                         BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT])
        if mouseDown:
            # Dump the board to json
            with open("board.json", "w") as f:
                json.dump(board, f)

            # Run the interperter
            print("---------------------------------")
            print("This shell window will be dropped into the interpreter")
            print()
            print("To exit the interpreter, press Ctrl+C")
            print("---------------------------------")

            os.system("python3 interperter.py")

            print("---------------------------------")
            print("Exiting interpreter")
            print("---------------------------------")
    else:
        pygame.draw.rect(SCREEN, BUTTON_LIGHT, [
                         BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT])

    SCREEN.blit(BUTTON_TEXT_SURFACE, (BUTTON_X + BUTTON_TEXT_OFFSET, BUTTON_Y))

def getNewPiece(previous_shape):
    """
    Returns a new piece weighted against the previous piece
    """
    temp_piece = random.choice(SHAPE_CODE)
    if previous_shape == temp_piece:
        temp_piece = random.choice(SHAPE_CODE)
    return temp_piece

def DrawHintText(screen, smol_font, larger_font):
    """
    Draw some text on the left half of the screen which tells the user what the pieces do in the interpreter
    """
    hint_text1 = "Hint: The interpreter will run the "
    hint_text_surface1 = smol_font.render(hint_text1, True, WHITE)
    screen.blit(hint_text_surface1, (10, 10))
    hint_text2 = "code in the shell window"
    hint_text_surface2 = smol_font.render(hint_text2, True, WHITE)
    screen.blit(hint_text_surface2, (10, 30))

    # Draw 8 cubes in all the different colors
    for i in range(8):
        y = 60 + i * 50
        x = 10
        pygame.draw.rect(screen, getColorFromChar(COLORS[i]), [x, y, 40, 40])

        # Draw the brainfuck code on the block
        if i == 0:
            brainfuck_char = "<"
        elif i == 1:
            brainfuck_char = ">"
        elif i == 2:
            brainfuck_char = "+"
        elif i == 3:
            brainfuck_char = "-"
        elif i == 4:
            brainfuck_char = "."
        elif i == 5:
            brainfuck_char = ","
        elif i == 6:
            brainfuck_char = "["
        elif i == 7:
            brainfuck_char = "]"
        brainfuck_text = larger_font.render(brainfuck_char, True, WHITE)
        screen.blit(brainfuck_text, (x + 12, y + 4))





if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
