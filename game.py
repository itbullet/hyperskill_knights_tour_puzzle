import math


class Knight:
    # sp for a starting position, cp for a current position
    def __init__(self):
        self.cp = []


def check_coordinates(coordinates_, dimensions_):
    for el in coordinates_:
        if not el.isdigit():
            return False
    if len(coordinates_) != 2:
        return False
    elif int(coordinates_[0]) > dimensions_[0] or int(coordinates_[0]) < 1 \
            or int(coordinates_[1]) > dimensions_[1] or int(coordinates_[1]) < 1:
        return False
    return True


def check_dimensions(dimensions_):
    for el in dimensions_:
        if not el.isdigit() or int(el) < 1:
            return False
    if len(dimensions_) != 2:
        return False
    return True


def check_moves(coordinates_, dimensions_, old_mv_):
    possible_moves_ = []
    for row_ in range(dimensions_[1], 0, -1):
        for col_ in range(1, dimensions_[0] + 1):
            if col_ == coordinates_[0] - 1 and row_ == coordinates_[1] + 2 and [col_, row_] not in old_mv_:
                possible_moves_.append([col_, row_])
            elif col_ == coordinates_[0] + 1 and row_ == coordinates_[1] + 2 and [col_, row_] not in old_mv_:
                possible_moves_.append([col_, row_])
            elif col_ == coordinates_[0] + 2 and row_ == coordinates_[1] + 1 and [col_, row_] not in old_mv_:
                possible_moves_.append([col_, row_])
            elif col_ == coordinates_[0] + 2 and row_ == coordinates_[1] - 1 and [col_, row_] not in old_mv_:
                possible_moves_.append([col_, row_])
            elif col_ == coordinates_[0] + 1 and row_ == coordinates_[1] - 2 and [col_, row_] not in old_mv_:
                possible_moves_.append([col_, row_])
            elif col_ == coordinates_[0] - 1 and row_ == coordinates_[1] - 2 and [col_, row_] not in old_mv_:
                possible_moves_.append([col_, row_])
            elif col_ == coordinates_[0] - 2 and row_ == coordinates_[1] - 1 and [col_, row_] not in old_mv_:
                possible_moves_.append([col_, row_])
            elif col_ == coordinates_[0] - 2 and row_ == coordinates_[1] + 1 and [col_, row_] not in old_mv_:
                possible_moves_.append([col_, row_])
    return possible_moves_


def check_knight_coordinates(row_, col_, coordinates_, underscore_size_, possible_moves_, board_dimensions_, old_mv_=[], draw=0):
    empty_cell = f" {underscore_size_ * '_'}"
    knight_cell = f" {(underscore_size_ - 1) * ' '}X"
    old_move_cell = ''
    if draw == 0:
        old_move_cell = f" {(underscore_size_ - 1) * ' '}*"
    elif draw == 1:
        move_no = old_mv_.index([col_, row_]) + 1
        len_move_no = count_digit(move_no)
        old_move_cell = f" {(underscore_size_ - len_move_no) * ' '}{move_no}"
    if row_ == coordinates_[1] and col_ == coordinates_[0] and [col_, row_] not in old_mv_:
        return knight_cell
    elif [col_, row_] in possible_moves_:
        possible_moves_count = len(check_moves([col_, row_], board_dimensions_, old_mv_)) - 1
        move_cell = f" {(underscore_size_ - 1) * ' '}{possible_moves_count}"
        return move_cell
    elif [col_, row_] in old_mv_:
        return old_move_cell
    else:
        return empty_cell


def count_digit(num):
    # recursive solution
    # if num//10 == 0:
    #     return 1
    # return 1 + count_digit(num // 10)
    return math.floor(math.log10(num)+1)


def draw_border(column_n, cell_size, left_shift):
    return f"{left_shift * ' '}{(column_n * (cell_size + 1) + 3) * '-'}"


def draw_bottom_numbers(column_n, cell_size, left_shift):
    numbers = ""
    left_shift = f"{(left_shift + 1) * ' '}"
    for i in range(1, column_n + 1):
        numbers += f" {(cell_size - count_digit(i)) * ' '}{i}"
    return f"{left_shift}{numbers}"


def draw_board(coordinates_, dimensions_, old_moves_=[], draw=0):
    # status 0 - continue, 1 - end (win/lost)
    status = 0
    possible_moves = check_moves(coordinates_, dimensions_, old_moves_)
    chessboard_max_number = dimensions_[0] * dimensions_[1]
    underscore_size = count_digit(chessboard_max_number)
    left_shift_size = count_digit(dimensions_[1])
    for i in range(dimensions_[1], 0, -1):
        for j in range(1, dimensions_[0] + 1):
            if i == dimensions_[1] and j == 1:
                print(draw_border(dimensions_[0], underscore_size, left_shift_size))
            if j == 1 and j == dimensions_[0]:
                print(f"{(left_shift_size - count_digit(i)) * ' '}{i}|", end="")
                print(check_knight_coordinates(i, j, coordinates_, underscore_size, possible_moves, dimensions_, old_moves_, draw), end="")
                print(f" |")
            elif j == 1:
                print(f"{(left_shift_size - count_digit(i)) * ' '}{i}|", end="")
                print(check_knight_coordinates(i, j, coordinates_, underscore_size, possible_moves, dimensions_, old_moves_, draw), end="")
            elif j == dimensions_[0]:
                print(check_knight_coordinates(i, j, coordinates_, underscore_size, possible_moves, dimensions_, old_moves_, draw), end="")
                print(f" |")
            else:
                print(check_knight_coordinates(i, j, coordinates_, underscore_size, possible_moves, dimensions_, old_moves_, draw), end="")

            if i == 1 and j == dimensions_[0]:
                print(draw_border(dimensions_[0], underscore_size, left_shift_size))
                print(draw_bottom_numbers(dimensions_[0], underscore_size, left_shift_size))
    if len(old_moves_) == dimensions_[0] * dimensions_[1] - 1:
        print('What a great tour! Congratulations!')
        status = 1
    elif len(old_moves_) != dimensions_[0] * dimensions_[1] - 1 and len(possible_moves) == 0 and draw == 0:
        print('No more possible moves!')
        print(f'Your knight visited {len(old_moves_) + 1} squares!')
        status = 1
    return possible_moves, status


def check_solution(dimensions_, coordinates_, old_moves_, knight_position, draw=1):
    chessboard_max_number = dimensions_[0] * dimensions_[1]
    old_moves_.append(coordinates_)
    i = 2
    while True:
        possible_moves = check_moves(coordinates_, dimensions_, old_moves_)
        temp_possible_moves_dict = dict()
        for move in possible_moves:
            temp_possible_moves_dict[len(check_moves(move, dimensions_, old_moves_))] = move
        min_count_possible_move = min(temp_possible_moves_dict.keys())
        next_move = temp_possible_moves_dict[min(temp_possible_moves_dict.keys())]
        old_moves_.append(next_move)
        if min_count_possible_move != 0 and i <= chessboard_max_number:
            coordinates_ = next_move
            i += 1
        elif min_count_possible_move == 0 and i < chessboard_max_number:
            print('No solution exists!')
            return False
        elif draw == 1:
            print("\nHere's the solution!")
            draw_board(knight_position, dimensions_, old_moves_, draw=1)
            return True
        elif draw == 0:
            return True


def game():
    old_moves = []
    while True:
        dimensions = input("Enter your board dimensions: ").lower().split()
        if not check_dimensions(dimensions):
            print("Invalid dimensions!")
        else:
            break

    # converting of str list of board dimension to int using map
    dimensions = list(map(int, dimensions))
    while True:
        coordinates = input("Enter the knight's starting position: ").lower().split()
        if not check_coordinates(coordinates, dimensions):
            print('Invalid position!')
        else:
            break
    while True:
        answer = input('Do you want to try the puzzle? (y/n): ').lower()
        if answer not in ['y', 'n']:
            print('Invalid input!')
        else:
            break
    knight = Knight()
    # converting of str list of knight position to int using list comprehension
    coordinates = [int(el) for el in coordinates]
    knight.cp = coordinates
    if answer == 'y':
        if check_solution(dimensions, coordinates, old_moves, knight.cp, draw=0):
            old_moves = []
            possible_moves, status = draw_board(knight.cp, dimensions)
            while True:
                next_move = input("Enter your next move: ").lower().split()
                if not check_coordinates(next_move, dimensions):
                    print('Invalid move!', end='')
                else:
                    next_move = list(map(int, next_move))
                    if next_move not in possible_moves:
                        print('Invalid move!', end='')
                    else:
                        old_moves.append(knight.cp)
                        knight.cp = next_move
                        possible_moves, status = draw_board(knight.cp, dimensions, old_moves)
                        if status == 1:
                            break
    elif answer == 'n':
        check_solution(dimensions, coordinates, old_moves, knight.cp)


def main():
    game()


if __name__ == '__main__':
    main()
