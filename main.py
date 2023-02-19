# Connect 4, Player vs Player or Player vs AI

# Written by Jack Meakin, 02/02/2023

# Requirements:
#   pip install pygame
#   pip install asyncio

import pygame as pg
import random
import copy
import asyncio  # Module required for creating web version

HEIGHT, WIDTH = 700, 700    # window dimensions

WIN = pg.display.set_mode((WIDTH, HEIGHT))

FPS = 60

pg.display.set_caption('CONNECT 4')
pg.font.init()

board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]

BOARD_WIDTH = len(board[0])
BOARD_HEIGHT = len(board)   # Dimensions of board
COUNTER_RAD = 0.9*WIDTH/(2*BOARD_WIDTH)
BLUE = (0,0,200)
WHITE = (200,200,200)
RED = (200,0,0)
YELLOW = (200,200,0)
LIGHT_BLUE = (200,200,255)
DARK_BLUE = (0,0,50)
LIGHT_YELLOW = (200,200,100)
LIGHT_RED = (200,100,100)
DARK_YELLOW = (100,100,50)
GREEN = (0,200,0)
BUTTON_WIDTH = 400
BUTTON_HEIGHT = BUTTON_WIDTH * (16/40)
BUTTON_X = (WIDTH - BUTTON_WIDTH)/2
BUTTON_Y = HEIGHT/4

my_font = pg.font.SysFont('Comic Sans MS', 60)
my_font1 = pg.font.SysFont('Comic Sans MS', 20)
yellow_text = my_font.render('YELLOW WINS!', False, YELLOW)
red_text = my_font.render('RED WINS!', False, RED)
draw_text = my_font.render("IT'S A DRAW!", False, BLUE)
new_game_text = my_font.render("NEW GAME", False, BLUE)
red_text = pg.image.load('red_wins.png')
yellow_text = pg.image.load('yellow_wins.png')
new_game_button = pg.image.load('new_game.png')
pvp_button = pg.image.load('player_vs_player.png')
pva_button = pg.image.load('player_vs_ai.png')
title_button = pg.image.load('connect_4_pic.png')

new_game_button = pg.transform.scale(new_game_button, (BUTTON_WIDTH, BUTTON_HEIGHT/2))
yellow_text = pg.transform.scale(yellow_text, (BUTTON_WIDTH, BUTTON_HEIGHT/1.8))
red_text = pg.transform.scale(red_text, (BUTTON_WIDTH, BUTTON_HEIGHT/1.8))
pva_button = pg.transform.scale(pva_button, (BUTTON_WIDTH*0.6, BUTTON_HEIGHT))
pvp_button = pg.transform.scale(pvp_button, (BUTTON_WIDTH*0.6, BUTTON_HEIGHT))
title_button = pg.transform.scale(title_button, (BUTTON_WIDTH*0.8, BUTTON_HEIGHT*0.5))

turn = 1
column = 6
won = 0
game_select = 0
red_wins = 0
yellow_wins = 0
score_text = my_font1.render(f"{yellow_wins}-{red_wins}", False, BLUE)

async def main():
    global column
    global board
    global turn
    global won
    global red_wins
    global yellow_wins
    global score_text
    global game_select
    

    run = True
    clock = pg.time.Clock()

    while run:
        clock.tick(FPS)
        draw_window(board) 
        await asyncio.sleep(0)  # Line required for async function
        for event in pg.event.get(): # checks for events (keys, clicks etc)

            if event.type == pg.QUIT:
                run = False
            if won == 0:    # Make sure no one has won
                if turn != 1 or game_select == 2:   # Yellow move in PvAI mode or both moves in PvP mode
                    if event.type == pg.MOUSEMOTION:
                        x = pg.mouse.get_pos()[0]
                        column = int(BOARD_WIDTH * x/WIDTH)
            
                    if event.type == pg.MOUSEBUTTONDOWN:
                        x = pg.mouse.get_pos()[0]
                        column = int(BOARD_WIDTH * x/WIDTH)     # Get column from mouseclick location
                        for row in range(BOARD_HEIGHT-1,-1,-1): # Find lowest 0 row
                            if board[row][column] == 0:
                                board[row][column] = turn
                                turn -= 1
                                turn = abs(turn-1)
                                turn += 1
                                break

                elif game_select == 1:  # Get AI move in PvAI mode
                    column = check_wins(board)

                    for row in range(BOARD_HEIGHT-1,-1,-1): # Find lowest 0 row
                        if board[row][column] == 0:
                            board[row][column] = turn
                            turn -= 1
                            turn = abs(turn-1)
                            turn += 1
                            break
                
                check_horizontal_win(board) # Check for wins and draws after moves have been made
                check_vertical_win(board)
                check_positive_diag(board)
                check_negative_diag(board)
                check_draw(board)
            
            else:   # Won not = 0 so reset game if new game clicked
                if event.type == pg.MOUSEBUTTONDOWN: 
                    if pg.mouse.get_pos()[0] > BUTTON_X and pg.mouse.get_pos()[0] < BUTTON_X + BUTTON_WIDTH and pg.mouse.get_pos()[1] > BUTTON_Y and pg.mouse.get_pos()[1] < BUTTON_Y + BUTTON_HEIGHT:               
                        board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
                        print(red_wins)
                        if won == 2:
                            yellow_wins += 1
                        elif won == 1:
                            red_wins += 1
                        score_text = my_font1.render(f"{yellow_wins}-{red_wins}", False, BLUE)
                        won = 0
                        turn = random.randint(1,2)
            
            if game_select == 0 and event.type == pg.MOUSEBUTTONDOWN:
                x = pg.mouse.get_pos()[0]
                if x < WIDTH/2:
                    game_select = 1
                else:
                    game_select = 2

def draw_window(board):

    if game_select == 0:    # Display game select screen if game not selected
        WIN.blit(pva_button, (50,HEIGHT/4))
        WIN.blit(pvp_button, (50 + WIDTH/2,HEIGHT/4))
        WIN.blit(title_button, ((WIDTH/2) - 160,30))
    else:
        WIN.fill(BLUE)
        pg.draw.rect(WIN, WHITE,pg.Rect(0,0,WIDTH,HEIGHT/(BOARD_HEIGHT+1)))

        for a in range(BOARD_WIDTH):
            for i in range(BOARD_HEIGHT):   # Check counter color and draw at location
                if board[i][a] == 0:
                    color = WHITE
                elif board[i][a] == 1:
                    color = RED
                elif board[i][a] == 2:
                    color = YELLOW
                elif board[i][a] == 4:
                    color = GREEN

                x = (WIDTH/(BOARD_WIDTH * 2) + a * WIDTH/BOARD_WIDTH)
                y = (HEIGHT/((BOARD_HEIGHT+1) * 2) + i * HEIGHT/(BOARD_HEIGHT+1)) + HEIGHT/(BOARD_HEIGHT+1)

                pg.draw.circle(WIN, DARK_BLUE, (x,y), 1 * COUNTER_RAD)
                pg.draw.circle(WIN, color, (x,y), 0.9 * COUNTER_RAD)
                
                WIN.blit(score_text, (5,5))

                if won == 0 and (turn == 2 or game_select == 2):    # Draw light colored circle over column mouse hovers over before placing a counter
                    if turn == 2:
                        light_color = LIGHT_YELLOW
                    else:
                        light_color = LIGHT_RED
                    light_x = (WIDTH/(BOARD_WIDTH * 2) + column * WIDTH/BOARD_WIDTH)
                    light_y = (HEIGHT/((BOARD_HEIGHT+1) * 2) + 0 * HEIGHT/(BOARD_HEIGHT+1))
                    pg.draw.circle(WIN, BLUE, (light_x,light_y), COUNTER_RAD * 0.85)
                    pg.draw.circle(WIN, light_color, (light_x,light_y), COUNTER_RAD * 0.8)
                
                if won == 2:    # Display winning message
                    WIN.blit(yellow_text,(-200+WIDTH/2, 10))
                    WIN.blit(new_game_button,(BUTTON_X,BUTTON_Y))

                elif won == 1:
                    WIN.blit(red_text,(-200+WIDTH/2, 10))
                    WIN.blit(new_game_button,(BUTTON_X,BUTTON_Y))

                elif won == 3:
                    WIN.blit(draw_text,(-190+WIDTH/2, 10))
                    WIN.blit(new_game_button,(BUTTON_X,BUTTON_Y))

    pg.display.update()

def avoid_column(game_board):   # Find columns where the AI should avoid as they could lead to a player win
    global won
    global board
    global turn
    columns = []
    test_board = copy.deepcopy(game_board)
    hold_board1 = copy.deepcopy(game_board)
    for a in range(BOARD_WIDTH):
        column1 = a
        test_board = copy.deepcopy(hold_board1)
        for row in range(BOARD_HEIGHT-1,-1,-1): # Place an AI counter in each column then proceed to test if it is possible for player to win on next turn
            if test_board[row][column1] == 0:
                test_board[row][column1] = 1
                break
        hold_board2 = copy.deepcopy(test_board)
        for b in range(BOARD_WIDTH):
            column2 = b
            for row in range(BOARD_HEIGHT-1,-1,-1):
                if test_board[row][column2] == 0:
                    test_board[row][column2] = 2
                    break
            check_horizontal_win(test_board)    # If player can win, win checks will make won 1
            check_vertical_win(test_board)
            check_positive_diag(test_board)
            check_negative_diag(test_board)
           
            board = copy.deepcopy(hold_board1)  # Reset boards
            test_board = copy.deepcopy(hold_board2)
            if won != 0:
                if a not in columns:
                    columns.append(a)   # If player can win, add column to list of those to avoid
                won = 0
                next = 1

    return columns

def next_best(board, avoid):    # This function uses a scoring system to indentify the best non winning or blocking move by counting the number of 3 in a rows
    hold_board = copy.deepcopy(board)
    highest = 0
    best_col = 'a'
    for a in [x for x in range(BOARD_WIDTH) if x not in avoid]:     # Iterate all columns not in avoid
        if board[0][a] != 0:     # If column is full (top row contains counter), continue to next column
            continue
        board = copy.deepcopy(hold_board)
        column = a
        score = 0
        
        
    
        for row in range(BOARD_HEIGHT-1,-1,-1): # Place an AI counter in each column then proceed to test if it is possible for player to win on next turn
            if board[row][column] == 0:
                board[row][column] = 1

                for row in range(BOARD_HEIGHT): # Iterate through potential board to check 3 in a rows
                    for col in range(BOARD_WIDTH):

        # Check for AI 3 in vertical
                        if row <= BOARD_HEIGHT - 4:
                            window  = [board[row][col], board[row+1][col], board[row+2][col], board[row+3][col]]
                            if window.count(1) == 3 and window.count(0) == 1:                 
                                score += 1 
                                print(f'v {row, col}: {window}')
                    
        # Check for AI 3 horizontal
                        if col <= BOARD_WIDTH - 4:
                            window = [board[row][col], board[row][col+1], board[row][col+2], board[row][col+3]]
                            if window.count(1) == 3 and window.count(0) == 1:
                                print(f'H {row, col}: {window}')
                                score += 1 
        
        # Check for positive diagonal
                        if row >= BOARD_HEIGHT - 3 and col <= BOARD_WIDTH - 4:
                            window = [board[row][col], board[row-1][col+1], board[row-2][col+2], board[row-3][col+3]]
                            if window.count(1) == 3 and window.count(0) == 1:
                                print(f'pd {row, col}: {window}')
                                score += 1.01   # Value diagonal higher than non diag

        # Check for negative diagonal
                        if row < 3 and col <= BOARD_WIDTH - 4:
                            window = [board[row][col], board[row+1][col+1], board[row+2][col+2], board[row+3][col+3]]
                            if window.count(1) == 3 and window.count(0) == 1:
                                print(f'nd {row, col}: {window}')
                                score += 1.01    
                break              
            else:
                continue
        print(score, a)
        if score > highest: # Remember highest score
            highest = score
            best_col = a
    return best_col

def check_wins(game_board): # Check if AI can win and if not, check if it can block
    global won
    global board
    global turn
    test_board = copy.deepcopy(game_board)
    hold_board = copy.deepcopy(game_board)

    next = 0
    for a in range(BOARD_WIDTH):
        column = a
        for row in range(BOARD_HEIGHT-1,-1,-1):
            if test_board[row][column] == 0:
                test_board[row][column] = turn
                break

        check_horizontal_win(test_board)
        check_vertical_win(test_board)
        check_positive_diag(test_board)
        check_negative_diag(test_board)
        board = copy.deepcopy(hold_board)
        test_board = copy.deepcopy(hold_board)
        if won != 0:
            column = a
            won = 0
            next = 1
            break
    print('next', next)
    if next == 0: # AI can not win so need to check for blocks

        hold_turn = copy.deepcopy(turn)
        turn -= 1
        turn = abs(turn-1)
        turn += 1

        for a in range(BOARD_WIDTH):
            column = a
            for row in range(BOARD_HEIGHT-1,-1,-1):
                if test_board[row][column] == 0:
                    test_board[row][column] = turn
                    break
                
            check_horizontal_win(test_board)
            check_vertical_win(test_board)
            check_positive_diag(test_board)
            check_negative_diag(test_board)
            board = copy.deepcopy(hold_board)
            test_board = copy.deepcopy(hold_board)
            if won != 0:
                column = a
                won = 0
                next = 1
                break

        turn = copy.deepcopy(hold_turn)

    if next == 0: # If AI can not block or win, find next best move
        available = []
        for entry in range(len(board[0])):
            if board[0][entry] == 0:
                available.append(entry)
        avoid = avoid_column(board) # Find which columns will set up opponent for a win
        column = next_best(board, avoid)    # Find column that creates the most 3 in a row for AI

        if column == 'a':
            sampleList = [0,1,2,3,4,5,6]
            if len([x for x in available if x not in avoid]) == 0:
                avoid = []
            for i in range(BOARD_WIDTH - 4):    # Need to avoid the case of player getting 3 in a row on the bottom
                print(board[5][i:i+5])
                if board[5][i:i+5] == [0,2,2,0,0]:
                    column = i + 3
                elif board[5][i:i+5] == [0,0,2,2,0]:
                    column = i + 1
                elif board[5][i:i+5] == [0,2,0,2,0]:
                    column = i + 2
            while 1:
                if board[0][3] == 0 and column == 'a':  # Pick central column if free
                    column = 3
                elif column == 'a':
                    column = random.choices(sampleList, weights=(10, 100, 1000, 0, 1000, 100, 10))[0] # Central columns are more likely to be picked     
                if hold_board[0][column] == 0 and column not in avoid:  # Repick if column in avoid
                    break
    pg.time.delay(400)
    return column

def check_horizontal_win(board):
    global won
    current = 0

    for row in range(BOARD_HEIGHT):
        total = 0
        rows = []
        cols = []
        for col in range(BOARD_WIDTH):
            if current == board[row][col]:
                total += 1
                rows.append(row)
                cols.append(col)

            else:
                total = 1
                current = board[row][col]
                rows = []
                cols = []
                rows.append(row)
                cols.append(col)
            if total == 4 and current != 0:
                won = current 
                #print('hor')
                for r in range(len(rows)):
                    board[rows[r]][cols[r]] = 4

def check_vertical_win(board):
    global won
    current = 0
    for col in range(BOARD_WIDTH):
        total = 0
        rows = []
        cols = []
        for row in range(BOARD_HEIGHT):
            counter = board[row][col]

            if current == counter:
                total += 1
                rows.append(row)
                cols.append(col)
            else:
                total = 1
                current = counter
                rows = []
                cols = []
                rows.append(row)
                cols.append(col)
            if total == 4 and current != 0:
                won = current
                #print('vert')

                for r in range(len(rows)):
                    board[rows[r]][cols[r]] = 4
                            
def check_positive_diag(board):
    global won
    for row in range(BOARD_HEIGHT-1, 2,-1):
        hold_row = row
        for col in range(BOARD_WIDTH-3): # -3 as to be 4 in a row, the line must start in the bottom left of the board
            row = hold_row
            current = board[row][col]
            total = 1
            rows = []
            cols = []
            rows.append(row)
            cols.append(col)
            if current != 0:
                for next in range(1,4): # Iterate through each point starting from leftmost to and going up and across
                    row -= 1
                    col += 1
                    if current == board[row][col]:
                        total += 1
                        rows.append(row)
                        cols.append(col)
                        if total == 4:
                            won = current
                            #print('pos')
                            for r in range(len(rows)):
                                board[rows[r]][cols[r]] = 4
                            break
                    else:
                        break

def check_negative_diag(board):
    global won
    current = 0
    total = 1
    for row in range(BOARD_HEIGHT-3):
        hold_row = row
        for col in range(BOARD_WIDTH-3):
            row = hold_row
            current = board[row][col]
            total = 1
            rows = []
            cols = []
            rows.append(row)
            cols.append(col)
            if current != 0:
                for next in range(1,4):
                    row += 1
                    col += 1
                    if current == board[row][col]: 
                        total += 1
                        rows.append(row)
                        cols.append(col)
                        
                        if total == 4:
                            won = current
                            #print('neg')
                            for r in range(len(rows)):
                                board[rows[r]][cols[r]] = 4
                            break
                    else:
                        break

def check_draw(board): # Check for gaps
    global won
    total = 0
    for row in board:
        for col in row:
            if col == 0:
                total += 1
    if total == 0 and won == 0:
        won = 3

asyncio.run(main())
