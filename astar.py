import pygame
import math 
from queue import PriorityQueue


#setting up visualizer display windowdow
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Shortest Path Search Algorithm")


#colors for board
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


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
        return self.color == RED
    
    def is_open(self): 
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    

    #state change functions
    def reset(self): 
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, window): 
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))


    def update_neighbors(self, grid):
        pass


    def __lt__(self, other):
        return False
    



#heuristic function, using the Manhattan Distance Formula aka quickest "L" distance
def h(point1, point2):
    #extract coordiates
    x1, y1 = point1
    x2, y2 = point2

    return abs(x1 - x2) + abs(y1 - y2)



#makes the grid
def make_grid(rows, width):
    grid = []
    gap = width // rows

    #row
    for i in range(rows):
        grid.append([])

        #column
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid



def draw_grid(window, rows, width):
    gap = WIDTH // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))

        for j in range(rows):
            pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, width))


def draw(window, grid, rows, width):
    window.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update()



def get_click_position(position, rows, width):
    gap = width // rows
    y, x = position

    row = y // gap
    col = x // gap

    return row, col



def main(window, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
  

    while run:

        draw(window, grid, ROWS, width)

        #event could be a mouse click, keyboard button pressed etc
        for event in pygame.event.get():

            #event where the "little x" is pressed  
            if event.type == pygame.QUIT: 
                run = False

            #algorithm running (state of board is LOCKED)
            if started:
                continue
            
            
            #left mouse
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, col = get_click_position(position, ROWS, width)
                node = grid[row][col]

                #if start node has not been placed yet, make the node a start node
                if not start and node != end:
                    start = node
                    start.make_start()

                #if end node has not been placed yet, make the node a end node
                elif not end and node != start: 
                    end = node
                    end.make_end()

                #else make the node a barrier
                elif node != end and node != start:
                    node.make_barrier()

            
            #right mouse deletes a block on the board 
            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, col = get_click_position(position, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None

                elif node == end:
                    end = None






    
    pygame.quit()



main(WIN, WIDTH)











        



    
    




    















    

    



    




    








