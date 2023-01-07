import sys
import time

import engine

SIZE = 3


def puzzle_solved(field):
    diag1 = set()
    diag2 = set()
    for i in range(SIZE):
        diag1.add(field[i][i])
        diag2.add(field[i][SIZE - i - 1])
        line = "".join({field[j][i] for j in range(SIZE)})
        column = "".join({field[i][j] for j in range(SIZE)})
        if line in ["O", "X"]:
            print(f"Выиграл игрок {line}!")
            return True
        if column in ["O", "X"]:
            print(f"Выиграл игрок {column}!")
            return True
    diag1, diag2 = "".join(diag1), "".join(diag2)
    if diag1 in ["O", "X"]:
        print(f"Выиграл игрок {diag1}!")
        return True
    if diag2 in ["O", "X"]:
        print(f"Выиграл игрок {diag2}!")
        return True
    return False


def print_field(field):
    print("*" + " *" * SIZE + " *")
    for i in field:
        print("* " + " ".join(i) + " *")
    print("*" + " *" * SIZE + " *")


def user_choise(field, sym_choice):
    print_field(field)
    print(f"Сейчас ходит игрок {sym_choice}")
    print("*" + " *" * SIZE + " *")
    buffer_list = []
    for i in range(SIZE):
        buffer_str = "* "
        for j in range(SIZE):
            if field[i][j] == "-":
                buffer_list.append((i, j))
                buffer_str = buffer_str + str(len(buffer_list)) + " "
            else:
                buffer_str += "- "
        print(buffer_str + "*")
    print("*" + " *" * SIZE + " *")
    num_choice = -1
    while not (len(buffer_list) > num_choice >= 0):
        num_choice = input("Выберите, куда поставить символ: ")
        try:
            num_choice = int(num_choice) - 1
        except ValueError:
            num_choice = -1
    field[buffer_list[num_choice][0]][buffer_list[num_choice][1]] = sym_choice


def step(sym_choice, current, mode, field, num_step):
    if mode == "1" and sym_choice != current:
        engine.engine(field, num_step, sym_choice, SIZE)
    else:
        user_choise(field, current)


def game_core():
    field = [["-" for _ in range(SIZE)] for _ in range(SIZE)]
    sym_choice = ""
    mode = ""
    while mode not in ["1", "2"]:
        mode = input("Выберите режим (1 - игра с ПК, 2 - игра 2 на 2): ")
    while sym_choice.upper() not in ["X", "O", "Х", "О", "0"] and mode == "1":  # Русский и английский, а ещё ноль
        sym_choice = input("Вы играете X или O?: ")
    sym_choice = "O" if sym_choice.upper() in ["O", "О", "0"] else "X"
    for num_step in range(SIZE ** 2 // 2):  # Есть предельное количество ходов, после которого ничья
        print(f"Ход {num_step + 1}")
        for sym in ('X', 'O'):
            step(sym_choice, sym, mode, field, num_step)
            if puzzle_solved(field):
                print_field(field)
                return
    if SIZE // 2 == 1:  # ещё один ход
        step(sym_choice, "X", mode, field, 5)
    print_field(field)
    print("Ничья!")


def start():
    for sym in "***************************\nXOllnorm by Allnorm\nCreated for Skillfactory\n":
        print(sym, end="", flush=True)
        time.sleep(0.02)


start()
while True:
    game_core()
    if input("Ещё разок?)))) (Д/н): ").upper() in ["Н", "N"]:
        sys.exit()
