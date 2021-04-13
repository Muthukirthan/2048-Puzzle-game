import random,os
from pynput.keyboard import Key, Listener

def on_press(key):
    #print(f"{key} pressed")
    if key == Key.up:
        board_changed = up(False)
    elif key == Key.down:
        board_changed = down(False)
    elif key == Key.left:
        board_changed = left(False)
    elif key == Key.right:
        board_changed = right(False)
    elif key == Key.esc:
        print("\nGame closed !!")
        return False
    else:
        print("Use arrow keys to play the game!\n")
        return
    if board_changed:
        insert_2_or_4()
    print_board()

def end_game():
    print("\nYOU WON !!")
    print('SCORE :',score)
    exit()

def start_game():
    for _ in range(2):
        board[ random.choice(list(range(total_size))) ] = 2
    print_board()
    play_game()

def play_game():
    with Listener(on_press=on_press) as listener:
        listener.join()

def check_board():
    if 2048 in board:
        end_game()
    elif 0 in board:
        return True
    return False

def insert_2_or_4():
    r = random.randint(0, total_size-1)
    while board[r] != 0:
        r = random.randint(0, total_size-1)
    board[r] = random.choice([2,4])

def create_new_list(from_index, to_index, increment):
    global score
    new_list = [0]
    for j in range(from_index, to_index, increment):
        if board[j] != 0:
            if new_list[-1] == 0:
                new_list[-1] = board[j]
            elif new_list[-1] == board[j]:
                new_list[-1] += board[j]
                score += new_list[-1]
                new_list.append(0)
            else:
                new_list.append(board[j])
    new_list = new_list + [0]*(row_size - len(new_list))
    return new_list

def change_list(new_list, from_index, to_index, increment):
    changed = False
    new_list_index = 0
    for j in range(from_index, to_index, increment):
        if board[j] != new_list[new_list_index]:
            board[j] = new_list[new_list_index]
            changed = True
        new_list_index += 1
    return changed

def up(changed):
    for i in range(row_size):
        new_col = create_new_list(i, total_size, row_size)
        changed = change_list(new_col, i, total_size, row_size)
    return changed

def down(changed):
    for i in range(row_size):
        new_col = create_new_list((total_size+i) - row_size, -1, -row_size)
        changed = change_list(new_col, (total_size+i) - row_size, -1, -row_size)
    return changed
    
def left(changed):
    for i in range(0,total_size, row_size):
        new_row = create_new_list(i, i+row_size, 1)
        changed = change_list(new_row, i, i+row_size, 1)
    return changed
    
def right(changed):
    for i in range(0,total_size, row_size):
        new_row = create_new_list((i+row_size)-1, i-1, -1)
        changed = change_list(new_row, (i+row_size)-1, i-1, -1)
    return changed
    
def clear():
    os.system("cls")

def print_board():
    clear()
    if check_board() == False:
        print("YOU LOST !!!!")
        print(f"SCORE : {score}")
        exit()
    print(f"\t\t\t\tSCORE : {score}\n")
    for i in range(total_size):
        if i % row_size == 0:
            print(f"\n\t\t\t---------------------------------{'-' * (row_size-4)*8}")
            print(end="\t\t\t|  ")
        print(" " if board[i] == 0 else board[i], end="")
        if board[i] < 10:
            print("    |  ", end="")
        elif board[i] > 9 and board[i] < 100:
            print("   |  ", end="")
        elif board[i] > 99 and board[i] < 1000:
            print("  |  ", end="")
        elif board[i] > 999 and board[i] < 10000:
            print(" |  ", end="")
    print(f"\n\t\t\t---------------------------------{'-' * (row_size-4)*8}")
    print("\n\t\t\tPress ESC to quit the game")

score = 0
print("\nDifficulty level:")
print("1 => Easy   (4 x 4)")
print("2 => Medium (5 x 5)")
print("3 => Hard   (6 x 6)")
row_size = int(input("\nplease enter the difficulty level of game: "))
while row_size < 1 or row_size > 3:
    row_size = int(input("\nplease enter a proper choice: "))
row_size += 3
total_size = row_size*row_size
board = [0]*(total_size)
start_game()