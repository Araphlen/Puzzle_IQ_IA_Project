

import itertools
import numpy as np
import itertools


def solve(board, pieces):
    iaSolver(board, pieces)

def iaSolver(board, pieces):
    if board.min() > 0:
        print("Solution trouvée :\n", board)
        return board

    localPieces = pieces.copy()
    piece = localPieces.pop()

    for variant in piece.variants:
        #pour toutes les coordonées possibles
        for line, column in itertools.product(range(board.shape[0] - variant.shape[0] + 1),
                                                range(board.shape[1] - variant.shape[1] + 1)):
            # Check si la variante peut etre placer sur la position ligne colonne
            if isFreespace(board,variant,line,column):
                #crée une nouvelle board pour pouvoir revenir si on ne peut pas placer toutes les pieces
                newBoard = board.copy()
                newBoard[line:line + variant.shape[0],
                column:column + variant.shape[1]] += variant # add the variant in the possible spot

                #print(" variant ",variant , "placée en (",line,",",column,")")
                #appel la méthode pour une nouvelle piece
                solution = solve(newBoard, localPieces)
                if solution is not None:
                    return solution
    # print("toutes les variantes faites pour la piece : " , piece.shapeNb)
    return None


def isFreespace(board,variant ,currentl,currentc):
    # for all the point in the piece check if the same spot in the grid is occupied
    for l in range(variant.shape[0]):
        for c in range(variant.shape[1]):
            if variant[l][c] != 0 and board[currentl+l][c+currentc] != 0:
                return False
    return True