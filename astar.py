import pygame
from grid import *
from node import *
from queue import PriorityQueue

    
#heuristic function, using the Manhattan Distance Formula aka quickest "L" distance
def h(point1, point2):
    #extract coordiates
    x1, y1 = point1
    x2, y2 = point2

    return abs(x1 - x2) + abs(y1 - y2)


#astar algorithm
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
            reconstruct_path(previous, end, start, draw)
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

        #draw updated board
        draw()
        
        #after we're done with a node mark it as done
        if current != start: 
            current.make_closed()


    return False



#retraces back the shortes path
def reconstruct_path(previous, current, start, draw):

    #eventually terminates because start node is not in start
    while current in previous:
        current = previous[current]
        if current == start:
            break

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



#draws grid lines
def draw_grid(window, rows, width):
    gap = WIDTH // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))

        for j in range(rows):
            pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, width))



#draw grid board
def draw(window, grid, rows, width):
    window.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update()


#gets the clock position
def get_click_position(position, rows, width):
    gap = width // rows
    y, x = position

    row = y // gap
    col = x // gap

    return row, col



def main(window, width):

    #declare number of rows (and columns since its a square) you want. The higher the number the more squares -> the slower it will run
    ROWS = 40

    #make the grid
    grid = make_grid(ROWS, width)

    #start and end are both None to start
    start = None
    end = None

    run = True

  
    while run:
        
        #draws the grid
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

                #reset that node (make it white)
                node.reset()

                #if deleted start or end nodes, make them None again
                if node == start:
                    start = None

                elif node == end:
                    end = None



            #if user presses space, start astar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid: 
                        for node in row: 

                            #update all the neighbors
                            node.update_neighbors(grid)

                    astar(lambda: draw(window, grid, ROWS, width), grid, start, end)

            
                #if the user presses "c", clear the board
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    
    pygame.quit()



#magic happens
main(WIN, WIDTH)

