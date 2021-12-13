import copy
class Node:
    # We initialize the new node with the data which is required.
    def __init__(self,data,path_cost,hueristic,parent):
        self.state = data
        self.path_cost = path_cost# path cost is the level. 
        # hueristic: heuristic value(1 or 2 which is misplaced tiles or manhatten distance).
        self.heuristic_func = hueristic
        self.Tcost = path_cost+hueristic # Tcost : total cost.
        self.parent_node = parent#parent of the node that is getting intialised.
        self.child_nodes = []#the possible outcomes for the current node_state is stored in this list.
            
    # index function returns position of 0 in the **8 puzzle in the intial_state or in the goal_state.
    def get_zero_index(self,matrix,k):
        for i in range(0,len(self.state)):
            for j in range(0,len(self.state)):
                if matrix[i][j] == k:
                    return i,j    
    
    # Move the 0 in the given direction and if the position is out of limits the return None.
    def move_title(self,first,second):
        posi_1 = first[0]
        posj_1 = first[1]
        posi_2 = second[0]
        posj_2= second[1]
        #copy library of python is used to create a deepcopy of the current state that is being changed based on the free title which is 0.
        temp_state = copy.deepcopy(self.state)
        temp = temp_state[posi_1][posj_1]
        temp_state[posi_1][posj_1] = temp_state[posi_2][posj_2]
        temp_state[posi_2][posj_2] = temp
        return temp_state

    # Moving the 0 in either left, right, up or down directions.
    def create_childnodes(self):
        self.zero = self.get_zero_index(self.state,0)
        ith_pos,jth_pos = self.get_zero_index(self.state,0)
        left = jth_pos - 1
        down = ith_pos + 1
        up = ith_pos - 1
        right = jth_pos + 1
        self.generate_child_nodes = []
        no_rows = 2
        no_cols = 2
        if(right <= no_cols):
            self.generate_child_nodes.append((ith_pos, right))
            puzzle.generated_count+=1
            
        if(up >= 0):
            self.generate_child_nodes.append((up, jth_pos))
            puzzle.generated_count+=1
            
        if(left >= 0):
            self.generate_child_nodes.append((ith_pos, left))
            puzzle.generated_count+=1
        
        if(down <= no_rows):
            self.generate_child_nodes.append((down, jth_pos))
            puzzle.generated_count+=1

class puzzle_solver:
    def __init__(self):
        self.open_list = []
        self.close_list = []
        
    # takes the input for the puzzle from the user and returns the input state as a 3*3 matrix
    #And it is also used to get the goal state from the user.
    def input_matrix(self,name_state):
            print("Enter the "+name_state+" state  values:")
            state=[]
            for i in range(0,9):
                n=int(input("Enter the values:"))
                state.append(n)
            return [state[0:3],state[3:6],state[6:9]]
    
    # Read the states {start,goal} and initialize node count to 0
    def initaliasing_states(self):
        self.start_state = self.input_matrix("initial")
        self.goal_state = self.input_matrix("Goal")
        self.node_count = 0

    # get the heuristic {Misplacedtiles, Manhattendistance} from the user
    def get_heuristic(self):
        while True:
            self.heuristic_func = input("\n Choose a heuristic approach:\n 1. Misplaced Tiles or 2. Manhattan Distance:\n")
            if self.heuristic_func == '1' or self.heuristic_func == '2':
                break
            else:
                print("Select a Valid Input")

    # get_zeroth_index function returns position of title with 0 in the given puzzle.
    def get_zeroth_index(self,matrix,num):
        for i in range(0,len(matrix)):
            for j in range(0,len(matrix)):
                if matrix[i][j] == num:
                    return i,j                
  
    # calculate the h(n) based on the user selected 
    def heuristic_functions(self,current_state,goal_state):
        if self.heuristic_func == '1':
            misplaced_tiles = 0
            for i in range(0,9):
                current_state_position = self.get_zeroth_index(current_state,i)
                goal_state_position = self.get_zeroth_index(goal_state,i)
                if current_state_position != goal_state_position:
                    misplaced_tiles += 1
            return misplaced_tiles 
        else:
           manhatten_value = 0
           for num in range(0,9):
               current_state_position = self.get_zeroth_index(current_state,num)
               goal_state_position = self.get_zeroth_index(goal_state,num)
               total_distance = abs(current_state_position[0] - goal_state_position[0]) + abs(current_state_position[1] - goal_state_position[1])
               manhatten_value += total_distance
           return manhatten_value
           
    # selected node with f,g and h values
    def node_selected(self,node,info = True):
        current_state = node
        if info == True:
            print("The path_cost g(n) = ", node.path_cost, ", heuristic value h(n) = ",node.heuristic_func, "And the total cost to reach the goal state f(n) = g(n)+h(n) = ",node.Tcost)
            current_state = node.state
            # print(current_state)
            for i in range(0,len(current_state)):
                for j in range(0,len(current_state[i])):
                    print(current_state[i][j],end=" ")
                print()
        
    # this is main function solving of the puzzle starts from here
    def solver_function(self):
        self.generated_count = 0
        self.initaliasing_states()
        self.get_heuristic()
        initial_hueristic = self.heuristic_functions(self.start_state,self.goal_state)
        # initialize start state and append the start node to opened list 
        start_state = Node(self.start_state,0,initial_hueristic,None)
        self.open_list.append(start_state)
        while True:
            current_node = self.open_list[0]
            self.node_count += 1
            self.node_selected(current_node)
            if current_node.heuristic_func == 0:
                print("Goal state has been reached\n\n")
                break
            current_node.create_childnodes()
            for node in current_node.generate_child_nodes:
                temp_node = current_node.move_title(node,current_node.zero)                
                #Calculating the heuristic value using the heuristic function
                temp_hueristic = self.heuristic_functions(temp_node,self.goal_state)
                current_node.child_nodes.append(Node(temp_node,current_node.path_cost+1,temp_hueristic,current_node))
            for node in current_node.child_nodes:
                self.open_list.append(node)
            #if a node is visited it is appended to the close_list
            self.close_list.append(current_node)
            del self.open_list[0]
            self.open_list.sort(key = lambda val:val.Tcost,reverse=False)
            # if the program is unable to find solution after 500 iterations then we end it saying no solution is found
            if self.node_count > 200:
                print("Unable to get a solution after 200 iterations!!")
                break

#the execution of the program starts from here 
if __name__=="__main__":
    puzzle = puzzle_solver()
    puzzle.solver_function()
    print("Number of nodes generated: ", puzzle.generated_count)
    print("Number of  nodes expanded: ", len(puzzle.close_list))

