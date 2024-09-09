import minesweeper as ms


def main():
    print("Minesweeper AI Prototype")

    minesweeper = ms.Minesweeper(num_rows=10, num_cols=10, seed=40531)
    print(f"Seed: {minesweeper.seed}")
    print(f"Number of mines: {minesweeper.num_mines}")
    minesweeper.print_board()
    print("\n")
    minesweeper.print_game_state()

    # Create a game loop where we accept user input and update the game state / print it out as we go
    while True:
        row = int(input("Enter row: "))
        col = int(input("Enter col: "))
        action = input("Enter action (r for reveal, f for flag): ")

        if action == "r":
            minesweeper.reveal(row, col)
        elif action == "f":
            minesweeper.flag(row, col)
        else:
            print("Invalid action")
            continue

        minesweeper.print_game_state()

        if minesweeper.check_win():
            print("You win!")
            break
        elif minesweeper.check_loss():
            print("You lose!")
            break


if __name__ == "__main__":
    main()
