import pygame
from grid import *




"""
Tracks row/column , WIDTH, neighbors, color
"""
class Node:
    
    #properties of each node
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col 
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows


    #getters and query functions
    def get_position(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == AQUAMARINE
    
    def is_open(self): 
        return self.color == AQUA
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == DARKGREY
    

    #state change functions
    def reset(self): 
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = AQUAMARINE

    def make_open(self):
        self.color = AQUA

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = DARKGREY

    def make_path(self):
        self.color = YELLOW

    def draw(self, window): 
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))


    #gets all the valid neighbors for the node
    def update_neighbors(self, grid):
        self.neighbors = []

        #check node below
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        #check node above
        if self.row > 0 and not grid[self.row -  1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        #check node right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        #check node left
        if self.col > 0 and not grid[self.row ][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])


    def __lt__(self, other):
        return False