from random import randint, randrange

class Dot: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f'Dot({self.x}, {self.y})'

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "This cell is out the board"

class BoardUsedException(BoardException):
    def __str__(self):
        return "This cell is busy"

class BoardWrongShipException(BoardException):
    pass

class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l
    
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i
            
            elif self.o == 1:
                cur_y += i
            
            ship_dots.append(Dot(cur_x, cur_y))
        
        return ship_dots
    
    def shooten(self, shot):
        return shot in self.dots

class Board:

    def __init__(self, hid = False, size = 6):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [ ['O']*size for _ in range(size) ]
        self.busy = []
        self.busy_without_dots = []
        self.ships = []
        self.f_m_p = False
        self.r_m_p = False

    def restart_more_percise(self):
        return self.r_m_p
    
    def for_more_percise(self):
        return self.f_m_p

    def for_busy_w_d(self):
        return self.busy_without_dots    

    def for_busy(self):
        return self.busy
    
    def for_out(self, d):
        return self.out(d)

    def return_board(self):
        res = ''
        res += '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.field):
            res += f'\n{i+1} | ' + ' | '.join(row) + ' |'
        
        if self.hid:
            res = res.replace('■', 'O')
        return res

    def out(self, d):
        return not((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb = False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException
        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            self.busy.append(d)
        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        self.r_m_p = False
        if self.out(d):
            raise BoardOutException
        if d in self.busy:
            raise BoardUsedException
        self.busy.append(d)
        self.busy_without_dots.append(d)
        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = 'X'
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print('Hit! The ship is destroyed!')
                    self.f_m_p = False
                    return False
                else:
                    print('Hit! The ship is damaged!')
                    self.f_m_p = True
                    self.r_m_p = True
                    return True
        self.field[d.x][d.y] = '.'
        self.busy_without_dots.remove(d)
        print('Miss!')
        return False

    def begin(self):
        self.busy = []
    
    def defeat(self):
        return self.count == len(self.ships)

class Player(Board):

    more_percise = Dot(0, 0)

    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError
    
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                if self.enemy.restart_more_percise():
                    self.more_percise = target
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    
    def contour_ai(self, d_ai):
        for_shot_ai_1 = []
        for_shot_ai_2 = []
        near_ai = [
                    (-1, 0), (0, -1), (0, 0), 
                    (0, 1), (1, 0)
                  ]
        count_busy = 0
        for dx, dy in near_ai:
            cur_ai = Dot(d_ai.x + dx, d_ai.y + dy)
            if cur_ai in self.enemy.for_busy_w_d():
                count_busy += 1
                for_shot_ai_2.append(cur_ai)
        if count_busy >= 2:
            for i in range(len(for_shot_ai_2)):
                if for_shot_ai_2[i].x == for_shot_ai_2[i+1].x:
                    sh_x = Dot(for_shot_ai_2[i].x, for_shot_ai_2[i].y + randrange(-1, 2, 2))
                    if not (self.enemy.for_out(sh_x)):
                        for_shot_ai_1.append(sh_x)
                        return for_shot_ai_1
                elif for_shot_ai_2[i].y == for_shot_ai_2[i+1].y:
                    sh_y = Dot(for_shot_ai_2[i].x + randrange(-1, 2, 2), for_shot_ai_2[i].y)
                    if not (self.enemy.for_out(sh_y)):
                        for_shot_ai_1.append(sh_y)
                        return for_shot_ai_1
        for dx, dy in near_ai:
            cur_ai = Dot(d_ai.x + dx, d_ai.y + dy)
            if not (self.enemy.for_out(cur_ai)) and cur_ai not in self.enemy.for_busy():
                for_shot_ai_1.append(cur_ai)
        return for_shot_ai_1
    
    def ask(self):
        if self.enemy.for_more_percise():
            pos_shot_ai = self.contour_ai(self.more_percise)
            random_var = randint(0, len(pos_shot_ai) - 1)
            d = pos_shot_ai[random_var]
        else:
            d = Dot(randint(0,5), randint(0,5))
        print(f"Computer's move: {d.x+1} {d.y+1}")
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input('Your move: ').split()
            if len(cords) != 2:
                print("INVALID FORMAT!")
                print("Valid input format: number from 0 to 2")
                continue
            x,y = cords
            if not(x.isdigit()) or not(y.isdigit()):
                print("INVALID FORMAT!")
                print("Valid input format: number from 0 to 2")
                continue
            x, y = int(x), int(y)
            return Dot(x-1, y-1)

class Game:
    def __init__(self, size = 6, lens = [3, 2, 2, 1, 1, 1, 1]):
        self.lens = lens
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        
        self.ai = AI(co, pl)
        self.us = User(pl, co)
    
    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board
    
    def try_board(self):
        board = Board(size = self.size)
        attempts = 0
        for l in self.lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
                
        board.begin()
        return board

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
    
    def print_boards(self):
        print("-"*57)
        res_us = self.us.board.return_board().split('\n')
        res_us.insert(0, "User's")
        res_us.insert(1, '')
        res_ai = self.ai.board.return_board().split('\n')
        res_ai.insert(0, "Computer's board")
        res_ai.insert(1, '')
        
        for row in range(len(res_us)):
            if row in [0, 1]:
                print('{:^27}{:^30}'.format(res_us[row], res_ai[row]))
            else:
                print('{}{:>30}'.format(res_us[row], res_ai[row]))
        
    def loop(self):
        num = 0
        while True:
            self.print_boards()
            if num % 2 == 0:
                print("-"*57)
                print("User's turn!")
                repeat = self.us.move()
            else:
                print("-"*57)
                print("Computer's turn!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            
            if self.ai.board.defeat():
                self.print_boards()
                print("-"*57)
                print("User won!")
                break
            
            if self.us.board.defeat():
                self.print_boards()
                print("-"*57)
                print("Computer won!")
                break
            num += 1
            
    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()