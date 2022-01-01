def isBoardCompleted(board):
    for i in range(5):
        for j in range(11):
            if board[i][j]==0:
                return False
    return True

