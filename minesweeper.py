import random

class Minesweeper:
    """
    A class representing the Minesweeper game.

    This class handles the game logic, including board setup, mine placement, and player interactions.
    It supports uncovering cells, flagging cells, and checking for win conditions.
    """
    def __init__(self, size=5, mines=5):
        self.size = size
        self.mines = mines
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.visible_board = [['-' for _ in range(size)] for _ in range(size)]
        self.mine_positions = set()
        self.generate_board()

    def generate_board(self):
        """Place mines and calculate numbers for the board."""
        while len(self.mine_positions) < self.mines:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            self.mine_positions.add((x, y))

        for x, y in self.mine_positions:
            self.board[x][y] = 'M'

        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != 'M':
                    self.board[x][y] = str(self.count_adjacent_mines(x, y))

    def count_adjacent_mines(self, x, y):
        """Count the number of mines adjacent to a cell."""
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == 'M':
                count += 1
        return count

    def display_board(self):
        """Display the visible board."""
        print("  " + " ".join(map(str, range(self.size))))
        for i, row in enumerate(self.visible_board):
            print(f"{i} " + " ".join(row))

    def uncover(self, x, y):
        """Uncover a cell."""
        if (x, y) in self.mine_positions:
            print("Boom! You hit a mine!")
            self.reveal_all()
            return True

        self.flood_fill(x, y)
        return False

    def flag(self, x, y):
        """Flag or unflag a cell."""
        if self.visible_board[x][y] == '-':
            self.visible_board[x][y] = 'F'
        elif self.visible_board[x][y] == 'F':
            self.visible_board[x][y] = '-'

    def flood_fill(self, x, y):
        """Uncover cells recursively if they are empty."""
        if not (0 <= x < self.size and 0 <= y < self.size) or self.visible_board[x][y] != '-':
            return

        self.visible_board[x][y] = self.board[x][y]

        if self.board[x][y] == '0':
            for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                self.flood_fill(x + dx, y + dy)

    def reveal_all(self):
        """Reveal the entire board."""
        self.visible_board = [row[:] for row in self.board]

    def check_win(self):
        """Check if the player has won."""
        for x in range(self.size):
            for y in range(self.size):
                if self.visible_board[x][y] == '-' and self.board[x][y] != 'M':
                    return False
        return True

def play_minesweeper():
    size = int(input("Enter the size of the board: "))
    mines = int(input("Enter the number of mines: "))

    game = Minesweeper(size, mines)

    while True:
        game.display_board()
        action = input("Choose an action (uncover/flag): ").lower()
        x, y = map(int, input("Enter coordinates (row col): ").split())

        if action == 'uncover':
            if game.uncover(x, y):
                print("Game Over!")
                break
        elif action == 'flag':
            game.flag(x, y)
        else:
            print("Invalid action! Choose 'uncover' or 'flag'.")

        if game.check_win():
            print("Congratulations! You won!")
            game.reveal_all()
            break

    game.display_board()

if __name__ == "__main__":
    play_minesweeper()
