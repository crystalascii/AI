# coding: utf-8

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

#贪食蛇运行场景的宽和高
HEIGHT = 18
WIDTH = 18
FIELD_SIZE = HEIGHT * WIDTH

#蛇头始终是一维数组的第一个元素
HEAD = 0

FOOD = 0
UNDEFINED = (HEIGHT+1) * (WIDTH+1)
SNAKE = 2 * UNDEFINED

LEFT = -1
RIGHT = 1
UP = -WIDTH
DOWN = WIDTH

#错误码
ERR = -1111

#board代表的是贪食蛇运行的场景
#init the snake at  (1, 1) position
#第0行，第Height行，第0列，第Width列为墙
#贪食蛇初始大小为1
board = [0] * FIELD_SIZE
snake = [0] * (FIELD_SIZE+1)
snake[HEAD] = 1*WIDTH+1
snake_size = 1

#虚拟贪食蛇运行的临时变量
tmpboard = [0] * FIELD_SIZE
tmpsnake = [0] * (FIELD_SIZE+1)
tmpsnake[HEAD] = 1*WIDTH+1
tmpsnake_size = 1

#食物位置为（0~FIELD_SIZE-1），初始位置为（3， 3）
#best_move: 下一时刻的运行方向
food = 2 * WIDTH + 3
best_move = ERR

#方向数组
mov = [LEFT, RIGHT, UP, DOWN]

#接收的按键信息
key = KEY_RIGHT
#分数，也就是贪食蛇长度
score = 1

#检测一个单元格是否被贪食蛇身体占用，如果没占用，返回TRUE，否则，返回False
def is_cell_free(index, psize, psnake):
    return not (index in psnake[:psize])

#检测贪食蛇在当前位置是否可向move指定的方向移动，可移动返回TRUE，否则返回False
def is_move_possible(index, move):
    flag = False
    if move == LEFT:
        flag = True if index%WIDTH > 1 else False
    elif move == RIGHT:
        flag = True if index%WIDTH < (WIDTH-2) else False
    elif move == UP:
        flag = True if index > (2*WIDTH - 1) else False #index/WIDTH > 1
    elif move == DOWN:
        flag = True if index < (FIELD_SIZE-2*WIDTH) else False #index/WIDTH < HEIGHT-2
    return flag
    
#检查一个位置是否有效
def is_position_valid(index):
    flag = False
    if index%WIDTH >= 1 and index%WIDTH <= (WIDTH-2) and index > (WIDTH - 1) and index < (FIELD_SIZE-WIDTH):
        flag = True
    return flag


#重置场景
def board_reset(psnake, psize, pboard):
    for i in xrange(FIELD_SIZE):
        if i == food:
            pboard[i] = FOOD
        elif is_cell_free(i, psize, psnake): #the position is null
            pboard[i] = UNDEFINED
        else: #the cell is snake body
            pboard[i] = SNAKE

#绘制场景
def draw_board(pboard):
    for i in xrange(FIELD_SIZE):
        print("%4d"%pboard[i]), 
        if (i+1)%WIDTH == 0:
            print("");
    print("")


#采用BFS更新地图中的棋盘格的权重，进而可以推算出可行路径
def board_refresh(pfood, psnake, pboard):
    queue = []
    queue.append(pfood)
    inqueue = [0] * FIELD_SIZE
    found = False

    #while loop
    while len(queue) != 0:
        index = queue.pop(0)
        if inqueue[index] == 1: continue
        inqueue[index] = 1
        for i in xrange(4):
            if index + mov[i] == psnake[HEAD]:
                found = True
            if is_position_valid(index+mov[i]) and pboard[index+mov[i]] < SNAKE:  #if the cell is not the snake body
                if pboard[index+mov[i]] > pboard[index] + 1:
                   pboard[index+mov[i]] = pboard[index] + 1
                if inqueue[index+mov[i]] == 0:
                    queue.append(index+mov[i])
    return found

#找出从贪食蛇头部出发的最短的路径
def choose_shortest_safe_move(psnake, pboard):
    best_move = ERR
    min = SNAKE
    for i in xrange(4):
        if is_move_possible(psnake[HEAD], mov[i]) and pboard[psnake[HEAD]+mov[i]] < min:
            min = pboard[psnake[HEAD]+mov[i]]
            best_move = mov[i]
    return best_move


#找出从贪食蛇头部出发的最长路径
def choose_longest_safe_move(psnake, pboard):
    best_move = ERR
    max = -1
    for i in xrange(4):
        if is_move_possible(psnake[HEAD], mov[i]) and pboard[psnake[HEAD]+mov[i]] < UNDEFINED and pboard[psnake[HEAD]+mov[i]] > max:
            max = pboard[psnake[HEAD]+mov[i]]
            best_move = mov[i]
    return best_move

#检测贪食蛇蛇头是否可以跟随蛇尾行走
def is_tail_inside():
    global tmpboard, tmpsnake, food, tmpsnake_size
    tmpboard[tmpsnake[tmpsnake_size-1]] = 0
    tmpboard[food] = SNAKE
    result = board_refresh(tmpsnake[tmpsnake_size-1], tmpsnake, tmpboard)
    for i in xrange(4):
        if is_move_possible(tmpsnake[HEAD], mov[i]) and tmpsnake[HEAD]+mov[i] == tmpsnake[tmpsnake_size-1] and tmpsnake_size > 3:
            result = False
    return result

#让蛇头跟随蛇尾行走
def follow_tail():
    global tmpboard, tmpsnake, food, tmpsnake_size
    tmpsnake_size = snake_size
    tmpsnake = snake[:]
    board_reset(tmpsnake, tmpsnake_size, tmpboard)
    tmpboard[tmpsnake[tmpsnake_size-1]] = FOOD
    tmpboard[food] = SNAKE
    board_refresh(tmpsnake[tmpsnake_size-1], tmpsnake, tmpboard)
    tmpboard[tmpsnake[tmpsnake_size-1]] = SNAKE
    
    return choose_longest_safe_move(tmpsnake, tmpboard)

#找出任何可行的路径
def any_possible_move():
    global food, snake, snake_size, board
    best_move = ERR
    board_reset(snake, snake_size, board)
    board_refresh(food, snake, board)
    min = SNAKE

    for i in xrange(4):
        if is_move_possible(snake[HEAD], mov[i]) and board[snake[HEAD]+mov[i]] < min:
            min = board[snake[HEAD]+mov[i]]
            best_move = mov[i]
    return best_move
    
#数组移动    
def shift_array(arr, size):
    for i in xrange(size, 0, -1):
        arr[i] = arr[i-1]
        
#给贪食蛇喂食        
def new_food():
    global food, snake_size
    cell_free = False
    while not cell_free:
        w = randint(1, WIDTH-2)
        h = randint(1, HEIGHT-2)
        food = h * WIDTH + w
        cell_free = is_cell_free(food, snake_size, snake)
    win.addch(food/WIDTH, food%WIDTH, '@')

#移动贪食蛇    
def make_move(pbest_move):
    global key, snake, board, snake_size, score
    shift_array(snake, snake_size)
    snake[HEAD] += pbest_move
    
    # 按esc退出，getch同时保证绘图的流畅性，没有它只会看到最终结果
    win.timeout(10)
    event = win.getch()
    key = key if event == -1 else event
    if key == 27:return
    
    p = snake[HEAD]
    win.addch(p/WIDTH, p%WIDTH, '*')
    
    # 如果新加入的蛇头就是食物的位置
    # 蛇长加1，产生新的食物，重置board(因为原来那些路径长度已经用不上了)
    if snake[HEAD] == food:
        board[snake[HEAD]] == SNAKE # 新的蛇头
        snake_size += 1
        score += 1
        if snake_size < FIELD_SIZE: new_food()
    else:# 如果新加入的蛇头不是食物的位置
        board[snake[HEAD]] = SNAKE # 新的蛇头
        board[snake[snake_size]] = UNDEFINED
        win.addch(snake[snake_size]/WIDTH, snake[snake_size]%WIDTH, ' ')
        
        
# 虚拟地运行一次，然后在调用处检查这次运行可否可行
# 可行才真实运行。
# 虚拟运行吃到食物后，得到虚拟下蛇在board的位置
def virtual_shortest_move():
    global snake, board, snake_size, tmpsnake, tmpboard, tmpsnake_size, food
    tmpsnake_size = snake_size
    tmpsnake = snake[:]
    tmpboard = board[:]
    board_reset(tmpsnake, tmpsnake_size, tmpboard)
    
    food_eated = False
    while not food_eated:
        board_refresh(food, tmpsnake, tmpboard)
        move = choose_shortest_safe_move(tmpsnake, tmpboard)
        shift_array(tmpsnake, tmpsnake_size)
        tmpsnake[HEAD] += move# 在蛇头前加入一个新的位置
        # 如果新加入的蛇头的位置正好是食物的位置
        # 则长度加1，重置board，食物那个位置变为蛇的一部分(SNAKE)
        
        if tmpsnake[HEAD] == food:
            tmpsnake_size += 1
            board_reset(tmpsnake, tmpsnake_size, tmpboard)# 虚拟运行后，蛇在board的位置(label101010)
            tmpboard[food] = SNAKE
            food_eated = True
        else:# 如果蛇头不是食物的位置，则新加入的位置为蛇头，最后一个变为空格
            tmpboard[tmpsnake[HEAD]] = SNAKE
            tmpboard[tmpsnake[tmpsnake_size]] = UNDEFINED

#寻找安全路径
def find_safe_way():
    global snake, board
    safe_move = ERR
    
    virtual_shortest_move()
    if is_tail_inside():
        return choose_shortest_safe_move(snake, board)
    safe_move = follow_tail()
    return safe_move


curses.initscr()
win = curses.newwin(HEIGHT, WIDTH, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)
win.addch(food/WIDTH, food%WIDTH, '@')

while key != 27:
    win.border(0)
    win.addstr(0, 2, 'S:' + str(score) + ' ')
    win.timeout(10)

    event = win.getch()
    key = key if event == -1 else event
    #reset board
    board_reset(snake, snake_size, board)

    if board_refresh(food, snake, board):
        best_move = find_safe_way()
    else:
        best_move = follow_tail()
        
    if best_move == ERR:
        best_move = any_possible_move()
    
    if best_move != ERR:
        make_move(best_move)
    else:
        break


curses.endwin()
print("\nscore - " + str(score))

