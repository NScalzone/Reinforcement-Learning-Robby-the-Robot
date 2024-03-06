from random import randint
from robot_board import GridWorld, Square

def get_current_state(world:GridWorld, robby_row:int, robby_col:int):
    """
    # Current state is returned as a string, with
    # the letter C indicating a can, W indicating a wall, and the letter E indicating an empty square.
    # The first character is the current square, then North, East, South, and West.
    """
    if world.board[robby_row][robby_col].has_can:
        current = "C"
    else:
        current = "E"
        
    if robby_row == 0:
        north = "W"
    else:
        if world.board[robby_row - 1][robby_col].has_can:
            north = "C"
        else:
            north = "E"
            
    if robby_row == 9:
        south = "W"
    else:
        if world.board[robby_row + 1][robby_col].has_can:
            south = "C"
        else:
            south = "E"
            
    if robby_col == 0:
        west = "W"
    else:
        if world.board[robby_row][robby_col - 1].has_can:
            west = "C"
        else:
            west = "E"
            
    if robby_col == 9:
        east = "W"
    else:
        if world.board[robby_row][robby_col + 1].has_can:
            east = "C"
        else:
            east = "E"
            
    state = current + north + east + south + west
    return state

def pick_up_can(world:GridWorld, robby_row:int, robby_col:int):
    if world.board[robby_row][robby_col].has_can:
        world.board[robby_row][robby_col].has_can = False
        return True
    else:
        return False

def move_north(world:GridWorld, robby_row:int, robby_col:int):
    new_row = robby_row - 1
    new_col = robby_col
    if new_row < 0:
        return False
    else:
        world.moveRobby(new_row, new_col)
        return True

def move_east(world:GridWorld, robby_row:int, robby_col:int):
    new_row = robby_row
    new_col = robby_col + 1
    if new_col > 9:
        return False
    else:
        world.moveRobby(new_row, new_col)
        return True
    
def move_south(world:GridWorld, robby_row:int, robby_col:int):
    new_row = robby_row + 1
    new_col = robby_col
    if new_row > 9:
        return False
    else:
        world.moveRobby(new_row, new_col)
        return True
    
def move_west(world:GridWorld, robby_row:int, robby_col:int):  
    new_row = robby_row
    new_col = robby_col - 1
    if new_col < 0:
        return False
    else:
        world.moveRobby(new_row, new_col)
        return True
    
def greedy_move(world:GridWorld, robby_row:int, robby_col:int, current_state:str):
    print(current_state)
    if current_state[0] == "C":
        pick_up_can(world, robby_row, robby_col)
    elif current_state[1] == "C":
        if move_north(world, robby_row, robby_col):
            robby_row -= 1
    elif current_state[2] == "C":
        if move_east(world, robby_row, robby_col):
            robby_col += 1
    elif current_state[3] == "C":
        if move_south(world, robby_row, robby_col):
            robby_row += 1
    elif current_state[4] == "C":
        if move_west(world, robby_row, robby_col):
            robby_col -= 1
            
    else:
        move = randint(0, 3)
        if move == 0:
            if move_north(world, robby_row, robby_col): 
                robby_row -= 1
        elif move == 1:
            if move_east(world, robby_row, robby_col):
                robby_col += 1
        elif move == 2:
            if move_south(world, robby_row, robby_col):
                robby_row += 1
        else:
            if move_west(world, robby_row, robby_col):
                robby_col -= 1
    return robby_row, robby_col
    
robby_row = randint(0, 9)
robby_col = randint(0, 9)
world = GridWorld(10, 10, robby_row, robby_col)
world.display_grid_world()
 
current_state = get_current_state(world, robby_row, robby_col)
print(current_state)

M = 20
while M > 0:
    current_state = get_current_state(world, robby_row, robby_col)
    robby_row, robby_col = greedy_move(world, robby_row, robby_col, current_state)
    world.display_grid_world()
    print((20 - M))
    M -= 1

