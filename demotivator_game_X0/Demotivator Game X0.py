import random
game_name = 'C R O S S - Z E R O'
lgm = len(game_name)
# left and right print borders
lb, rb = 'X0X**   ', '   **X0X'
llb = len(lb)
# options for what_to_do()
wtd = ['MAKE YOUR CHOICE ',
       '1 - play ',
       '2 - X or 0 choice',
       '9 - exit '
       ]
lwtd = [len(x) for x in wtd]
# options for xo_choice()
xoch = ['MAKE YOUR CHOICE ',
        'X -you start first ',
        '0 -you start second'
        ]
lxoch = [len(x) for x in xoch]
# options for game_result()
rst = ['Games played: ',
       'Win:          ',
       'Draw:         ',
       'Lost:         '
       ]
lrst = [len(x) for x in rst]
# options for exit()
ext = ['NO CHANCE TO WIN!',
       'GOOD TRY!',
       'SEE YOU SOON!'
       ]
lext = [len(x) for x in ext]

xo = ''
game_played = 0
game_win = 0
game_lost = 0


def upper_border():
    # Print upper border
    print(f'{"_" * (lgm + 2 * llb)}')
    print(f'{"X0" * (int(lgm/2) + llb)}X')
    print(f'X0X{"*" * (lgm + 2 * llb - 6)}X0X')
    print(f'{lb}{" " * lgm}{rb}')


def lower_border():
    # Print lower border
    print(f'{lb}{" " * lgm}{rb}')
    print(f'X0X{"*" * (lgm + 2 * llb - 6)}X0X')
    print(f'{"X0" * (int(lgm/2) + llb)}X')


def greeting():
    # Print greeting window
    print(f'{" " * (lgm + 2 * llb - len("MapleBloom Co"))}MapleBloom Co')
    upper_border()
    print(f'{lb}W E L C O M E{" " * (lgm - len("W E L C O M E") - len("T O"))}T O{rb}')
    print(f'{lb}{game_name}{rb}')
    print(f'{lb}{" " * int((lgm - len("G A M E"))/2)}G A M E{" " * int((lgm - len("G A M E"))/2)}{rb}')
    lower_border()
    input('Enter to start >>>>>')


def what_to_do():
    # Print main menu window and return choice
    upper_border()
    for i in range(len(wtd)):
        print(f'{lb}{" " * int((lgm - lwtd[i])/2)}{wtd[i]}{" " * int((lgm - lwtd[i])/2)}{rb}')
    lower_border()
    return input('Enter your choice >>>>>')


def xo_choice():
    # Print menu and return choice of X or 0
    while True:
        upper_border()
        for i in range(len(xoch)):
            print(f'{lb}{" " * int((lgm - lxoch[i])/2)}{xoch[i]}{" " * int((lgm - lxoch[i])/2)}{rb}')
        lower_border()
        xo_ = input('Enter X or 0 >>>>>')
        if xo_ == 'x':
            xo_ = 'X'
        if xo_ == 'o' or xo_ == 'O':
            xo_ = '0'
        if xo_ == 'X' or xo_ == '0':
            return xo_
        print(f"\n{xo_} doesn't play this game!")


def game_start(xop):
    # Game part: print current board, wait player's turn, check and return game result
    game_board = [[' ' for _ in range(3)] for _ in range(3)]   # empty game board
    xoc = '0' if xop == 'X' else 'X'     # xop - player, xoc - comp
    if xop == '0':
        game_board[1][1] = 'X'           # X-comp always start at center
    while True:
        print_board(game_board, xop)
        while True:                      # check player's turn input
            try:
                i, j = map(int, input('Enter your turn with space >>>>>').split(' '))
            except ValueError:
                print('\n' + 'Your choice should be two integers')
                print('in range from 1 to 3 divided by space')
                continue
            if i < 1 or i > 3 or j < 1 or j > 3:
                print('\n' + 'Your choice is out of range')
                continue
            if game_board[i-1][j-1] != ' ':
                print('\n' + 'Cell is already engaged')
                continue
            game_board[i-1][j-1] = xop   # remember player's turn
            break
        if win_check(xop, game_board):                                # check board after player's turn
            print_board(game_board, xop)
            return 'YOU WIN !!!'
        if draw_check(game_board):
            print_board(game_board, xop)
            return 'DRAW ;)'
        game_board = comp_turn(xop, xoc, game_board, i - 1, j - 1)    # receive comp turn
        if win_check(xoc, game_board):                                # check board after comp turn
            print_board(game_board, xop)
            return 'Lost this time...'
        if draw_check(game_board):
            print_board(game_board, xop)
            return 'DRAW ;)'


def print_board(board, player):
    # Print the current state of the board
    upper_border()
    print(f'{lb}{" " * int((lgm - 13)/2 - 4)}{player}    1   2   3  {" " * int((lgm - 13)/2)}{rb}')
    print(f'{lb}{" " * int((lgm - 13)/2)}{"_" * 13}{" " * int((lgm - 13)/2)}{rb}')
    for i in range(3):
        print(f'{lb}{" " * int((lgm - 13)/2-3)}{i+1}  '
              f'| {board[i][0]} | {board[i][1]} | {board[i][2]} |'
              f'{" " * int((lgm - 13)/2)}{rb}')
        print(f'{lb}{" " * int((lgm - 13)/2)}|___|___|___|{" " * int((lgm - 13)/2)}{rb}')
    lower_border()


def win_check(xow, board):
    # For turn made check filled diagonal, horizontal or vertical. If True -> the last turn win.
    player = xow
    if sum(1 for i in range(3) if board[i][i] == player) == 3 \
            or sum(1 for i in range(3) if board[i][2-i] == player) == 3:
        return True
    for i in range(3):
        if sum(1 for j in range(3) if board[i][j] == player) == 3:
            return True
    for j in range(3):
        if sum(1 for i in range(3) if board[i][j] == player) == 3:
            return True
    return False


def draw_check(board):
    # For X and 0 check absence of possibility to fill diagonal, horizontal or vertical. If True -> draw.
    if sum(1 for i in range(3) for j in range(3) if board[i][j] == ' ') == 0:
        return True
    for symb in ['0', 'X']:
        if sum(1 for i in range(3) if board[i][i] == symb or board[i][i] == ' ') == 3 \
                or sum(1 for i in range(3) if board[i][2-i] == symb or board[i][2-i] == ' ') == 3:
            return False
        for i in range(3):
            if sum(1 for j in range(3) if board[i][j] == symb or board[i][j] == ' ') == 3:
                return False
        for j in range(3):
            if sum(1 for i in range(3) if board[i][j] == symb or board[i][j] == ' ') == 3:
                return False
    return True


def comp_turn(player, comp, board, i_last, j_last):
    # Calculate comp turn, return board state
    if board[1][1] == ' ':     # if center is empty take it immediately
        board[1][1] = comp
        return board
    # if the player's first step is at the center -> take any corner
    if board == [[' ', ' ', ' '], [' ', player, ' '], [' ', ' ', ' ']]:
        i, j = [random.randint(0, 1)*2 for _ in [0, 1]]
        board[i][j] = comp
        return board
    # X-comp center, 0-player any -> X-comp further corner
    if sum(1 for i in range(3) for j in range(3) if board[i][j] == player) == 1:
        d_comp = {0: 2, 1: random.randint(0, 1) * 2, 2: 0}
        i, j = d_comp[i_last], d_comp[j_last]
        board[i][j] = comp
        return board
    # if comp is going to win at the next turn -> fill immediately winning diagonal, horizontal or vertical
    if sum(1 for i in range(3) if board[i][i] == comp) == 2:
        for i in range(3):
            if board[i][i] == ' ':
                board[i][i] = comp
                return board
    if sum(1 for i in range(3) if board[i][2 - i] == comp) == 2:
        for i in range(3):
            if board[i][2 - i] == ' ':
                board[i][2 - i] = comp
                return board
    for i in range(3):
        if sum(1 for j in range(3) if board[i][j] == comp) == 2:
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = comp
                    return board
    for j in range(3):
        if sum(1 for i in range(3) if board[i][j] == comp) == 2:
            for i in range(3):
                if board[i][j] == ' ':
                    board[i][j] = comp
                    return board
    # if player is going to win at the next turn -> interrupt his diagonal, horizontal or vertical
    if sum(1 for i in range(3) if board[i][i] == player) == 2:
        for i in range(3):
            if board[i][i] == ' ':
                board[i][i] = comp
                return board
    if sum(1 for i in range(3) if board[i][2 - i] == player) == 2:
        for i in range(3):
            if board[i][2 - i] == ' ':
                board[i][2 - i] = comp
                return board
    for i in range(3):
        if sum(1 for j in range(3) if board[i][j] == player) == 2:
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = comp
                    return board
    for j in range(3):
        if sum(1 for i in range(3) if board[i][j] == player) == 2:
            for i in range(3):
                if board[i][j] == ' ':
                    board[i][j] = comp
                    return board
    # 0-comp 2nd step
    if player == 'X' and sum(1 for i in range(3) for j in range(3) if board[i][j] == comp) == 1:
        pmap = [(i, j) for i in range(3) for j in range(3) if board[i][j] == player and (i, j) != (1, 1)]
        # if X-player at center and corner -> 0-comp any near corner
        if len(pmap) == 1:
            if pmap[0][0] == pmap[0][1]:
                i = random.randint(0, 1)*2
                j = 2 - i
                board[i][j] = comp
                return board
            elif pmap[0][0] == 2 - pmap[0][1]:
                i = random.randint(0, 1) * 2
                j = i
                board[i][j] = comp
                return board
        if len(pmap) == 2:
            # if X-player at diagonal corners -> 0-comp any side
            if pmap == [(0, 0), (2, 2)] or pmap == [(0, 2), (2, 0)]:
                k = random.randint(0, 3)
                i, j = [(0, 1), (1, 0), (1, 2), (2, 1)][k]
                board[i][j] = comp
                return board
            # if X-player at opposite sides -> 0-comp any corner
            if pmap == [(0, 1), (2, 1)] or pmap == [(1, 0), (1, 2)]:
                i, j = [random.randint(0, 1)*2 for _ in [0, 1]]
                board[i][j] = comp
                return board
            # if X-player at near sides -> 0-comp corner between them
            if pmap[0] in [(0, 1), (1, 0), (1, 2), (2, 1)] and pmap[1] in [(0, 1), (1, 0), (1, 2), (2, 1)]:
                i = sum(pmap[k][0] for k in [0, 1] if pmap[k][0] != 1)
                j = sum(pmap[k][1] for k in [0, 1] if pmap[k][1] != 1)
                board[i][j] = comp
                return board
            # if X-player at corner and far side -> 0-comp diagonal corner
            for k in [0, 1]:
                if pmap[k] in [(0, 0), (0, 2), (2, 0), (2, 2)]:
                    i, j = 2 - pmap[k][0], 2 - pmap[k][1]
                    board[i][j] = comp
                    return board
    # X-comp 3rd step: X-comp at center and corner, 0-player at near corner and diagonal -> X-comp at far corner
    if player == '0':
        pmap = [(i, j) for i in range(3) for j in range(3) if board[i][j] == player]
        if len(pmap) == 2:
            for k in [0, 1]:
                if pmap[1 - k][0] == 1:
                    i, j = 2 - pmap[k][0], pmap[k][1]
                    board[i][j] = comp
                    return board
                elif pmap[1 - k][1] == 1:
                    i, j = pmap[k][0], 2 - pmap[k][1]
                    board[i][j] = comp
                    return board
    # if free cells <= 4 take any cell
    fmap = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    if len(fmap) <= 4:
        (i, j) = fmap[random.randint(0, len(fmap) - 1)]
        board[i][j] = comp
        return board


def game_result(res, *args):
    # Print results
    args = list(args)                          # takes number of games, wins, losts
    args.append(args[2])
    args[2] = args[0] - args[1] - args[3]      # add number of draws
    upper_border()
    print(f'{lb}{" " * int((lgm - len(res))/2)}{res}{" " * int((lgm - len(res))/2)}{rb}')
    for i in range(len(rst)):
        print(f'{lb}{" " * int((lgm - lrst[i]-3)/2)}{rst[i]}{args[i]:3d}{" " * int((lgm - lrst[i]-3)/2)}{rb}')
    lower_border()


def exit_():
    # Print exit menu
    upper_border()
    for i in range(len(ext)):
        print(f'{lb}{" " * int((lgm - lext[i])/2)}{ext[i]}{" " * int((lgm - lext[i])/2)}{rb}')
    lower_border()


greeting()
while True:
    wtd_res = what_to_do()
    if wtd_res == '1' or wtd_res == '2':
        if wtd_res == '2' or not xo:
            xo = xo_choice()
        result = game_start(xo)
        game_played += 1
        if result == 'YOU WIN !!!':
            game_win += 1
        elif result == 'Lost this time...':
            game_lost += 1
        input('Enter to continue >>>>>')
        print(' ')
        game_result(result, game_played, game_win, game_lost)
        input('Enter to continue >>>>>')
        print(' ')
        if game_played == 999:
            print("That's enough!")
            exit_()
            break
    elif wtd_res == '9':
        exit_()
        break
    else:
        print('\nUps! This is not your option!')
        continue
