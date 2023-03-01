import os
import pygame
import random

import consts
from interperter import *
import sys
from consts import *
import copy
from piece import Piece

WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1200
GRID_WIDTH = 10
TICKSPERMOVE = 60
INITIAL_GAME_BOARD_HEIGHT = 40
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
PIECE_SPAWN_ABOVE_BOARD_HEIGHT = 15
CELL_SIZE = 55
SCROLLING_MULTIPLIER = 100

PIECE_DEFAULT_X = 3


def main():
    # Initialize stuff
    global SCREEN, CLOCK
    pygame.init()
    smallfont = pygame.font.SysFont('Corbel', 25)
    largerFont = pygame.font.SysFont('Courier New', 25)  # The only monospaced font that comes with windows
    BUTTON_TEXT_SURFACE = smallfont.render(
        "Run brainf*ck", True, BUTTON_TEXT_COLOR)
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("Tetris time!")
    SCREEN.fill(BLACK)

    # Setup game variable
    scroll = 0
    ticks = 0
    gridHeight = 40

    # Initialize the piece
    piece = Piece(
        color=random.choice(COLORS),
        rotation=0,
        shape=random.choice(SHAPE_CODE),
        x=PIECE_DEFAULT_X,
        y=gridHeight
    )

    gameBoard = initBoard()
    running = True

    # Game loop
    while running:
        SCREEN.fill(BLACK)
        # Draw the board
        renderToScreen(
            gameBoard,
            piece,
            scroll
        )
        # Handle user input
        scroll = handleInput(scroll)
        # Update the board based on input

        pygame.display.flip()
        CLOCK.tick(60)


def initBoard(height=INITIAL_GAME_BOARD_HEIGHT):
    """
    Initializes the board
    """
    board = []
    for i in range(height):
        board.append([])
        for _ in range(GRID_WIDTH):
            board[i].append(BOAD_EMPTY)

    return board


def drawBoardToScreen(board, scrollpx):
    """
    Draws the grid on the screen
    """

    # Calculates a % of scroll and uses that to place the grid
    boardHeight = CELL_SIZE * len(board)  # Calculate the height
    print(scrollpx)
    scrollPercentage = 0.0
    if scrollpx > 0:
        scrollPercentage = scrollpx / boardHeight  # Should be a number 0-1 where 1 is max scroll

    if boardHeight < WINDOW_HEIGHT:
        # protect against small grids breaking stuff
        scrollPercentage = 0

    scrollPercentage = clamp(0, 1, scrollPercentage)

    boardWidth = CELL_SIZE * GRID_WIDTH
    boardLeftPosition = WINDOW_WIDTH / 2 - boardWidth / 2

    for rowIndex, row in enumerate(board):
        for colIndex, col in enumerate(row):
            # Row 0 (The first one) should be the bottom
            # Row {max} should be the top
            color: colorTuple = random.choice(COLORS)

            x = boardLeftPosition + (CELL_SIZE * colIndex)
            y = CELL_SIZE * rowIndex - (boardHeight * scrollPercentage) - WINDOW_HEIGHT
            print(f"x: {x} y: {y} scroll: {scrollpx} scrollPer: {scrollPercentage} BoardHeight: {boardHeight}")
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(SCREEN, color.rgb, rect)


def blitPieceOnBoard(gameboard, piece: Piece):
    """
    "Renders" a piece on the passed in gameboard.
    Does not verify the validity of the position
    """

    # Python shenanigans means that it might work without the copy
    # But it also might not, and it gives really dumb and hard
    # to track bugs. Thus, this line stays even if it's slow
    gameboard = copy.deepcopy(gameboard)

    shape = SHAPES[piece.shape][piece.rotation % 4]
    for i in range(len(shape)):
        for j in range(len(shape[i])):
            if shape[i][j] != 0:
                try:
                    gameboard[piece.y + i][piece.x + j] = piece.color.code
                except IndexError:  # Just ignore any cells outside the board since they are just empty anyways
                    pass
    return gameboard


def renderToScreen(gameBoard, piece, scroll):
    gameBoard = blitPieceOnBoard(gameBoard, piece)
    drawBoardToScreen(gameBoard, scroll)


def handleInput(scroll: int):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEWHEEL:
            scroll += event.y * SCROLLING_MULTIPLIER
    print(scroll)
    return scroll


def clamp(min, max, value):
    return sorted((min, value, max))[1]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
