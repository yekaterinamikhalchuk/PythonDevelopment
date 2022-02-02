def main():
    global full_field
    global first_player
    global result_who_win
    global field_x0
    print('Welcome to TicTacToe!')
    field_x0 = [['-' for j in range(3)] for i in range(3)]
    field_x0.insert(0, [' ', '0', '1', '2'])
    for i in range(1, len(field_x0)):
        field_x0[i].insert(0, str(i - 1))
    print('\n'.join(map(' '.join, field_x0)))
   
    full_field = False
    result_who_win = False
    check_coord = []
    first_player = str(input('The first player choose x or 0 - '))
    
    while first_player not in ['x', 'X', '0']:
        first_player = str(input('The first player choose x or 0 - '))

    if first_player == 'x' or first_player == 'X':
        print('Enter two coordinates (row, column) separated by a space')
        while (full_field == False) and (result_who_win == False):
            
            coord_x = str(input('Coordinates for X - ')).split()

            if (len(coord_x) != 2) or \
                (coord_x[0] not in [str(i) for i in range(len(field_x0) - 1)]) or \
                (coord_x[1] not in [str(i) for i in range(len(field_x0) - 1)]) or \
                (coord_x in check_coord):
                while (len(coord_x) != 2) or \
                    (coord_x[0] not in [str(i) for i in range(len(field_x0) - 1)]) or \
                    (coord_x[1] not in [str(i) for i in range(len(field_x0) - 1)]) or \
                    (coord_x in check_coord):
                    coord_x = str(input('Wrong move! Coordinates for X - ')).split()
                check_coord.append(coord_x)
            else:
                check_coord.append(coord_x)   

            field(int(coord_x[0]), int(coord_x[1]), 'x')
            who_win(field_x0)
            field_size(field_x0)

            if (full_field == True) or (result_who_win == True):
                break

            coord_0 = str(input('Coordinates for 0 - ')).split()

            if (len(coord_0) != 2) or \
                (coord_0[0] not in [str(i) for i in range(len(field_x0) - 1)]) or \
                (coord_0[1] not in [str(i) for i in range(len(field_x0) - 1)]) or \
                (coord_0 in check_coord):
                while (len(coord_0) != 2) or \
                    (coord_0[0] not in [str(i) for i in range(len(field_x0) - 1)]) or (coord_0[1] not in [str(i) for i in range(len(field_x0) - 1)]) or (coord_0 in check_coord):
                    coord_0 = str(input('Wrong move! Coordinates for 0 - ')).split()
                check_coord.append(coord_0)
            else:
                check_coord.append(coord_0)

            field(int(coord_0[0]), int(coord_0[1]), '0')
            who_win(field_x0)
            field_size(field_x0)
            
    elif first_player == '0':
        print('Enter two coordinates (row, column) separated by a space')
        while (full_field == False) and (result_who_win == False):
            
            coord_0 = str(input('Coordinates for 0 - ')).split()

            if (len(coord_0) != 2) or \
                (coord_0[0] not in [str(i) for i in range(len(field_x0) - 1)]) or \
                (coord_0[1] not in [str(i) for i in range(len(field_x0) - 1)]) or \
                (coord_0 in check_coord):
                while (len(coord_0) != 2) or \
                    (coord_0[0] not in [str(i) for i in range(len(field_x0) - 1)]) or \
                    (coord_0[1] not in [str(i) for i in range(len(field_x0) - 1)]) or \
                    (coord_0 in check_coord):
                    coord_0 = str(input('Wrong move! Coordinates for 0 - ')).split()
                check_coord.append(coord_0)
            else:
                check_coord.append(coord_0)

            field(int(coord_0[0]), int(coord_0[1]), '0')
            who_win(field_x0)
            field_size(field_x0)

            if (full_field == True) or (result_who_win == True):
                break

            coord_x = str(input('Coordinates for X - ')).split()

            if (len(coord_x) != 2) or \
                (coord_x[0] not in [str(i) for i in range(len(field_x0) - 1)]) \
                or (coord_x[1] not in [str(i) for i in range(len(field_x0) - 1)]) \
                or (coord_x in check_coord):
                
                while (len(coord_x) != 2) or \
                    (coord_x[0] not in [str(i) for i in range(len(field_x0) - 1)]) or \
                    (coord_x[1] not in [str(i) for i in range(len(field_x0) - 1)]) or \
                    (coord_x in check_coord):
                    coord_x = str(input('Wrong move! Coordinates for X - ')).split()
                check_coord.append(coord_x)
            
            else:
                check_coord.append(coord_x)

            field(int(coord_x[0]), int(coord_x[1]), 'x')
            who_win(field_x0)
            field_size(field_x0)
    
    if full_field == True:
        print('Draw!')
    
    return restart()

def field(where_x, where_y, what):
    global field_x0
    if what == 0:
        field_x0[where_x + 1][where_y + 1] = str(what)
    else:
        field_x0[where_x + 1][where_y + 1] = str.lower(what)
    print('\n'.join(map(' '.join, field_x0)))

def who_win(field):
    global result_who_win
    global diagonal_1
    diagonal_1 = []
    ind_1 = 0
    diagonal_2 = []
    ind_2 = len(field)
    for i in field:
        if ind_1 != len(field):
            if (ind_1 != 0) and (ind_2 != len(field)):
                diagonal_1.append(i[ind_1])
                diagonal_2.append(i[ind_2])
        ind_1 += 1
        ind_2 -= 1
        if all(i[j]=='x' for j in range(1, len(i))):
            result_who_win = True
            print('Player x won')
        if all(i[j]=='0' for j in range(1, len(i))):
            result_who_win = True
            print('Player 0 won')
    for q in range(len(field) - 1):
        if all(w[q]=='x' for w in field):
            result_who_win = True
            print('Player x won')
        if all(w[q]=='0' for w in field):
            result_who_win = True
            print('Player 0 won')
    
    if all(i=='x' for i in diagonal_1) and (len(diagonal_1) == len(field) - 1):
        result_who_win = True
        print('Player x won')
    elif all(i=='0' for i in diagonal_1) and (len(diagonal_1) == len(field) - 1):
        result_who_win = True
        print('Player 0 won')
    
    if all(i=='x' for i in diagonal_2) and (len(diagonal_2) == len(field) - 1):
        result_who_win = True
        print('Player x won')
    elif all(i=='0' for i in diagonal_2) and (len(diagonal_2) == len(field) - 1):
        result_who_win = True
        print('Player 0 won')

def field_size(field):
    global full_field
    count_j = 0
    for i in field:
        for j in i:
            if j=='-':
                count_j += 1
    if count_j == 0:
        full_field = True

def restart():
    rest = str(input('Do we want to play again? Choose Y or N: ')) 
    if rest == 'Y':
        return main()
    return 'Thanks for the game!'

###GAME
main()