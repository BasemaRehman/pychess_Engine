import pygame as p
import chessEngine
import sys
#Higher = less resolution
WIDTH = HEIGHT = 512
DIMESION = 8
SQ_SIZE = HEIGHT // DIMESION
MAX_FPS = 15 #for animations
IMAGES = {}

#Takes the images saved and assigns them to each couplet of letters - All the same size
def loadImages():
    pieces = ['wp', 'bp', 'wR', 'bR', 'wB', 'bB', 'wK', 'bK', 'wQ', 'bQ', 'wN', 'bN']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    # Starts up Pygame, gives a condition for exiting GUI
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    #Calls in the chess board from chessEngine.py
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #Flag for when move is made
    print (gs.board)
    #Loads in the images only once to make it quicker
    loadImages()
    running = True
    sqSelected = () #empty tuple to keep track of users last click
    playerClicks = [] #player clicks with two tuples
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #Coordinate location
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #User clicked the same square twice
                    sqSelected = () #deselct
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    #Make a move and then restart the player clicks
                    move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
            #Key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    #Brings together drawing the board and pieces
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    #Makes the squares with alternating gray and white
    colours = [p.Color("white"), p.Color("gray")]
    for r in range(DIMESION):
        for c in range(DIMESION):
            colour = colours[((r+c) % 2)]
            p.draw.rect(screen, colour, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    #Makes the pieces according to the 2d structure in chess Engine as the images have now been assigned
    for r in range(DIMESION):
        for c in range(DIMESION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()