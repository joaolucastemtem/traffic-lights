import semaforo  # Check semaforo.py for a lot more information, it defines important functions.


len_square = 170  # 170 100  150
len_space = 8     # 8   5    7
board = [[0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]]
# list_of_turns = [True, False]  # True corresponds to the computer's turn and False to the player's turn.
# depth = 4
# difficulty = "hard"


list_of_turns, depth, difficulty = semaforo.menu_loop()

semaforo.game_loop(board, len_square, len_space, list_of_turns, depth, difficulty)
