def print_board(board):
    for row in board:
        print("|", end="")
        for cell in row:
            print(cell, end="|")
        print("\n-------")

def is_winner(board, row, col, symbol):
    horizontal_count = 0
    vertical_count = 0
    diagonal_count = 0
    second_diagonal_count = 0

    for i in range(3):
        horizontal_count += 1 if board[row][i] == symbol else 0
        vertical_count += 1 if board[i][col] == symbol else 0
        diagonal_count += 1 if board[i][i] == symbol else 0
        second_diagonal_count += 1 if board[i][2-i] == symbol else 0

    if horizontal_count == 3 or vertical_count == 3 or diagonal_count == 3 or second_diagonal_count == 3:
        return True

    return False

def is_tie(board):
    return all(" " not in row for row in board)

def get_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return True

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return True
        
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return True
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return True

    return False

def get_best_move(board):
    best_score = float('-inf')
    move = None

    for i in range(3):
        for j in range(3):
            if (board[i][j] != " "):
                continue

            board[i][j] = "O"
            move_score = minimax(board, 0, float('-inf'), float('inf'),  True)
            board[i][j] = " "
            if move_score > best_score:
                best_score = move_score
                move = [i, j]
            
    return move

def minimax(board, depth, alpha, beta, to_minimize) -> int:
  game_end_state = get_winner(board)
  if game_end_state and to_minimize:
    return 1
  if game_end_state and not to_minimize:
    return -1
  if is_tie(board):
    return 0

  best_score = float('inf') if to_minimize else float('-inf')
  current_player = 'X' if to_minimize else 'O'

  for i in range(3):
    for j in range(3):
      if (board[i][j] != ' '):
        continue

      board[i][j] = current_player
      move_score = minimax(board, depth + 1, alpha, beta, not(to_minimize))
      board[i][j] = ' '

      if to_minimize:
        best_score = min(best_score, move_score)
        beta = min(beta, best_score)
      else:
        best_score = max(best_score, move_score)
        alpha = max(alpha, best_score)

      if alpha >= beta:
        break

  return best_score
