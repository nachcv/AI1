#!/usr/bin/env python
"""
Name of the author(s):
- Auguste Burlats <auguste.burlats@uclouvain.be>
"""
import time
import sys
from copy import deepcopy
from search import *


#################
# Problem class #
#################
class TowerSorting(Problem):

    def actions(self, state):
        num=state.number
        size=state.size
        grid=state.grid
        #Selection of the possible movements.
        for move in range(num):
            for compare in range(num):
                if(move!=compare and len(grid[move])>0 and len(grid[compare])<size):
                    move_tup=(move,compare)
                    yield move_tup

    def result(self, state, action):
        origin = action[0]
        end = action[1]
        modify_grid=state.grid
        value = modify_grid[origin].pop()
        modify_grid[end].append(value)
        new_state = State(state.number, state.size,modify_grid,'Value :'+ str(value)+' moved from '+ str(origin) + " to "+ str(end))
        return new_state

    def goal_test(self, state):
        num=state.number
        size=state.size
        grid=state.grid
        for colum in range(num):
            if (len(grid[colum])!=0 and len(grid[colum])!=size):
                return False
            else:
                for same in range(size-1):
                    if grid[colum][same]!=grid[colum][same+1]:
                        return False
        return True


###############
# State class #
###############
class State:

    def __init__(self, number, size, grid, move="Init"):
        self.number = number
        self.size = size
        self.grid = grid
        self.move = move

    def __str__(self):
        s = self.move + "\n"
        for i in reversed(range(self.size)):
            for tower in self.grid:
                if len(tower) > i:
                    s += "".join(tower[i]) + " "
                else:
                    s += ". "
            s += "\n"
        return s
    #unico objetivo es ver si dos grid son iguales
    def __eq__(self, other):
        eq = True
        if ((self.number == other.number) and (self.size == other.size)):
            for i in range(self.number):
                for j in range(self.size):
                    if self.grid[i] == other.grid[i]:
                        eq=True
        else:
            eq=False
        return eq

    def __hash__(self):
        return hash(tuple(tuple(sorted(row)) for row in self.grid))
        


######################
# Auxiliary function #
######################
def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()

    number_tower, size_tower = tuple([int(i) for i in lines[0].split(" ")])
    initial_grid = [[] for i in range(number_tower)]
    for row in lines[1:size_tower+1]:
        elems = row.split(" ")
        for index in range(number_tower):
            if elems[index] != '.':
                initial_grid[index].append(elems[index])

    for tower in initial_grid:
        tower.reverse()

    return number_tower, size_tower, initial_grid


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./sort_tower.py <path_to_instance_file>")
    filepath = sys.argv[1]

    number, size, initial_grid = read_instance_file(filepath)
    
    init_state = State(number, size, initial_grid, "Init")

    problem = TowerSorting(init_state)

    print(problem.actions)

    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)
    end_timer = time.perf_counter()

    # Example of print
    path = node.path()

    for n in path:
        # assuming that the __str__ function of state outputs the correct format
        print(n.state)

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)
