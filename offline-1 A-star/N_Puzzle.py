from helper import Count_Inversion
import copy

class N_Puzzle:
    def __init__(self, initial_grid : list[list[int]], parent : 'N_Puzzle' = None):
        self.grid = initial_grid
        self.moves_count = 0
        self.parent = parent
        self.k = len(initial_grid)
        self.priority = 0

    def get_blank_index(self):
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val == 0:
                   return i,j

    def generate_config(self):
        row_blank, col_blank = self.get_blank_index()
        valid_configs = []
        #up move allowed
        if(row_blank > 0):
            new_grid_up = copy.deepcopy(self.grid)
            target_num = new_grid_up[row_blank-1][col_blank]
            new_grid_up[row_blank][col_blank] = target_num
            new_grid_up[row_blank-1][col_blank] = 0
            valid_configs.append(new_grid_up)

        #down move allowed
        if(row_blank < (self.k - 1)):
            new_grid_down = copy.deepcopy(self.grid)
            target_num = new_grid_down[row_blank + 1][col_blank]
            new_grid_down[row_blank][col_blank] = target_num
            new_grid_down[row_blank + 1][col_blank] = 0
            valid_configs.append(new_grid_down)
            

        #left move allowed
        if(col_blank > 0):
            new_grid_left = copy.deepcopy(self.grid)
            target_num = new_grid_left[row_blank][col_blank - 1]
            new_grid_left[row_blank][col_blank] = target_num
            new_grid_left[row_blank][col_blank - 1] = 0
            valid_configs.append(new_grid_left)
            
        #right move allowed
        if(col_blank < (self.k - 1)):
            new_grid_right = copy.deepcopy(self.grid)
            target_num = new_grid_right[row_blank][col_blank + 1]
            new_grid_right[row_blank][col_blank] = target_num
            new_grid_right[row_blank][col_blank + 1] = 0
            valid_configs.append(new_grid_right)
        
        return valid_configs
    
    def is_correct_config(self) -> bool:
        flattened_grid = [item for row in self.grid for item in row]
        for i, val in enumerate(flattened_grid):
            if(i + 1 != val and val != 0):
                return False
        
        return True
    
    def is_solvable(self) -> bool:
        
        k = len(self.grid)
        flattened_grid = [item for arr in self.grid for item in arr]
        blank_index = flattened_grid.index(0)
        flattened_grid.pop(blank_index)
        _, inversions = Count_Inversion(flattened_grid)
        #print("number of inversions : ", inversions)
        
        # k odd
        if(k % 2):
            return not(inversions % 2)
        else:
            blank_index_from_bottom = k - (blank_index // 2)
            return bool((blank_index_from_bottom % 2) ^ (inversions % 2))

    
    def __str__(self):
        string = ''
        for rows in self.grid:    
            for elem in rows:
                if(elem == 0):
                    string += "- "
                    continue
                string += str(elem) + " "
            string += '\n' 
        
        return string
            
