import battleship as bs


class Game:
    def __init__(self, size: int = 10):
        self.player1 = bs.Board(size)
        self.player2 = bs.Board(size)
        self.current_player = 1

    def switch_turn(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    def get_current_board(self):
        if self.current_player == 1:
            return self.player1
        return self.player2

    def get_opponent_board(self):
        if self.current_player == 1:
            return self.player2
        return self.player1

    def attack(self, row: int, col: int) -> str:
        opponent_board = self.get_opponent_board()
        result = opponent_board.shoot(row, col)

        if not opponent_board.all_ships_sunk():
            self.switch_turn()

        return result