import battleship as bs

def place_ship_manually(board, size):
    print(f"\nPosicionando navio de tamanho {size}")

    row = int(input("Linha inicial: "))
    col = int(input("Coluna inicial: "))
    direction = input("Direção (h para horizontal, v para vertical): ").lower()

    positions = []

    for i in range(size):
        if direction == "h":
            positions.append((row, col + i))
        elif direction == "v":
            positions.append((row + i, col))
        else:
            print("Direção inválida.")
            return place_ship_manually(board, size)

    ship = bs.Ship(size)
    ship.place(positions)
    board.add_ship(ship)

game = bs.Game()

# ----------------------
# Posicionamento
# ----------------------

print("=== Jogador 1 posicionando navios ===")
place_ship_manually(game.player1, 3)
place_ship_manually(game.player1, 2)

print("\n" * 50)  # limpa tela simples

print("=== Jogador 2 posicionando navios ===")
place_ship_manually(game.player2, 3)
place_ship_manually(game.player2, 2)

print("\n" * 50)

# ----------------------
# Loop do jogo
# ----------------------

while True:
    print(f"\n=== Turno do Jogador {game.current_player} ===")

    opponent_board = game.get_opponent_board()
    opponent_board.display(show_ships=False)

    row = int(input("Atacar linha: "))
    col = int(input("Atacar coluna: "))

    result = game.attack(row, col)
    print(result)

    if opponent_board.all_ships_sunk():
        print(f"Jogador {game.current_player} venceu!")
        break
