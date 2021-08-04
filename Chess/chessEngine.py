class GameState():
    def __init__(self):
        #This is a 2d list - try to implement with numpy arrays
        #Letter notation is colour and type (N = knight, K = King)
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "bN", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'p' : self.getPawnMoves,
                              'R' : self.getRookMoves,
                              'N' : self.getKnightMoves,
                              'B' : self.getBishopMoves,
                              'Q' : self.getQueenMoves,
                              'K' : self.getKingMoves }
        self.whiteToMove = True
        self.moveLog = []

    '''
    Takes a Move as a parameter and execute it (will not work for castling, pawn promotion and en-passent)
    '''
    global toMove
    def team(self):
        global toMove
        if self.whiteToMove:  # White knight moves
            toMove = 'w'
        else:
            toMove = 'b'

    def makeMove(self, move):
        if(self.board[move.startRow][move.startCol] != "--"):
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move) #Log the move to show game history or to undo the move
            self.whiteToMove = not self.whiteToMove #swap players

    '''
    Undo the last move
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop();
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #Switch the turn back

    '''
    Get all moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllMoves()

    '''
    All moves without considering checks
    '''
    def getAllMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) #Calls the method by the piece type
        return moves

    '''
    Gets all moves for pawns
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #Only for white pawns
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c), (r-1, c), self.board))
                if(r == 6 and self.board[r-2][c] == "--"):
                    moves.append(Move((r,c), (r-2, c), self.board))
            if(c - 1 >= 0):
                if(self.board[r-1][c-1][0] == 'b'):
                    moves.append(Move((r,c), (r-1, c-1), self.board))
            if c + 1 <= 7:
                if (self.board[r - 1][c + 1][0] == 'b'):
                    moves.append(Move((r,c), (r-1, c+1), self.board))

        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1, c), self.board))
                if(r == 1 and self.board[r+2][c] == "--"):
                    moves.append(Move((r,c), (r+2, c), self.board))
            if(c - 1 >= 0):
                if(self.board[r + 1][c - 1][0] == 'w'):
                    moves.append(Move((r,c), (r+1, c-1), self.board))
            if c + 1 <= 7:
                if (self.board[r + 1][c + 1][0] == 'w'):
                    moves.append(Move((r,c), (r+1, c+1), self.board))
        #Add Pawn promotions
    '''
    Gets all moves for the Rook
    '''
    def getRookMoves(self, r, c, moves):
        #Rooks can move forward back left and right until then get another piece
        directions = ((-1,0), (0,-1), (1,0), (0,1))
        enemyColour = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColour:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    '''
    Gets all moves for the Knight
    '''
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2 , -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColour = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if(0 <= endRow < 8 and 0 <= endCol < 8):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColour:
                    moves.append(Move((r,c), (endRow, endCol), self.board))


    '''
    Gets all moves for the Bishop
    '''
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (1, -1), (-1, 1), (1, 1))
        enemyColour = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColour:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    '''
    Gets all moves for the King
    '''
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (1, -1), (-1, 1), (1, 1),(-1,0), (0,-1), (1,0), (0,1))
        allyColour = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColour:
                    moves.append(Move((r,c), (endRow, endCol), self.board))

    '''
    Gets all moves for the Queen
    '''
    def getQueenMoves(self, r, c, moves):
        #Queen moves should be equal to the rook moves + bishop moves - No need to repeat
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r,c,moves)


#Make a class to do the movements. It can be done by keeping track of coordinates but this is easier
class Move():
    #Creates the chess coordinate notation
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
        Override the equals method as we are using a class
        '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]