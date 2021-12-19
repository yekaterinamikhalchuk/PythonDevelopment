field = [[' '] * 3 for i in range(3)]

def starting():
    print('------------------------------')
    print("WELCOME TO TicTacToe GAME!")
    print("THE GAME STARTS!")
    print('------------------------------')
def show_field(field):
    print('  | 0 | 1 | 2 |')
    for i, row in enumerate(field):
        row_string = f'{i} | {" | ".join(row)} |'
        print('---------------')
        print(row_string)



def input_coordinates():
    print("Getting the coordinates for input")
    while True:
        row = input("----Enter the string number please:")
        column = input("----Enter the column number please:")

        if not (row.isdigit()) or not (column.isdigit()):
            print("         INVALID FORMAT!")
            print("         Valid input format: number from 0 to 2")
            continue

        if int(column) > 2 \
                or int(column) < 0 \
                or int(row) > 2 \
                or int(row) < 0 \
                or len(row) != 1 \
                or len(column) != 1:
            print("             THIS NUMBER DOES NOT EXIST!")
            print("         Valid input format: number from 0 to 2")
            continue
        column = int(column)
        row = int(row)
        if field[row][column] != ' ':
            print("THE CELL IS BUSY, repeat your move please!")
            continue
        print("----YOU HAVE CHOSEN:", row, column)
        return row, column

def check_win(field):
    win_coordinates = (
        ((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),
        ((0, 0), (1, 1), (2, 2)), ((2, 0), (1, 1), (0, 2))
    )
    for coordinate in win_coordinates:

        if (field[coordinate[0][0]][coordinate[0][1]] ==
            field[coordinate[1][0]][coordinate[1][1]] ==
            field[coordinate[2][0]][coordinate[2][1]]) & ((field[coordinate[2][0]][coordinate[2][1]] != ' ') &
        (field[coordinate[1][0]][coordinate[1][1]] != ' ') & (field[coordinate[0][0]][coordinate[0][1]] != ' ')):
            print('----------------------')
            print('--CONGRATULATIONS!!!--')
            print("--THE PLAYER", field[coordinate[0][0]][coordinate[0][1]], 'WON ---')
            print('----------------------')
            win = True
            return win
        else:
            win = False
    return win

def restart():
    rest = str(input('Do you want to play again? YES or NO'))
    if rest == 'YES':
        global field
        field = [[' '] * 3 for i in range(3)]
        return main(field)
    else:
        print('---THANKS FOR THE GAME!---')

def main(field):
    starting()
    count = 0
    win = check_win(field)
    while not win:
        show_field(field)
        count += 1
        if count % 2 == 0:
            print("Player X, it is your turn")
        else:
            print("Player 0, it is your turn")

        row, column = input_coordinates()

        if count % 2 == 0:
            field[row][column] = 'X'

        else:
            field[row][column] = 'O'



        check = check_win(field)

        if check:
            show_field(field)
            break

        if (count >= 9) & (' ' not in field[0]) & (' ' not in field[1]) & (' ' not in field[2]):
            print("THE GAME IS OVER! THE DRAW!")
            break
    restart()
main(field)



