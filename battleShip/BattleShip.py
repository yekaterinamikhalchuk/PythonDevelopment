# field = [['О'] * 6 for i in range(6)]
# print(field)
from random import randint
#класс исключений
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "This cell is out the board"

class BoardBusyException(BoardException):
    def __str__(self):
        return "This cell is busy"

class BoardWrongShipException(BoardException):
    pass




#класс точек на поле
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        rep = f'Dot({self.x}, {self.y})'
        return rep

class Ship:
    def __init__(self,  dot, length, direction):
        self.length = length
        self.dot = dot # точка, где размещен нос корабля
        self.direction = direction
        self.lives = length # сколько кораблей еще не подбито

    @property
    def dots(self):
        dots_list = []
        for i in range(self.length):
            x_dot = self.dot.x
            y_dot = self.dot.y

            if self.direction == 0:
                y_dot += i
            elif self.direction == 1:
                x_dot += i
            dots_list.append(Dot(x_dot, y_dot))

        return dots_list

    def shot_check(self, shot):
        return shot in self.dots



class Board:
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size
        self.ships = [] # список кораблей доски
        self.field = [['O'] * size for i in range(size)]
        self.busy_cell = []
        self.count = 0

    def __str__(self):
        res = ""
        res += '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.field):
            res += f'\n{i + 1} | {" | ".join(row)} |'
        if self.hid:
            res = res.replace("■", "0")
        return res

    def out(self, cell):
        return not ((0 <= cell.x < self.size) & (0 <= cell.y < self.size))

    def add_ship(self, ship):
        for cell in ship.dots:
            if cell in self.busy_cell or self.out(cell):
                raise BoardWrongShipException()

        for cell in ship.dots:
            self.field[cell.x][cell.y] = "■"
            self.busy_cell.append(cell)
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, 1), (0, 1), (1, 1),
            (-1, 0), (0, 0), (1, 0),
            (-1, -1), (0, -1), (1, -1)
        ]
        for cell in ship.dots:
            for dx, dy in near:
                cur = Dot(cell.x + dx, cell.y + dy)
                if not(self.out(cur)) and cur not in self.busy_cell:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy_cell.append(cur)

    def shot(self, cell):
        if self.out(cell):
            raise BoardOutException()
        if cell in self.busy_cell:
            raise BoardBusyException()
        self.busy_cell.append(cell)

        for ship in self.ships:
            if cell in ship.dots:
                ship.lives -= 1
                self.field[cell.x][cell.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Hit! The ship is destroyed')
                    return False
                else:
                    print('Hit! The ship is damaged')
                    return True
        self.field[cell.x][cell.y] = "."
        print('Miss!')
        return False

    def begin(self):
        self.busy_cell = []

    def defeat(self):
        return self.count == len(self.ships)


class Player:
    def __init__(self, board_own, board_competitor):
        self.board_own = board_own
        self.board_competitor = board_competitor


    def ask(self):
        raise NotImplementedError

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.board_competitor.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):

    def ask(self):
        cell = Dot(randint(0, 5), randint(0, 5))
        print(f"The AI's move: {cell.x + 1}, {cell.y + 1}")
        return cell

class User(Player):

    def ask(self):
        while True:
            coordinates = input("Your move:").split()
            if len(coordinates) != 2:
                print("INVALID FORMAT!")
                print("Valid input format: number from 0 to 2")
                continue
            x, y = coordinates
            if not (x.isdigit()) or not (y.isdigit()):
                print("INVALID FORMAT!")
                print("Valid input format: number from 0 to 2")
                continue
            x, y = int(x), int(y)
            #print(f"The Player's move: {x}, {y}")
            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size = 6):
        self.size = size
        user_board = self.random_board()
        computer_board = self.random_board()
        computer_board.hid = True
        self.computer = AI(computer_board, user_board)
        self.user = User(user_board, computer_board)

    def board_initial(self):
        length_ships = [1, 1, 1, 1, 2, 2, 3]
        board = Board(size=self.size)
        attempts = 0
        for i in length_ships:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), i, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.board_initial()
        return board

    def loop(self):
        num = 0
        while True:
            print("-" * 30)
            print("User's board")
            print(self.user.board_own)
            print("-" * 30)
            print("Computer's board")
            print(self.computer.board_own)
            print("-" * 30)
            if num % 2 == 0:
                print("User's turn")
                repeat = self.user.move()
            else:
                print("Computer's turn")
                repeat = self.computer.move()
            if repeat:
                num -= 1

            if self.computer.board_own.defeat():
                print("-" * 30)
                print("User won!")
                print("-" * 30)
                break
            if self.user.board_own.defeat():
                print("-" * 30)
                print("Computer won!")
                print("-" * 30)
                break
            num += 1
    def greet(self):
        print("-" * 30)
        print("Welcome to BattleShip!")
        print("The game is starting!")
        print("-" * 30)
        print("Input available (separated by space):")
        print("x - string number")
        print("y - column number")
        print("-" * 30)
        print("   Good luck!")
        print("-" * 30)

    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()








