"""
Made by João Lucas Temtem
Current version: 25/july/2020

This is an implementation of the game "Traffic Lights" or "Semáforo" in portuguese, using python and pygame.

Check the file main.py, which "applys" the functions that this file defines.

The parts of this program that lead with the user, such as the messages displayed in the console, are in portuguese. It is obvious that this should communicate with the user in portuguese since this was made to be used by students in Portugal.

This is not the final versio yet.
I've to make this code "clean" and I've commented, I've tried to follow PEP-8.
"""

import pygame
from copy import deepcopy  # To help copying lists und so weiter.
from random import randint

try:
    import replit
    replit.clear()
except:
    pass

### The next part is building the bones of Semáforo without pygame  (kind of the backend):

def create_board(n_cols, n_rows):
    """Create a board with n_cols columns and n_rows rows."""
    return [[0 for i in range(n_cols)] for i in range(n_rows)]


def print_board(board):
    """Displays semáforo's board in the console."""
    for i in range(3):
        for j in range(4):
            if board[i][j] == 0:
                print("⬜", sep='', end=' ')
            elif board[i][j] == 1:
              print("🟢", sep='', end=' ')
            elif board[i][j] == 2:
              print("⚠️", sep='', end=' ')
            elif board[i][j] == 3:
              print("🟥", sep='', end=' ')
        print()


def is_legal_move(board, move):
    """Returns True is the move is legal, False otherwise."""
    if not(isinstance(move, list) or isinstance(move, tuple) or isinstance(move, str)):
        return False
    if len(move) != 2:
        return False
    if not(isinstance(move[0], int)) or not(isinstance(move[1], int)):
        return False
    if (move[0] not in [0,1,2]) or (move[1] not in [0,1,2,3]):
        return False
    if someone_won(board):
        return False
    return board[move[0]][move[1]] != 3


def someone_won(board, turn=0):
    """Returns True if the game has finished, False otherwise."""
    return (0 != board[0][0] == board[0][1] == board[0][2])\
        or (0 != board[0][1] == board[0][2] == board[0][3])\
        or (0 != board[1][0] == board[1][1] == board[1][2])\
        or (0 != board[1][1] == board[1][2] == board[1][3])\
        or (0 != board[2][0] == board[2][1] == board[2][2])\
        or (0 != board[2][1] == board[2][2] == board[2][3])\
        or (0 != board[0][0] == board[1][0] == board[2][0])\
        or (0 != board[0][1] == board[1][1] == board[2][1])\
        or (0 != board[0][2] == board[1][2] == board[2][2])\
        or (0 != board[0][3] == board[1][3] == board[2][3])\
        or (0 != board[0][0] == board[1][1] == board[2][2])\
        or (0 != board[0][1] == board[1][2] == board[2][3])\
        or (0 != board[2][0] == board[1][1] == board[0][2])\
        or (0 != board[2][1] == board[1][2] == board[0][3])


def play_move(board, move, turn=0):
    """Plays a move in the board,
    note that this function CHANGES the list board
    if the move is legal!"""
    if is_legal_move(board, move):
      board[move[0]][move[1]] += 1
      return board


def possible_positions(board, turn=0):
    """Returns a list with possible the positions that the
    board can have after the next move."""
    list_of_positions = []
    for i in range(3):
        for j in range(4):
            if board[i][j] != 3:
                new_board = deepcopy(board)
                new_board[i][j] += 1
                list_of_positions.append(new_board)
    return list_of_positions


def randomise_the_beginning(sequence):
    """Receives a list just as [0, 1, 2, 3, 4, 5]
    and returns a list with the same order than the argument
    but starting in a randomised item
    Eg, that input can result in ouput: [3, 4, 5, 0, 1,2] or [2 , 3, 4, 5, 0, 1]"""
    new_sequence=[0 for i in range(len(sequence))]
    i = randint(0, len(sequence)-1)
    for j in range(len(sequence)):
        new_sequence[j] = sequence[i]
        i += 1
        if i == len(sequence):
            i = 0
    return new_sequence


def static_evaluation(board, turn, n):
    """Returns the evaluation of a position.
    The higher the evaluation is, the better the position is for "me".    
    It receivies the list board, turn and n:
    A positive evaluation means that it is considered that the player with the turn is better, while a postive evaluation means that the player is worst. Winning or losing means that there is a forced win or loss.
    board: is just the current position.

    turn:
    turn==1 means that it is "my" turn in this postion so I want to win now, 
    turn==-1 means that it is "my" opponent's turn.
  
    n:
    n is the number of turns of the game until now
    n is used to tell the computer that a quick win is better
    than a long win, and that a long defeat is better than a quik defeat since
    the computer will use minimax and it assumes opponent's perfect play.
    n is important for it not to commit "suicide". Eg, if the computer sees that
    its opponent has a forced win, it will not play any move, it will play
    the move that keeps it alive for the longest. Likewise, if he knows it
    has a forced win, it win play the fastest forced win. This work because
    a quick win is evaluated with a higher number than a long win and a quick
    loss is evaluated with a lower number than a quick loss. 
    So, it is evident the number of turns is important to help us choose
    a quick win or a long defeat rather than a long win or a quick defeat. 
    """
    if someone_won(board):
        return -turn * (100-n)  # n is basically, a quick win is better than a delayed win and a quick loss is worst than a delayed loss.
    return 0  # If the game has not ended, the position is evaluated as neutral.


def minimax(board, depth, turn=1, alpha=-200, beta=200, n=1):
    """ minimax with alpha and beta! Returns number saying how good the postion is.
    The variables turn and n are here to "help" the funtion static_evaluation()

    turn:
    turn==1 means that it is "my" turn in this postion so I want to win now, 
    turn==-1 means that it is "my" opponent's turn.

    n:
    n is the number of turns of the game until now
    n is used to tell the computer that a quick win is better
    than a long win, and that a long defeat is better than a quik defeat since
    the computer will use minimax and it assumes opponent's perfect play.
    n is important for it not to commit "suicide". Eg, if the computer sees that
    its opponent has a forced win, it will not play any move, it will play
    the move that keeps it alive for the longest. Likewise, if he knows it
    has a forced win, it win play the fastest forced win. This work because
    a quick win is evaluated with a higher number than a long win and a quick
    loss is evaluated with a lower number than a quick loss. 
    So, it is evident the number of turns is important to help us choose
    a quick win or a long defeat rather than a long win or a quick defeat.  
    """
    if depth == 0 or someone_won(board):
        return static_evaluation(board, turn, n)
    
    if turn == 1:
        max_evalu = -1
        for child in possible_positions(board):
            evalu=minimax(child, depth-1, -1, alpha, beta, n+1)
            max_evalu = max(max_evalu, evalu)
            alpha = max(alpha, evalu)
            if beta <= alpha:
                break
        return max_evalu

    else:
        min_evalu=1
        for child in possible_positions(board):
            evalu = minimax(child, depth-1, 1, alpha, beta, n+1)
            min_evalu = min(min_evalu, evalu)
            beta = min(beta,evalu)
            if beta <= alpha:
                break
        return min_evalu


def make_user_choose(board):
    """Receives a board and returns a move inputted by the user in console.
    This "safe" because this function forces the user to input a legal move.
    """
    move = [-1, -1]
    while not(is_legal_move(board, move)):
        move[0] = int(input("Linha: "))-1
        move[1] = int(input("Coluna: "))-1
    return move


def make_computer_choose(board, depth, turn=1):
    """Receives a list board, a depth and turn
    and returns a move chosen by the computer using minimax.
    
    The computer will see possible_positions(board) and return the move that leads to the postion he thinks is best for it.

    turn==1 means that it is "my" turn in this postion so I want to win now, 
    turn==-1 means that it is "my" opponet's turn. So, generally turn==1
    beacause we want the computer to decide its move when it's its turn.

    The depth is the number of moves that the computer will see aheah,
    if depth==1 it will only see if it can win in its move
    if depth==2 it will see if it can win in the next move
    and see if it will not lose in opponent's move
    etc.
    """
    list_of_values = []
    list_of_evals = []

    for i in randomise_the_beginning([0, 1, 2]):
        for j in randomise_the_beginning([0, 1, 2, 3]):
            if not(is_legal_move(board, [i, j])):
                continue
            list_of_values.append([i, j])
            list_of_evals.append(minimax(play_move(deepcopy(board), [i, j]), depth-1, -turn))
    
    if turn == 1:
        return list_of_values[list_of_evals.index(max(list_of_evals))]
    else:
        return list_of_values[list_of_evals.index(min(list_of_evals))]


def get_notation_move(move, reverse = False):
    """ if reverse, receives something such as "c3"
    and returns (0,2), else recieves (0, 2) and returns "c3".
    """
    rows = ['3', '2', '1']
    cols = ['a', 'b', 'c', 'd']
    if reverse:
        return rows.index(move[1]), cols.index(move[0])
    return cols[move[1]] + rows[move[0]]

### The next part is Semáforo with pygame (kind of the frontend):

def create_window_for_board(n_cols, n_rows, len_square, len_space):
    """Creates a window with just the right space to a board with
    n_cols columns, n_rows rows, squares in length len_square and separated
    by a margin with length equal to len_space.
    """
    return pygame.display.set_mode((n_cols*len_square + (n_cols+1)*len_space, (n_rows)*len_square + (n_rows+1)*len_space))

    #return pygame.display.set_mode((0,0), pygame.FULLSCREEN)  # Make the window go full screen.


def draw_squares(window,  n_cols, n_rows, len_square, len_space, color=(255,255,255)):
    """Draws the squares of aboard in a previously created window (see create_window_for_board()) with
    n_cols columns, n_rows rows, squares in length len_square and separated
    by a margin with length equal to len_space.
    and RETURNS squares_list, a list with the coordinates of which square which is way too useful!
    """
    squares_list = []

    if (window.get_width() < 4*len_square + 5*len_space) or (window.get_height() < 3*len_square + 4*len_space):
        return "Erro"

    y=len_space  
    for i in range(n_rows):
        to_add_list = []
        x = len_space
        for j in range(n_cols):      
            to_add_list.append(pygame.draw.rect(window, color, (x, y, len_square, len_square)))
            x += len_square + len_space    
        y += len_square + len_space
        squares_list.append(deepcopy(to_add_list))
    
    return squares_list

### Making the board showed by pygame responsive (kind of connecting backend and frontend):

def clicked_in_which_square(pos, squares_list):
    """Return the square in which pos is
    From example is the mouse clicked in pos, a certain square in the screen,
    this function finds it and return [2,3] for instance.
    Pretty useful!"""
    for y in range(len(squares_list)):
        for x in range(len(squares_list[0])):
            if squares_list[y][x].collidepoint(pos):
                return (y, x)
    return None


def update_board(window, board, move, squares_list):
    """Paints the board with the correct color. For example:
    If board[0][0]==1 and move=[0,0], this function
    will update the first square and put it green. 
    Note that we need pygame.display.update() after this fuction so that it really shows the alteration.
    """
    i = move[0]
    j = move[1]
    square = squares_list[i][j]
    color = (255, 255, 255)
    
    pygame.draw.rect(window, color, (square[0], square[1], square[2], square[3]))  # Paint a white square.
    if board[i][j] == 1:
        color=(0,255,0)
    if board[i][j] == 2:
        color=(255,255,0)
    if board[i][j] == 3:
        color=(255,0,0)
    pygame.draw.rect(window, color, (square[0], square[1], square[2], square[3]))  # Paint the square with the chosen color.


def next_interation(list_of_turns, current_turn):
    """Returns the next interation in list_of_turns.
    This is used to know if it is a human or the computer's turn to play,
    I think I might improve this function later, like generalising it.
    """
    if list_of_turns == [True, True]:
        return True
    if list_of_turns == [False, False]:
        return False
    if list_of_turns == [True, False] or list_of_turns==[False, True]:
        return not(current_turn)
    print("Deu asneira")

### Loops: menu and the game itself:

def game_loop(board, len_square, len_space, list_of_turns, depth, difficulty):
    """Game loop in pygame.
    Receives the board, in valid position.
    Receives len_square and len_space to draw the squares with a specific space between them.
    Receives list_of_turns, if list_of_turns == [True, True], this means that the game is human vs human
    If it is [True, False] it means that the game is human vs machine and the human starts. You got the idea.
    Depth is how many moves the computer will "see ahead" to chose its move
    And difficulty is a string that describes the mode in which the computer is playing
    for instance, "muito fácil" means it is very easy, only one move ahead.
    """
    initial_board = deepcopy(board)
    n_cols = 4          
    n_rows = 3 
    color_of_squares = (255, 255, 255)

    pygame.init()
    window = create_window_for_board(n_cols, n_rows, len_square, len_space)
    #window.fill((0,0,0))  # Paint the whole window of black.

    squares_list= draw_squares(window, n_cols, n_rows, len_square, len_space, color_of_squares)

    # Variables that need to start with these values:
    run = True
    is_user_turn = list_of_turns[0]
    is_turn_of_first_player = True
    list_of_moves = []

    list_of_captions = ["Jogador %d, é a tua vez!"%(i) if list_of_turns[i-1] else "O computador no modo %s (%d) está a pensar..."%(difficulty, i) for i in (1,2)]
    
    try:
        replit.clear()
    except:
        pass

    print("Semáforo:")
    print_board(board)
    
    for i in range(3):  # By doing this, the screen updates everything in the beginning, so we can star the game at any position, pretty good :D
        for j in range(4):
            update_board(window, board, (i,j), squares_list)
    
    print(list_of_captions[not(is_turn_of_first_player)])
    pygame.display.set_caption(list_of_captions[not(is_turn_of_first_player)])

    pygame.display.update()

    while run:
        pygame.time.delay(100)
        new_move = False  # This will become True when a valid move is chosen
        if is_user_turn:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    move=clicked_in_which_square(pygame.mouse.get_pos(), squares_list)
                    # Chosing the move when mouse is pressed but this will only be the chosen move by the player if the mouse goes up in the same square.
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if move == clicked_in_which_square(pygame.mouse.get_pos(), squares_list) and is_legal_move(board, move): 
                        new_move = True  # Only if the mouse went down and up in the same square, will the move be considered valid.
                if event.type == pygame.KEYDOWN and event.unicode == 'r':  # Restart the game.
                    board = deepcopy(initial_board)
                    is_user_turn = list_of_turns[0]
                    is_turn_of_first_player = True
                    list_of_moves = []
                    
                    print("O jogo foi reiniciado.")
                    print("Semáforo:")
                    print_board(board)
                    
                    for i in range(3):
                        for j in range(4):
                            update_board(window, board, (i,j), squares_list)
                    
                    print(list_of_captions[not(is_turn_of_first_player)])
                    pygame.display.set_caption(list_of_captions[not(is_turn_of_first_player)])

        else:
            move = make_computer_choose(board, depth)
            new_move = True  # Well, we are assuming that the computer choses a valid move... but who cares.
            pygame.event.get()  # To stop the player from doing unwanted "premoves". Pretty happy when I "discovered" this.
        
        if new_move:  # If the chosen move is valid, then play it and display it.
            play_move(board, move)  # This changes the board.
            print_board(board)
            update_board(window, board, move, squares_list)  # Update the changed square in pygame's window.            
            list_of_moves.append(move)

            if not(someone_won(board)):
                print(list_of_captions[is_turn_of_first_player])
                pygame.display.set_caption(list_of_captions[is_turn_of_first_player])
            
            is_turn_of_first_player = not(is_turn_of_first_player)
            is_user_turn = next_interation(list_of_turns, is_user_turn)            
    
        pygame.display.update()
    
        if someone_won(board):
            run = False

    if is_turn_of_first_player:  # To get the after game caption.
        if list_of_turns[1]:
            if list_of_turns == [True, True]:
               after_game_caption = "O jogador 2 ganhou!"
            else:
               after_game_caption = "O jogador 2 ganhou contra o computador no modo %s!"%(difficulty)
        else:  
            after_game_caption = "O computador no modo %s (2) ganhou!"%(difficulty)
    else:
        if list_of_turns[0]:
            if list_of_turns == [True, True]:
                after_game_caption = "O jogador 1 ganhou!"
            else:
                after_game_caption = "O jogador 1 ganhou contra o computador no modo %s!"%(difficulty)
        else:  
            after_game_caption = "O computador no modo %s (1) ganhou!"%(difficulty)

    pygame.display.set_caption(after_game_caption)
    pygame.display.update()
    
    print(after_game_caption)
    input("...")
    pygame.quit()
    list_of_algebraric_moves = [get_notation_move(move) for move in list_of_moves]
    print(list_of_algebraric_moves)

def menu_loop():
    """Menu that is displayed before the game with options."""

    width = 700
    height = 500

    pygame.init()
    
    window = pygame.display.set_mode((width, height))
    # window.fill((80,80,180))  # Paint the window with a shade of blue.
    # pygame.display.set_caption("Semáforo")

    color_of_text=(0,0,0)
    font = pygame.font.Font(None, 50)

    caption_1 = "Começar a partir:"
    caption_2 = "Queres jogar contra quem?"
    caption_3 = "Dificuldade"
    caption_4 = "Quem começa?"

    list_of_captions = [caption_1, caption_2, caption_3, caption_4]

    text_a1 = font.render("Da posição inicial", True, color_of_text)
    text_a2 = font.render("De uma posição escolhida", True, color_of_text)

    text_b1 = font.render("Contra um(a) amigo(a)", True, color_of_text)
    text_b2 = font.render("Contra o computador", True, color_of_text)

    text_c1 = font.render("Muito fácil", True, color_of_text)
    text_c2 = font.render("Fácil", True, color_of_text)
    text_c3 = font.render("Médio", True, color_of_text)
    text_c4 = font.render("Difícil", True, color_of_text)

    text_d1 = font.render("Eu", True, color_of_text)
    text_d2 = font.render("O computador", True, color_of_text)

    list_of_text = [[text_a1, text_a2], [text_b1, text_b2],[text_c1, text_c2, text_c3, text_c4], [text_d1, text_d2]]

    list_of_coords = [[(100,150), (100,350)], [(100,150), (100,350)], [(100, 150), (425,150), (100, 350), (425,350)], [(100,150), (100,350)]]

    button_a1 = pygame.draw.rect(window, (255,255,255), (50,100,600,100))
    button_a2 = pygame.draw.rect(window, (255,255,255), (50,300,600,100))

    button_b1 = pygame.draw.rect(window, (255,255,255), (50,100,275,100))
    button_b2 = pygame.draw.rect(window, (255,255,255), (375,100,275,100))
    button_b3 = pygame.draw.rect(window, (255,255,255), (50,300,275,100))
    button_b4 = pygame.draw.rect(window, (255,255,255), (375,300,275,100))


    try:
        replit.clear()
    except:
        pass

    run = True
    option = 0
    list_of_options = [0, 0, 0, 0]
    c = 0
    while run:
        pygame.time.delay(100)
        if c != 0: # The fisrt option is not being displayed!
            pygame.display.set_caption(list_of_captions[c])
            #            R    G    B 
            window.fill((80,80,180))  # Paint the screen of a shade of blue so that the previous button "disappear"
            if c != 2:
                button_a1 = pygame.draw.rect(window, (255,255,255), (50,100,600,100))
                button_a2 = pygame.draw.rect(window, (255,255,255), (50,300,600,100))
                for i in range(2):
                    window.blit(list_of_text[c][i], list_of_coords[c][i])
            else:
                button_b1 = pygame.draw.rect(window, (255,255,255), (50,100,275,100))
                button_b2 = pygame.draw.rect(window, (255,255,255), (375,100,275,100))
                button_b3 = pygame.draw.rect(window, (255,255,255), (50,300,275,100))
                button_b4 = pygame.draw.rect(window, (255,255,255), (375,300,275,100))
                for i in range(4):
                    window.blit(list_of_text[c][i], list_of_coords[c][i])
                
            pygame.display.update()

            valid_option=False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    raise "Erro, interrupção"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if c != 2:
                        if button_a1.collidepoint(pos):
                            option = 1
                        elif button_a2.collidepoint(pos):
                            option = 2
                    else:
                        if button_b1.collidepoint(pos):
                            option = 1
                        elif button_b2.collidepoint(pos):
                            option = 2
                        elif button_b3.collidepoint(pos):
                            option = 3
                        elif button_b4.collidepoint(pos):
                            option = 4
                
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos= pygame.mouse.get_pos()
                    if c != 2:
                        if button_a1.collidepoint(pos) and option == 1:
                            valid_option=True
                        elif button_a2.collidepoint(pos) and option == 2:
                            valid_option=True
                    else:
                        if button_b1.collidepoint(pos) and option == 1:
                            valid_option = True
                        elif button_b2.collidepoint(pos) and option == 2:
                            valid_option = True
                        elif button_b3.collidepoint(pos)and option == 3:
                            valid_option = True
                        elif button_b4.collidepoint(pos) and option == 4:
                            valid_option = True
    
            pygame.display.update()

            if valid_option:
                list_of_options[c] = option
                if c==3:
                    run=False
                    break
                elif list_of_options[1] == 1:
                    run = False
                    break
                c +=1
        else:
            c += 1
    pygame.quit()

    depth=0

    if list_of_options[0]==1:
        pass
    else:
        if list_of_options[1] == 1:
            list_of_turns = [True, True]
        else:
            if list_of_options[3]==1:
                list_of_turns = [True, False]
            else:
                list_of_turns = [False, True]

            if list_of_options[2] == 1:
                depth = 1
            elif list_of_options[2] == 2:
                depth = 2
            elif list_of_options[2] == 3:
                depth = 4
            elif list_of_options[2] == 4:
                depth = 6    
    
    n_difficulty = list_of_options[2]

    list_of_difficulties = ["muito fácil", "fácil", "médio", "difícil"]

    difficulty = list_of_difficulties[n_difficulty-1]

    return list_of_turns, depth , difficulty
