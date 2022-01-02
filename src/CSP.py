import itertools

import numpy as np



def solve(board, pieces):
    if board.min() > 0:
        # No empty cells left in grid
        print("Solution found:\n", board)
        return board

    # Make a local copy of the pieces before we remove one piece
    my_pieces = pieces.copy()
    piece = my_pieces.pop()

    for i, variant in enumerate(piece.variants):
        for r, c in itertools.product(
                range(board.shape[0] - variant.shape[0] + 1),
                range(board.shape[1] - variant.shape[1] + 1)):

            if not np.any(board[r:r + variant.shape[0],
                          c:c + variant.shape[1]] * variant):
                # This piece can be placed in this position
                # Do that and call ourselves with the resulting grid
                newgrid = board.copy()
                newgrid[r:r + variant.shape[0],
                c:c + variant.shape[1]] += variant

                #  print("{}Placing piece {}, variant {} at {}, {}".format(
                #  '    '*(2-len(my_pieces)), variant.max(), i, r, c))

                solution = solve(newgrid, my_pieces)
                if solution is not None:
                    return solution

    #  print("{}Finished with piece {}".format(
    #  '    '*(2-len(my_pieces)), piece.variants[0].max()))
    return None
