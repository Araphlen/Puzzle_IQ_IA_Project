import itertools

import numpy as np
import itertools


# Generate a solution and test it
# def generateAndTest(csp,search_for=None):
#     V=csp.Domains
#     if getattr(csp,"f",None):
#         best_f=None
#         for v in itertools.product(*V):
#             if csp.condition(v):
#                 f=csp.f(v)
#                 if best_f is None or f<best_f:
#                     best_f=f
#                     best_assignement=v
#
#         return best_assignement,best_f
#     else:
#         for v in itertools.product(*V):
#             if csp.condition(v):
#                 return v


# Generate a sub-solution and test it
def simpleBT(i,csp,A):
    V=csp.Domains
    if i==len(V):
        return A
    else:
        d=V[i]
        for k,v in enumerate(d):
            sol=A+[v]
            if csp.condition(sol):
                return simpleBT(i+1,csp,sol)

        return simpleBT(i+1,csp,A)

# Generate sub-solutions by testing them
def testAndGenerate(csp):
    return simpleBT(0,csp,[])













def solve(board, pieces):
    if board.min() > 0:
        print("Solution found:\n", board)
        return board

    # Make a local copy of the pieces before we remove one piece
    my_pieces = pieces.copy()
    piece = my_pieces.pop()

    for i, variant in enumerate(piece.variants):
        for line, column in itertools.product(
                range(board.shape[0] - variant.shape[0] + 1),
                range(board.shape[1] - variant.shape[1] + 1)):


            if isFreespace(board,variant,line,column):
                # This piece can be placed in this position
                # Do that and call ourselves with the resulting grid
                newgrid = board.copy()
                newgrid[line:line + variant.shape[0],
                column:column + variant.shape[1]] += variant

                print("{}Placing piece {}, variant {} at {}, {}".format(
                    '    '*(2-len(my_pieces)), variant.max(), i, line, column))
                solution = solve(newgrid, my_pieces)
                if solution is not None:
                    return solution

    print("{}Finished with piece {}".format(
    '    '*(2-len(my_pieces)), piece.tag))
    return None


def isFreespace(board,variant ,currentl,currentc):
    for l in range(variant.shape[0]):
        for c in range(variant.shape[1]):
            if variant[l][c] != 0 and board[currentl+l][c+currentc] != 0:
                return False
    return True