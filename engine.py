# Движок нерасширяемый, захардкожен под 3x3
import random


def counter_line(sym_choice, computer_choice, line):
    counter_sym = 0
    counter_computer = 0
    for i in line:
        if i == sym_choice:
            counter_sym += 1
        elif i == computer_choice:
            counter_computer += 1
    return counter_sym, counter_computer


def max_in_line(line, sym_choice, computer_choice, size):
    counter_sym, counter_computer = counter_line(sym_choice, computer_choice, line)
    if counter_computer == size - 1 and counter_sym == 0:
        return set_sym(line, computer_choice)
    return line, False


def set_sym(line, computer_choice):
    for i in range(len(line)):
        if line[i] == "-":
            line[i] = computer_choice
            return line, True
    return line, False


def dangerous(line, sym_choice, computer_choice, size):
    counter_sym, counter_computer = counter_line(sym_choice, computer_choice, line)
    if counter_sym == size - 1 and counter_computer == 0:
        return set_sym(line, computer_choice)
    return line, False


def line_gen(field, fun, sym_choice, computer_choice, size):
    diag1 = list()
    diag2 = list()
    for i in range(size):
        diag1.append(field[i][i])
        diag2.append(field[i][size - i - 1])
        buf_line, changed = fun([field[i][j] for j in range(size)], sym_choice, computer_choice)
        if changed:
            for j in range(size):
                field[i][j] = buf_line[j]
            return True
        buf_line, changed = fun([field[j][i] for j in range(size)], sym_choice, computer_choice)
        if changed:
            for j in range(size):
                field[j][i] = buf_line[j]
            return True
    buf_line, changed = fun(diag1, sym_choice, computer_choice)
    if changed:
        for i in range(size):
            field[i][i] = buf_line[i]
        return True
    buf_line, changed = fun(diag2, sym_choice, computer_choice)
    if changed:
        for i in range(size):
            field[i][size - i - 1] = buf_line[i]
        return True
    return False


def stupid_mode(field, sym_choice, computer_choice, size):
    if line_gen(field, max_in_line, sym_choice, computer_choice, size):
        return
    if line_gen(field, dangerous, sym_choice, computer_choice, size):
        return

    for i in range(size):
        for j in range(size):
            if field[i][j] not in (sym_choice, computer_choice):
                field[i][j] = computer_choice
                return


def set_corner(field, sym_choice, computer_choice, size):
    for i in range(0, size, size - 1):
        for j in range(0, size, size - 1):
            if field[i][j] not in (sym_choice, computer_choice):
                field[i][j] = computer_choice
                return


def set_side(field, sym_choice, computer_choice, size):
    for i in range(size):
        for j in range(size):
            if (i or j not in [0, size - 1]) and field[i][j] != sym_choice:
                field[i][j] = computer_choice
                return


def pair(field, sym_choice):  # Защита от грубой атаки крестиков на 3 ходу
    if field[0][2] == sym_choice and field[2][0] == sym_choice \
            or field[0][0] == sym_choice and field[2][2] == sym_choice:
        return True
    return False


def cross(field, sym_choice):  # Тупая защита от тупой атаки ноликов на 3 ходу
    if field[1][0] == sym_choice and field[0][1] == sym_choice:
        return True
    return False


def engine(field, step, sym_choice, size):
    computer_choice = "X" if sym_choice == "O" else "O"
    if step == 0:
        if computer_choice == "X":
            if random.randint(0, 1) == 1:
                field[1][1] = computer_choice
            else:
                set_corner(field, sym_choice, computer_choice, size)
        else:
            if field[1][1] == sym_choice:
                set_corner(field, sym_choice, computer_choice, size)
            else:
                field[1][1] = computer_choice

    elif step in [1, 2]:
        if line_gen(field, dangerous, sym_choice, computer_choice, size):
            return
        elif line_gen(field, max_in_line, sym_choice, computer_choice, size):
            return
        elif not pair(field, sym_choice) and not cross(field, sym_choice):
            set_corner(field, sym_choice, computer_choice, size)
        else:
            set_side(field, sym_choice, computer_choice, size)
    else:
        stupid_mode(field, sym_choice, computer_choice, size)
