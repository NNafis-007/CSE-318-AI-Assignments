from N_Puzzle import N_Puzzle
from heuristics import hamming_distance, manhattan_distance, euclidean_distance, linear_conflict
from PQueue import PriorityQueue

#define the heuristic
h_n = euclidean_distance

#Take input
k = int(input("enter matrix size then the elements\n"))
n = k*k

matrix = []
for i in range(k):
    input_str = input("")
    arr = list(map(int, input_str.split(" ")))
    #print(f'string is = {input_str} and corresponding array is {arr}')
    matrix.append(arr)


#Driver code
initial_state = N_Puzzle(matrix)
if not(initial_state.is_solvable()):
    print("Unsolvable puzzle")

else:
    pqueue = PriorityQueue()
    pqueue.push(0, initial_state)

    # open_list : list[N_Puzzle] = []
    #closed_list : list[N_Puzzle] = []
    closed_set: set = set()  # To store string representations of grids
    i = 0
    explored = 0
    expanded = 0
    while pqueue.size() != 0:
        # i += 1
        # print(f"iteration number : {i}")
        _, curr_state = pqueue.pop()
        #closed_list.append(curr_state)
        closed_set.add(str(curr_state.grid))
        expanded += 1
        #print(curr_state)
        if(curr_state.is_correct_config()):
            break
        
        possible_configs = curr_state.generate_config()
        for config in possible_configs:
            nei_puzzle = N_Puzzle(config)
            nei_puzzle.moves_count = curr_state.moves_count + 1
            nei_puzzle.priority = nei_puzzle.moves_count + h_n(nei_puzzle.grid)
            nei_puzzle.parent = curr_state
            if str(nei_puzzle.grid) not in closed_set:
                pqueue.push(nei_puzzle.priority, nei_puzzle)
                explored += 1


    print(f"\nMinimum number of moves =  {curr_state.moves_count}\n")

    #Construct path from nodes
    states_path = []
    while curr_state.parent is not None:
        states_path.append(curr_state)
        curr_state = curr_state.parent
    states_path.append(curr_state)
    states_path = states_path[::-1]

    for state in states_path:
        print(state)

    print("Explored : ", explored)
    print("Expanded : ", expanded)