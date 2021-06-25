import pygame as p
import chessEngine
import sys
#Higher = less resolution
WIDTH = HEIGHT = 512
DIMESION = 8
SQ_SIZE = HEIGHT // DIMESION
MAX_FPS = 15 #for animations
IMAGES = {}

def loadImages():
    pieces = ['wp', 'bp', 'wR', 'bR', 'wB', 'bB', 'wK', 'bK', 'wQ', 'bQ', 'wN', 'bN']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():

    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    print (gs.board)
    loadImages()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colours = [p.Color("white"), p.Color("gray")]
    for r in range(DIMESION):
        for c in range(DIMESION):
            colour = colours[((r+c) % 2)]
            p.draw.rect(screen, colour, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMESION):
        for c in range(DIMESION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()