import helpers

def play_game_AI():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        helpers.print_board(board)

        if current_player == "X":
            cell_number = int(input("Enter Cell Number (1-9): "))
            if cell_number < 1 or cell_number > 9:
                print("Invalid move, Try again :^)")
                continue

            cell_number -= 1
            row = cell_number // 3
            col = cell_number % 3

            if board[row][col] == " ":
                board[row][col] = current_player
            else:
                print("Invalid move, Try again :^)")
                continue
        else:
            print("AI PLAYED: ->>>>>>>>>>>>>>")
            cells = helpers.get_best_move(board)
            row = cells[0]
            col = cells[1]
            board[row][col] = current_player

        print(helpers.is_winner(board, row, col, current_player))
        if helpers.is_winner(board, row, col, current_player):
            helpers.print_board(board)
            print(f"WINNER ISSSSSSSSS {current_player}!!!!!!!!!")
            break

        if helpers.is_tie(board):
            helpers.print_board(board)
            print("TIEEEEEEEEEEE!!!!!!!!!!!!!")
            break
        
        current_player = "X" if current_player == "O" else "O"


play_game_AI()