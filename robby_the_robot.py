from random import randint
from matplotlib import pyplot
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
    
def greedy_move(world:GridWorld, robby_row:int, robby_col:int, action:int):
    action_performed = None
    if action == 0:
        if pick_up_can(world, robby_row, robby_col):
            action_performed = 'P'
        else:
            action_performed = 'M'
    elif action == 1:
        if move_north(world, robby_row, robby_col):
            action_performed = 'N'
            robby_row -= 1
        else:
            action_performed = 'F'
    elif action == 2:
        if move_east(world, robby_row, robby_col):
            action_performed = 'E'
            robby_col += 1
        else:
            action_performed = 'F'
    elif action == 3:
        if move_south(world, robby_row, robby_col):
            action_performed = 'S'
            robby_row += 1
        else:
            action_performed = 'F'
    elif action == 4:
        if move_west(world, robby_row, robby_col):
            action_performed = 'W'
            robby_col -= 1
        else:
            action_performed = 'F'
    return robby_row, robby_col, action_performed

def select_greedy_move(current_state, Q_matrix, all_states, epsilon):
   
    chosen_action = None
    
    #epsilon is the probability of a random move.
    probability_dice = randint(0, 100)
    if probability_dice < (epsilon * 100):
        chosen_action = randint(0, 4)
        best_score = Q_matrix[all_states[current_state]][chosen_action]
    else:
        q_index = all_states[current_state]
      #  if (Q_matrix[q_index][0]) == (Q_matrix[q_index][1]) == (Q_matrix[q_index][2]) == (Q_matrix[q_index][3]) == (Q_matrix[q_index][4]) :
       #     chosen_action = randint(0, 4)
        #    best_score = Q_matrix[q_index][chosen_action]
       # else:
        best_score = max(Q_matrix[q_index])
        chosen_action = Q_matrix[q_index].index(best_score)

    #print(f'action chosen: {action}')
    return best_score, chosen_action  
    

def generate_Q_matrix(all_states, current_state, Q_matrix):
    if current_state not in all_states:
        all_states[current_state] = len(all_states)
        Q_matrix.append([0, 0, 0, 0, 0])
        return True
    else:
        return False
def get_current_Q_value(Q_matrix, all_states, current_state, action_index):
    q_index = all_states[current_state]
    return Q_matrix[q_index][action_index]

def update_Q_matrix(Q_matrix, all_states, current_state, action_index, updated_Q):
    Q_matrix[all_states[current_state]][action_index] = updated_Q
    return Q_matrix 

def display_Q_matrix(Q_matrix, all_states):
    for i in range(len(Q_matrix)):
        print(f'Q-values at index{i}: {Q_matrix[i]}')
 
#current_state = get_current_state(world, robby_row, robby_col)
#print(current_state)

Q_matrix = []
all_states = {}
reward_matrix = []

episodes_N = 5000
steps_M = 200
step_size = 0.2
discount_factor = 0.9
epsilon = 0.1

while episodes_N > 0:
    robby_row = randint(0, 9)
    robby_col = randint(0, 9)
    world = GridWorld(10, 10, robby_row, robby_col)
    world.display_grid_world()
    total_reward = 0
    
    while steps_M > 0:
        
        #get the current state
        current_state = get_current_state(world, robby_row, robby_col)
        generate_Q_matrix(all_states, current_state, Q_matrix)
        
        # identify the best next action
        maxA, action_index = select_greedy_move(current_state, Q_matrix, all_states, epsilon)
        robby_row, robby_col, action = greedy_move(world, robby_row, robby_col, action_index)
        max_state = get_current_state(world, robby_row, robby_col)
        generate_Q_matrix(all_states, max_state, Q_matrix)
        
        # Pick up can
        if action == 'P':
            reward = 10
        # Hit wall
        elif action == 'F':
            reward = -5
        # Pick up can in empty square
        elif action == 'M':
            reward = -1
        else:
            reward = 0
        
        current_Q = get_current_Q_value(Q_matrix, all_states, current_state, action_index)
        max_Q = get_current_Q_value(Q_matrix, all_states, max_state, action_index)
        
        updated_Q = current_Q + (step_size * (reward + (discount_factor * max_Q) - current_Q))
            
        Q_matrix = update_Q_matrix(Q_matrix, all_states, current_state, action_index, updated_Q)
        
        #world.display_grid_world()
        print((200 - steps_M), 'reward:', reward, 'Total reward:', total_reward, 'Current state:', current_state, 'Action:', action, 'current Q', current_Q, 'Max Q:', max_Q, 'Updated Q:', updated_Q)
        #display_Q_matrix(Q_matrix, all_states)
        #print(f'All states: {all_states}, \n Reward matrix: {reward_matrix}') 
        total_reward += reward
        steps_M -= 1
    if episodes_N % 100 == 0:
        reward_matrix.append(total_reward)
    steps_M = 200
    episodes_N -= 1
    if episodes_N % 50 == 0:
        epsilon -= 0.01

display_Q_matrix(Q_matrix, all_states)

with open('Q_matrix.txt', 'w') as f:
    for i in range(len(Q_matrix)):
        f.write(f'{Q_matrix[i]}\n')
print(f'All states: {all_states}, \n Reward matrix: {reward_matrix}')

with open('all_states.txt', 'w') as g:
    for i in all_states:
        g.write(f'{i}\n')

x = [x for x in range(len(reward_matrix))]
pyplot.plot(x, reward_matrix, label = "Total Reward")
pyplot.title('Total Reward per Episode')
pyplot.legend()
pyplot.show()