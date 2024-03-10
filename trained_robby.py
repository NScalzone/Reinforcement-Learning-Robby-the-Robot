from random import randint
from matplotlib import pyplot
from robot_board import GridWorld
from robby_the_robot import get_current_state, greedy_move, select_greedy_move

Q_Data = open('Q_matrix.txt', 'r', encoding='UTF-8')
State_Data = open('all_states.txt', 'r', encoding='UTF-8')
Q_matrix = []
all_states = {}
Q_index = 0
for line in Q_Data:
    Q_matrix.append([0,0,0,0,0])
    for i in range(5):
        value = line.strip('[]\n').split(',')[i]
        value = float(value)
        Q_matrix[Q_index][i] = value
        
    Q_index += 1
    

all_states_index = 0
for line in State_Data:
    current_state = line.strip()
    all_states[current_state] = all_states_index
    all_states_index += 1


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
    #world.display_grid_world()
    total_reward = 0
    
    while steps_M > 0:
        
        #get the current state
        current_state = get_current_state(world, robby_row, robby_col)
        
        # identify the best next action
        maxA, action_index = select_greedy_move(current_state, Q_matrix, all_states, epsilon)
        robby_row, robby_col, action = greedy_move(world, robby_row, robby_col, action_index)
        max_state = get_current_state(world, robby_row, robby_col)
        
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
        
        
        #world.display_grid_world()
        #print((200 - steps_M), 'reward:', reward, 'Total reward:', total_reward, 'Current state:', current_state, 'Action:', action, 'current Q', current_Q, 'Max Q:', max_Q, 'Updated Q:', updated_Q)
        #display_Q_matrix(Q_matrix, all_states)
        #print(f'All states: {all_states}, \n Reward matrix: {reward_matrix}') 
        total_reward += reward
        steps_M -= 1
    
    reward_matrix.append(total_reward)
    steps_M = 200
    episodes_N -= 1

print(f'All states: {all_states}, \n Reward matrix: {reward_matrix}')

Average_Reward = sum(reward_matrix) / len(reward_matrix)
Std_Dev_Reward = (sum([(x - Average_Reward)**2 for x in reward_matrix]) / len(reward_matrix))**0.5

print(f'Average Reward: {Average_Reward}, Standard Deviation: {Std_Dev_Reward}')

x = [x for x in range(len(reward_matrix))]
pyplot.plot(x, reward_matrix, label = "Total Reward")
pyplot.title('Total Reward per Episode')
pyplot.legend()
pyplot.show()

Q_Data.close()
State_Data.close()