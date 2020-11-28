import pygame, random
from pygame.locals import *

WIDTH = 800
HEIGHT = 800
FPS = 30

white = [255, 255, 255, 255]
black = [0,0,0, 255]
transparent = [0, 0, 0, 0]

class Maze:
    def __init__(self, mazeLayer):
        self.mazeArray = []
        self.state = 'c'        # c = creating, s = solving, r = reset
        self.mLayer = mazeLayer # surface
        self.mLayer.fill((0,0,0,0))#alpha = 0, fill mazeLayer with transparent background
        self.n = 20
        for y in range(self.n): # 20 wide + 20 tall
            pygame.draw.line(self.mLayer, black, (0, y*40), (800, y*40))#draw horizontal lines
            for x in range(self.n):
                self.mazeArray.append(0)
                if ( y == 0 ):
                    pygame.draw.line(self.mLayer, black, (x*40,0), (x*40,800))#draw vertical lines
        # Maze Section
        self.totalCells = 400 # 20 x 20
        self.currentCell = random.randint(0, self.totalCells-1)
        self.visitedCells = 1
        self.cellStack = []
        self.compass = [(-1,0),(0,1),(1,0),(0,-1)]

    def update(self):
        if self.state == 'c':
            if self.visitedCells >= self.totalCells:
                self.currentCell = 0 # set current to top-left
                self.cellStack = []
                #self.state = 's'
                return
            moved = False
            while(self.visitedCells < self.totalCells):#moved == False):
                x = self.currentCell % 20
                y = self.currentCell // 20
                neighbors = []
                for i in range(4):
                    nx = x + self.compass[i][0]
                    ny = y + self.compass[i][1]
                    if ((nx >= 0) and (ny >= 0) and (nx < 20) and (ny < 20)):
                        if (self.mazeArray[(ny*20+nx)]) == 0:# & 0x000F
                            nidx = ny*20+nx
                            neighbors.append((nidx,1<<i))
                            #print(neighbors)
                if len(neighbors) > 0:
                    idx = random.randint(0,len(neighbors)-1)
                    nidx,direction = neighbors[idx]
                    dx = x*40
                    dy = y*40
                    if direction & 1:
                        self.mazeArray[nidx] |= (4)
                        pygame.draw.line(self.mLayer, transparent, (dx,dy+1),(dx,dy+39))
                    elif direction & 2:
                        self.mazeArray[nidx] |= (8)
                        pygame.draw.line(self.mLayer, transparent, (dx+1,dy+40),(dx+39,dy+40))
                    elif direction & 4:
                        self.mazeArray[nidx] |= (1)
                        pygame.draw.line(self.mLayer, transparent, (dx+40,dy+1),(dx+40,dy+39))
                    elif direction & 8:
                        self.mazeArray[nidx] |= (2)
                        pygame.draw.line(self.mLayer, transparent, (dx+1,dy),(dx+39,dy))
                    self.mazeArray[self.currentCell] |= direction
                    self.cellStack.append(self.currentCell)
                    self.currentCell = nidx
                    self.visitedCells = self.visitedCells + 1
                    moved = True
                else:
                    self.currentCell = self.cellStack.pop()

    def draw(self, screen):
        screen.blit(self.mLayer, (0,0))


# initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid")
clock = pygame.time.Clock()
screen.fill(white)
pygame.display.update()

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(white)

mazeLayer = pygame.Surface(screen.get_size())
mazeLayer = mazeLayer.convert_alpha()
mazeLayer.fill(transparent)

newMaze = Maze(mazeLayer)
screen.blit(background, (0, 0))

running = True
while running:
    # keep running at the at the right speed
    clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    screen.blit(background, (0, 0))
    newMaze.update()
    newMaze.draw(screen)
    pygame.display.flip()
