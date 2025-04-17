import math

#Hamming Distance
def hamming_distance(grid : list[list[int]]) -> int:
    flattened_grid = [item for arr in grid for item in arr]
    dist = 0
    for i, num in enumerate(flattened_grid):
        if(num != 0 and i + 1 != num):
            dist += 1
    
    return dist

#Manhattan Distance
def manhattan_distance(grid : list[list[int]]) -> int:
    dist = 0
    k = len(grid)
    for row, arr in enumerate(grid):
        for col, num in enumerate(arr):
            if(num == 0):
                continue
            target_row = (num - 1) // k
            target_col = (num - 1) % k
            curr_dist = abs(row - target_row) + abs(col - target_col)
            dist += curr_dist
            #print(f"manhattan dist for {num} = {curr_dist}")
        
    return dist

#Euclidean Distance
def euclidean_distance(grid : list[list[int]]) -> int:
    dist = 0
    k = len(grid)
    for row, arr in enumerate(grid):
        for col, num in enumerate(arr):
            if(num == 0):
                continue
            target_row = (num - 1) // k
            target_col = (num - 1) % k
            curr_dist = (abs(row - target_row))**2 + (abs(col - target_col))**2
            dist += math.sqrt(curr_dist)
            #print(f"euclidean dist squared for {num} = {curr_dist}")

    return dist.__round__(3)

def row_conflicts(arr, row, num, num_index):
    conflicts = 0
    k = len(arr)
    for i,elem in enumerate(arr):
        target_row = (elem - 1) // k
        if(row == target_row and num > elem and num_index < i):
            conflicts += 1
            #print(f"conflict in row {row} bw {num} and {elem}")
    
    return conflicts

def col_conflicts(arr, col, num, num_index):
    conflicts = 0
    k = len(arr)
    for i, elem in enumerate(arr):
        target_col = (elem - 1) % k
        if(col == target_col and num > elem and num_index < i):
            conflicts += 1
            #print(f"conflict in col {col} bw {num} and {elem}")

    return conflicts

#Linear Conflict
def linear_conflict(grid : list[list[int]]) -> int:
    conflicts = 0
    k = len(grid)
    #row wise
    for row, arr in enumerate(grid):
        for col, num in enumerate(arr):
            target_row = (num - 1) // k
            target_col = (num - 1) % k
            if(target_row == row):
                conflicts += row_conflicts(arr, row, num, col)
            if(target_col == col):
                col_arr = [row[col] for row in grid]
                conflicts += col_conflicts(col_arr, col, num, row)
    
    #print(f"no of linear conflicts : {conflicts}")
    return manhattan_distance(grid) + (2 * conflicts)
            
            
