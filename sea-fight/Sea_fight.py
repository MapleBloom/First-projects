from random import randint


class BoardOutException(Exception):
    pass


class DoubleShot(Exception):
    pass


class ShipIsNotPossible(Exception):
    pass


class Dot:
    def __init__(self, x: int = 0, y: int = 0):
        Dot.verify_coord(x)
        Dot.verify_coord(y)
        self._x = x
        self._y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @classmethod
    def verify_coord(cls, x):
        if type(x) != int or x < 0 or x > 5:
            raise BoardOutException("Dot coordinates should be integers in [1, 6] !")

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        Dot.verify_coord(x)
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        Dot.verify_coord(y)
        self._y = y

    @property
    def coord(self):
        return self.x, self.y

    def set_coord(self, x, y):
        Dot.verify_coord(x)
        Dot.verify_coord(y)
        self._x = x
        self._y = y


class Ship:
    def __init__(self, length: int, x: int, y: int, direction: str):
        # length - number of dots of the ship
        # x, y - coordinates of the upper-left dot
        # direction: 'h' - horizontal, 'v' - vertical
        Ship.verify_length(length)
        Ship.verify_coord(x)
        Ship.verify_coord(y)
        Ship.verify_direction(direction)
        self._length = length
        self._x = x
        self._y = y
        self._direction = direction
        self.lives = length

    @classmethod
    def verify_length(cls, length):
        if length not in [1, 2, 3]:
            raise TypeError(f"Ship length {length} should be integer in [1, 3] !")

    @classmethod
    def verify_coord(cls, x):
        if type(x) != int or x < 0 or x > 5:
            raise TypeError("Coordinates should be integers in [1, 6] !")

    @classmethod
    def verify_direction(cls, direction):
        if direction != 'h' and direction != 'v':
            raise TypeError("Ship direction should be 'h' horizontal or 'v' vertical !")

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        Ship.verify_length(length)
        self._length = length

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        Ship.verify_coord(x)
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        Ship.verify_coord(y)
        self._y = y

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        Ship.verify_direction(direction)
        self._direction = direction

    @property
    def dots(self) -> list[tuple]:
        # Return list of coordinates of all dots of the ship
        return [(self.x, self.y + _) for _ in range(self.length)] if self.direction == 'h' \
            else [(self.x + _, self.y) for _ in range(self.length)]

    @property
    def contour(self) -> list[tuple]:
        # Return list of coordinates of all dots around the ship
        if self._direction == 'h':
            cont = [(i, self.y + j) for i in (self.x - 1, self.x + 1) if 0 <= i <= 5
                    for j in range(-1, self.length + 1) if 0 <= self.y + j <= 5] \
                 + [(self.x, j) for j in (self.y - 1, self.y + self.length) if 0 <= j <= 5]
        else:
            cont = [(self.x + i, j) for i in range(-1, self.length + 1) if 0 <= self.x + i <= 5
                    for j in (self.y - 1, self.y + 1) if 0 <= j <= 5] \
                 + [(i, self.y) for i in (self.x - 1, self.x + self.length) if 0 <= i <= 5]
        return cont


class Board:
    def __init__(self, player: str, game_board: list[list[tuple]] = None,
                 ships: list[Ship] = None, ships_alive: int = 0):
        # Player - 'AI' for AI, 'US' or two upper-symbols of user choice for user
        # game_board - matrix 6x6 with current state of the board dots (' ', '■', 'X', '*', 'o')
        # list of the board ships, fills by Game.random_board
        # ships_alive - keeps number of ships that have at least one dot alive
        self.player = player
        self.game_board = game_board if game_board else [[' ' for _ in range(6)] for _ in range(6)]
        self.hid = True if self.player == 'AI' else False  # to print AI board with ships hidden
        self.ships = ships if ships else []
        self.ships_alive = ships_alive
        self.board_print = [[' ' if self.hid and self.game_board[i][j] == chr(9632)   # print-form
                            else self.game_board[i][j] for j in range(6)] for i in range(6)]
        self.shoots = []  # list of shoots that needn't be repeated: misses, ships revealed and their contour

    def print_board(self) -> None:
        # Print current board with player's call sign and ships alive
        print(f" {self.player}{' '*2}" + "".join(f"{i + 1}{' ' * 3}" for i in range(6)))
        print(f"{' '*3}{'_'*25}")
        for i in range(6):
            print(f" {i + 1} | " + "".join(f"{self.board_print[i][j]} | " for j in range(6)))
            print(f"{' ' * 3}{'_' * 25}")
        print(f" {self.player} ships alive: {self.ships_alive}")
        print()

    def add_ship(self, ship: Ship) -> None:
        # Add new ship info to all board params
        self.ships.append(ship)
        self.ships_alive += 1
        for i in range(len(ship.dots)):
            self.game_board[ship.dots[i][0]][ship.dots[i][1]] = chr(9632)
        if not self.hid:
            for i in range(len(ship.dots)):
                self.board_print[ship.dots[i][0]][ship.dots[i][1]] = chr(9632)


class Player:
    def __init__(self, board: Board):
        self.board = board

    def ask(self):
        # Defined in subclasses
        pass

    def move(self, i, j, player, turn) -> int:
        # Add shot info to all board params, check shot result
        # Return 0 or 1 depending on the next turn: 0 - user, 1 - AI
        # Return -1 when somebody wins (the opponent board ships_alive = 0)
        self.board.shoots.append((i, j))                # mark the cell as checked
        if self.board.game_board[i][j] == ' ':          # miss shot processing
            self.board.game_board[i][j] = '*'
            self.board.board_print[i][j] = '*'
            print(f"   {player} shot: Miss!")
        elif self.board.game_board[i][j] == chr(9632):  # good shot processing
            self.board.game_board[i][j] = 'X'
            self.board.board_print[i][j] = 'X'
            for ship in self.board.ships:
                if (i, j) in ship.dots:
                    turn = Game.turns(turn)            # left turn to the current player
                    ship.lives -= 1
                    if ship.lives == 0:                              # if ship is killed
                        self.board.ships_alive -= 1
                        for (x, y) in ship.contour:                  # add ship contour to the board
                            if self.board.game_board[x][y] == ' ':
                                self.board.game_board[x][y] = 'o'
                            if self.board.board_print[x][y] == ' ':
                                self.board.board_print[x][y] = 'o'
                            if (x, y) not in self.board.shoots:      # and mark contour cells as checked
                                self.board.shoots.append((x, y))
                        print(f"   {player} shot: Killed!")
                    else:
                        print(f"   {player} shot: Hurt!")            # if ship is just hurt
        self.board.print_board()
        if self.board.ships_alive == 0:                              # check whether somebody has won
            print(f"{player} win !!!\n")
            return -1
        _ = input(">>>>>\n")
        return turn


class User(Player):
    def __init__(self, board: Board):
        Player.__init__(self, board)

    def ask(self) -> tuple[int, int]:
        # Print AI board, ask to make turn and catch errors of input (ValueError, DoubleShot)
        # Return the user's shot coordinates
        self.board.print_board()
        while True:
            try:
                x = int(input("Make your shoot x-coord: ")) - 1
                y = int(input("Make your shoot y-coord: ")) - 1
                dot = Dot(x, y)
                if (dot.x, dot.y) in self.board.shoots:
                    raise DoubleShot
                print()
                return dot.x, dot.y
            except ValueError:
                print("Your shoot coordinates should be integers in [1, 6] !\n")
            except BoardOutException:
                print("Your shoot coordinates should be integers in [1, 6] !\n")
            except DoubleShot:
                print("You've already checked this quadrant. Try other shot.\n")


class AI(Player):
    def __init__(self, board: Board):
        Player.__init__(self, board)

    def ask(self) -> tuple[int, int]:
        # Make random x and y coordinates and catch DoubleShot error
        # Return AI shot coordinates
        while True:
            try:
                dot = Dot(randint(0, 5), randint(0, 5))
                if (dot.x, dot.y) in self.board.shoots:
                    raise DoubleShot
                return dot.x, dot.y
            except DoubleShot:
                pass


class Game:
    def __init__(self):
        # Init two players with the opposite board as param
        self.player = [User(Board('AI')), AI(Board('User'))]

    def start(self) -> None:
        # game start and finish
        for p in [0, 1]:
            Game.random_board(self.player[p].board)   # fill both boards
        self.player[1].board.player = Game.greet()    # customise user's call sign
        print("Your fleet:\n")
        self.player[1].board.print_board()            # show user's board
        print("Now you should reveal 'AI' ships\nbefore it reveals yours.")
        _ = input("Enter if you are ready >>>>>")
        print()
        self.loop()                                   # game body
        print(f"Game over")

    @staticmethod
    def turns(i: int) -> int:
        # Change turn: 0 - user, 1 - ai
        return 1 if i == 0 else 0

    def loop(self) -> None:
        # game body
        turn = 1
        while turn != -1:
            turn = Game.turns(turn)           # pass turn. Goes before ask-move to catch -1 after
            x, y = self.player[turn].ask()                                             # ask-move
            turn = self.player[turn].move(x, y, self.player[Game.turns(turn)].board.player, turn)

    @staticmethod
    def greet() -> str:
        # Greet and ask user's call sign
        # Return user's call sign (instead of 'User')
        print("\nHello! Let's play SEA FIGHT game!\n")
        player_call = input("Enter your two-symbol call sign: ")[:2].upper()
        if len(player_call) == 1:
            player_call = '0' + player_call
        elif len(player_call) == 0:
            player_call = '00'
        print()
        print(f"Your call sign is '{player_call}'")
        return player_call

    @staticmethod
    def random_board(b: Board) -> None:
        # Fill Board instance with ships by random
        bd = {(i, j) for i in range(6) for j in range(6)}  # all board cells
        while True:
            full = set()  # set to check the cell whether it already ship-dot or contour
            length = 3
            while length >= 1:          # starts with 3-dot ship, then 2-dot and 1-dot
                i = 1
                while i <= 4 - length:  # one 3-dot ship, two 2-dot and three 1-dot
                    fault_count = 0     # if 100 tries are not successful 
                    while True:           # stop tries and start new board
                        try:
                            sh = Ship(length, randint(0, 5), randint(0, 5), 
                                      'h' if randint(0, 1) else 'v')
                            # if some ship-dots are out of board or filled -> ShipIsNotPossible
                            if set(sh.dots).difference(bd) != set() \
                                    or set(sh.dots).intersection(full) != set():
                                raise ShipIsNotPossible
                            full = (full.union(set(sh.dots))).union(set(sh.contour))
                            b.add_ship(sh)
                            i += 1
                            break
                        except ShipIsNotPossible:
                            fault_count += 1
                            if fault_count == 100:
                                i, length = 5, 0    # out of all whiles to external
                                break
                length -= 1
            break


if __name__ == '__main__':
    game = Game()
    game.start()
