import battleship as bs

class Board:
    def __init__(self, size: int = 10):
        self.size = size
        self.grid = [["~" for _ in range(size)] for _ in range(size)]
        self.ships: list[bs.Ship] = []

    # Mostrar tabuleiro
    def display(self, show_ships: bool = True):
        # 🔢 Linha do topo (números das colunas)
        print("   ", end="")
        for col in range(self.size):
            print(col, end=" ")
        print()

        # 🔢 Linhas com número na lateral
        for row_index, row in enumerate(self.grid):

            print(f"{row_index:2} ", end="")

            for cell in row:
                if not show_ships and cell == "S":
                    print("~", end=" ")
                else:
                    print(cell, end=" ")

            print()  # quebra linha
    
    # Verificar se posição é válida
    def _is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size
    
    # Adicionar navio
    def add_ship(self, ship: bs.Ship):
        for row, col in ship.positions:
            if not self._is_valid_position(row, col):
                raise ValueError("Navio fora do tabuleiro.")
            
            if self.grid[row][col] != "~":
                raise ValueError("Já existe algo nessa posição.")
            
        for row, col in ship.positions:
            self.grid[row][col] = "S"
        
        self.ships.append(ship)

    # Atirar
    def shoot(self, row: int, col: int) -> str:
        if not self._is_valid_position(row, col):
            raise ValueError("Tiro fora do tabuleiro.")

        cell = self.grid[row][col]

        if cell == "X" or cell == "O":
            return "Posição já atingida."

        if cell == "S":
            self.grid[row][col] = "X"

            # descobrir qual navio foi atingido
            for ship in self.ships:
                if (row, col) in ship.positions:
                    ship.hits.add((row, col))
                    if ship.is_sunk():
                        return "Navio afundado!"
                    return "Acertou!"

        else:
            self.grid[row][col] = "O"
            return "Água."

    # Verificar vitória
    def all_ships_sunk(self) -> bool:
        return all(ship.is_sunk() for ship in self.ships)

    