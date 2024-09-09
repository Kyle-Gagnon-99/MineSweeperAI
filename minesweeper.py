import random


class Minesweeper:
    def __init__(self, num_rows: int, num_cols: int, num_mines: int = None, mine_percentage: float = 16, seed: int = None):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_mines = num_mines
        self.mine_percentage = mine_percentage
        self.seed = seed
        self.board = []
        self.game_state = []
        self.game_over = False

        if seed is not None:
            random.seed(seed)
        else:
            self.seed = random.randint(0, 1000000)
            random.seed(self.seed)

        self._generate_baord()

    def get_seed(self):
        return self.seed

    def _generate_baord(self):
        # Initialize the board with all zeros
        self.board = [0 for _ in range(self.num_cols * self.num_rows)]

        # If num_mines is not provided, calculate it based on mine_percentage
        if self.num_mines is None:
            self.num_mines = int(
                self.num_cols * self.num_rows * self.mine_percentage / 100)

        # Randomly place mines on the board (represented by -1)
        # Since this is a single-dimensional list, we need to convert the 2D coordinates to 1D index
        mine_indices = random.sample(
            range(self.num_cols * self.num_rows), self.num_mines)
        for idx in mine_indices:
            self.board[idx] = -1

        # Calculate the value of each non-mine cell
        for idx in range(self.num_cols * self.num_rows):
            if self.board[idx] == 0:
                self.board[idx] = self._calculate_value(idx)

        # Initialize the game state with a dict for each cell where the first value is False (revealed) and the second value is False (flagged)
        self.game_state = [{"revealed": False, "flagged": False}
                           for _ in range(self.num_cols * self.num_rows)]

    # Calculates the value of each non-mine cell based on the number of mines in the neighboring cells
    def _calculate_value(self, idx: int) -> int:
        # If the cell is a mine, return -1
        if self.board[idx] == -1:
            return -1

        # Get whether the cell is in the first/last row/column
        is_first_col = self._is_first_col(idx)
        is_last_col = self._is_last_col(idx)
        is_first_row = self._is_first_row(idx)
        is_last_row = self._is_last_row(idx)

        total_mines = 0

        # If the cell is not in the first column, check the left cell if it's a mine, if so increment the count
        total_mines += 1 if not is_first_col and self.board[idx - 1] == -1 else 0

        # If the cell is not in the last column, check the right cell if it's a mine, if so increment the count
        total_mines += 1 if not is_last_col and self.board[idx + 1] == -1 else 0

        # If the cell is not in the first row, check the top cell if it's a mine, if so increment the count
        total_mines += 1 if not is_first_row and self.board[idx -
                                                            self.num_cols] == -1 else 0

        # If the cell is not in the last row, check the bottom cell if it's a mine, if so increment the count
        total_mines += 1 if not is_last_row and self.board[idx +
                                                           self.num_cols] == -1 else 0

        # If the cell is not in the first row or first column, check the top-left cell if it's a mine, if so increment the count
        total_mines += 1 if not is_first_row and not is_first_col and self.board[idx -
                                                                                 self.num_cols - 1] == -1 else 0

        # If the cell is not in the first row or last column, check the top-right cell if it's a mine, if so increment the count
        total_mines += 1 if not is_first_row and not is_last_col and self.board[idx -
                                                                                self.num_cols + 1] == -1 else 0

        # If the cell is not in the last row or first column, check the bottom-left cell if it's a mine, if so increment the count
        total_mines += 1 if not is_last_row and not is_first_col and self.board[idx +
                                                                                self.num_cols - 1] == -1 else 0

        # If the cell is not in the last row or last column, check the bottom-right cell if it's a mine, if so increment the count
        total_mines += 1 if not is_last_row and not is_last_col and self.board[idx +
                                                                               self.num_cols + 1] == -1 else 0

        return total_mines

    def _is_first_col(self, idx: int) -> bool:
        """Checks if the given cell is in the first column of the board

        Args:
            idx (int): The cell to check

        Returns:
            bool: True if the cell is in the first column, False otherwise
        """
        return idx % self.num_cols == 0

    def _is_last_col(self, idx: int) -> bool:
        """Checks if the given cell is in the last column of the board

        Args:
            idx (int): The cell to check

        Returns:
            bool: True if the cell is in the last column, False otherwise
        """
        return idx % self.num_cols == self.num_cols - 1

    def _is_first_row(self, idx: int) -> bool:
        """Checks if the given cell is in the first row of the board

        Args:
            idx (int): The cell to check

        Returns:
            bool: True if the cell is in the first row, False otherwise
        """
        return idx < self.num_cols

    def _is_last_row(self, idx: int) -> bool:
        """Checks if the given cell is in the last row of the board

        Args:
            idx (int): The cell to check

        Returns:
            bool: True if the cell is in the last row, False otherwise
        """
        return idx >= self.num_cols * (self.num_rows - 1)

    def convert_idx_to_coords(self, idx: int) -> tuple:
        """Converts the 1D index to 2D coordinates

        Args:
            idx (int): The 1D index

        Returns:
            tuple: The 2D coordinates (row, col)
        """
        row = idx // self.num_cols
        col = idx % self.num_cols
        return row, col

    def convert_coords_to_idx(self, row: int, col: int) -> int:
        """Converts the 2D coordinates to 1D index

        Args:
            row (int): The row
            col (int): The column

        Returns:
            int: The 1D index
        """
        return row * self.num_cols + col

    def print_board(self):
        """Prints the board
        """
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                idx = self.convert_coords_to_idx(row, col)
                if self.board[idx] == -1:
                    print("*", end=" ")
                else:
                    print(self.board[idx], end=" ")
            print()

    def get_board(self):
        return self.board

    def get_total_mines(self):
        return self.num_mines

    def print_game_state(self):
        """Prints the game state
        """
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                idx = self.convert_coords_to_idx(row, col)
                if self.game_state[idx]["flagged"]:
                    print("F", end=" ")
                elif self.game_state[idx]["revealed"]:
                    print(self.board[idx], end=" ")
                else:
                    print("-", end=" ")
            print()

    def reveal(self, row: int, col: int):
        """Reveals the cell at the given coordinates

        Args:
            row (int): The row
            col (int): The column
        """
        idx = self.convert_coords_to_idx(row, col)
        self.game_state[idx]["revealed"] = True

        # If the cell is a mine, game over
        if self.board[idx] == -1:
            self.game_over = True

        # If the cell is empty, reveal all neighboring cells
        if self.board[idx] == 0:
            self._reveal_neighbors(row, col)

    def flag(self, row: int, col: int):
        """Flags the cell at the given coordinates

        Args:
            row (int): The row
            col (int): The column
        """
        idx = self.convert_coords_to_idx(row, col)
        self.game_state[idx]["flagged"] = not self.game_state[idx]["flagged"]

    def _reveal_neighbors(self, row: int, col: int):
        """Reveals all neighboring cells of the given cell

        Args:
            row (int): The row
            col (int): The column
        """
        # Get whether the cell is in the first/last row/column
        is_first_col = self._is_first_col(self.convert_coords_to_idx(row, col))
        is_last_col = self._is_last_col(self.convert_coords_to_idx(row, col))
        is_first_row = self._is_first_row(self.convert_coords_to_idx(row, col))
        is_last_row = self._is_last_row(self.convert_coords_to_idx(row, col))

        # Check all neighboring cells and reveal them if they are not mines and not already revealed
        if not is_first_col:
            self._reveal_cell(row, col - 1)
        if not is_last_col:
            self._reveal_cell(row, col + 1)
        if not is_first_row:
            self._reveal_cell(row - 1, col)
        if not is_last_row:
            self._reveal_cell(row + 1, col)
        if not is_first_row and not is_first_col:
            self._reveal_cell(row - 1, col - 1)
        if not is_first_row and not is_last_col:
            self._reveal_cell(row - 1, col + 1)
        if not is_last_row and not is_first_col:
            self._reveal_cell(row + 1, col - 1)
        if not is_last_row and not is_last_col:
            self._reveal_cell(row + 1, col + 1)

    def _reveal_cell(self, row: int, col: int):
        """Reveals the cell at the given coordinates if it's not a mine and not already revealed

        Args:
            row (int): The row
            col (int): The column
        """
        idx = self.convert_coords_to_idx(row, col)
        if not self.game_state[idx]["revealed"] and self.board[idx] != -1:
            self.game_state[idx]["revealed"] = True
            if self.board[idx] == 0:
                self._reveal_neighbors(row, col)

    def check_win(self) -> bool:
        """Checks if the game is won

        Returns:
            bool: True if the game is won, False otherwise
        """
        for idx in range(self.num_cols * self.num_rows):
            if not self.game_state[idx]["revealed"] and self.board[idx] != -1:
                return False
        return True

    def check_loss(self) -> bool:
        """Checks if the game is lost

        Returns:
            bool: True if the game is lost, False otherwise
        """
        return self.game_over
