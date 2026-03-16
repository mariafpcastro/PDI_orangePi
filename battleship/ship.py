class Ship:
    def __init__(self, size: int):
        self.size = size    # Tamanho do navio
        self.positions = [] # Armazena as coordenadas do tabuleiro
        self.hits = set()   # Guarda posições que já foram atingidas

    def place(self, positions: list[tuple[int, int]]):
        if len(positions) != self.size:
            raise ValueError("Numero de posicoes diferente do tamanho do navio.")
        
        rows = [pos[0] for pos in positions]
        cols = [pos[1] for pos in positions]

        # Caso horizontal -> todas as linhas iguais
        if len(set(rows)) == 1:
            sorted_cols = sorted(cols)
            if sorted_cols != list(range(min(cols), min(cols) + self.size)):
                raise ValueError("Navio horizontal deve estar em sequencia.")
        
        #Caso vertical -> todas as colunas iguais
        elif len(set(cols)) == 1:
            sorted_rows = sorted(rows)
            if sorted_rows != list(range(min(rows), min(rows) + self.size)):
                raise ValueError("Navio vertical deve estar em sequencia.")
        
        else:
            raise ValueError("Navio deve ser totalmente horizontal ou vertical.")
        
        self.positions = positions
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

    def is_sunk(self) -> bool:
        return len(self.hits) == self.size