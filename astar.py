import pygame
from queue import PriorityQueue

#setting up visualizer display windowdow
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Shortest Path Search Algorithm")

#colors for board
AQUAMARINE = (28,134,238)
AQUA = (16,78,139)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255,255,0)
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
        return self.color == AQUAMARINE
    
    def is_open(self): 
        return self.color == AQUA
    
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
        self.color = AQUAMARINE

    def make_open(self):
        self.color = AQUA

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = YELLOW

    def draw(self, window): 
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))


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
    



#heuristic function, using the Manhattan Distance Formula aka quickest "L" distance
def h(point1, point2):
    #extract coordiates
    x1, y1 = point1
    x2, y2 = point2

    return abs(x1 - x2) + abs(y1 - y2)



"""
Takes in the function draw

"""
def astar(draw, grid, start, end):

    #count breaks ties between two nodes that have the same f score
    #tiebreaker = whichever node is inserted first
    count = 0

    open_set = PriorityQueue()

    open_set.put((0, count, start))

    #keeps track of the previous node of a node (used to backtrack path)
    previous = {}

    #g score of each node, which is the current shortest distance from the start node to this node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    
    #f score of each node, which is the pAQUAMARINEicted distance of this node to the end node
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = 0 + h(start.get_position(), end.get_position())

    #keeps track of what nodes are in the priority queue or not in O(1)
    open_set_hash = {start}

    #keeps looping as long as the pq is not empty
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        #gets the node with the lowest f score from the queue
        current = open_set.get()[2]
        open_set_hash.remove(current)

        #if it's the end then we found the shortest path, so need to reconstruct by backtracking
        if current == end:
            reconstruct_path(previous, end, draw)
            end.make_end()
            return True
        
        #iterate through each neighbor
        for neighbor in current.neighbors:

            #gscore + 1 (because it would be 1 more from the start than the current node)
            temp_g_score = g_score[current] + 1

            #if the new g score is better than the previous g score it had, update it since we found a better g score
            if temp_g_score < g_score[neighbor]:

                #record the previous node of the neighbor (which is the current node)
                previous[neighbor] = current

                #update the g score (because we found a better one)
                g_score[neighbor] = temp_g_score

                #update f score
                f_score[neighbor] = temp_g_score + h(neighbor.get_position(), end.get_position())

                #if this neighbor is not in the pq, add it
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start: 
            current.make_closed()


    return False


def reconstruct_path(previous, current, draw):

    #eventually terminates because start node is not in start
    while current in previous:
        current = previous[current]
        current.make_path()
        draw()

                

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



            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid: 
                        for node in row: 
                            node.update_neighbors(grid)


                    astar(lambda: draw(window, grid, ROWS, width), grid, start, end)

            

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    
    pygame.quit()



main(WIN, WIDTH)











        



    
    




    















    

    



    




    








