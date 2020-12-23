import pygame
import time
import random
import math
import socket

BUFFER_SIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    host = socket.gethostname()
    s.bind(('localhost', 5004))
    s.listen(1)
    (conn, addr) = s.accept()
    print("got connection from: ", addr)

def sendMessage(data):
    request = conn.recv(1024)
    if not request:
        print("ERROR")
        pass
    #print("step requested: ", request.decode())
    conn.send(data.encode())

WIDTH = 800
HEIGHT = 800
FPS = 30
grid = []
visited = []
solVisited = []
availableSpaces = {}
solution = []

direction = {
    "N":[0,-1],
    "S":[0,1],
    "E":[1,0],
    "W":[-1,0],
}

n = 10
w = WIDTH/n
h = HEIGHT/n

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid")
clock = pygame.time.Clock()
white = [255, 255, 255]
black = [0,0,0]
screen.fill(white)
pygame.display.update()

def drawGrid(n):
    w = WIDTH/n
    h = HEIGHT/n
    x = 0.0
    y = 0.0
    for i in range(0,n):
        for j in range(0,n):
            pygame.draw.line(screen, black,[x,y],[x+w,y],2) # TOP
            pygame.draw.line(screen, black,[x, y], [x, y+h],2) # LEFT
            pygame.draw.line(screen, black,[x + w, y], [x + w, y + h],2) # RIGHT
            pygame.draw.line(screen, black,[x, y + h], [x+w, y + h],2) # BOTTOM
            grid.append([x,y])
            availableSpaces[(x,y)] = []
            x += w
        x = 0.0
        y += h
    print("grid length: ",len(grid))
    pygame.display.update()

def carveMazefrom(x,y,grid):
    if [x,y] in visited or [x,y] not in grid:
        return
    else:
        visited.append([x,y])


    dir_order = ["N","S","E","W"]
    random.shuffle(dir_order)

    for i in range(0,len(dir_order)):
        next_x = x + (direction.get(dir_order[i])[0])*w
        next_y = y + (direction.get(dir_order[i])[1])*h

        if [next_x, next_y] not in visited and [next_x, next_y] in grid:
            if dir_order[i] == "N":
                availableSpaces[(x,y)] = availableSpaces.get((x,y)) + ["N"]
                pygame.draw.line(screen, white,[x,y],[x+w,y],2)
            if dir_order[i] == "S":
                availableSpaces[(x,y)] = availableSpaces.get((x,y)) + ["S"]
                pygame.draw.line(screen, white,[x, y + h], [x+w, y + h],2)
            if dir_order[i] == "E":
                availableSpaces[(x,y)] = availableSpaces.get((x,y)) + ["E"]
                pygame.draw.line(screen, white,[x + w, y], [x + w, y + h],2)
            if dir_order[i] == "W":
                availableSpaces[(x,y)] = availableSpaces.get((x,y)) + ["W"]
                pygame.draw.line(screen, white,[x, y], [x, y+h],2)
            pygame.display.update()
            #time.sleep(0.01) # Comment This If You Dont Want To Wait For Maze To Generate
            carveMazefrom(next_x,next_y,grid)

def solveMaze (x,y,aSpaces,grid,currentPath):
    if ((x,y) in currentPath):
        return
    currentPath.append((x,y))

    if (x,y) == (WIDTH-w,HEIGHT-h):
        solution[:] = list(currentPath)
        currentPath.pop()
        return

    for i in range(0,len(aSpaces.get((x,y)))):
        next_x = x + (direction.get(aSpaces.get((x,y))[i])[0])*w
        next_y = y + (direction.get(aSpaces.get((x,y))[i])[1])*h
        if aSpaces.get((x,y))[i] == "N":
            solveMaze(next_x,next_y,aSpaces,grid,currentPath)
        if aSpaces.get((x,y))[i] == "S":
            solveMaze(next_x,next_y,aSpaces,grid,currentPath)
        if aSpaces.get((x,y))[i] == "E":
            solveMaze(next_x,next_y,aSpaces,grid,currentPath)
        if aSpaces.get((x,y))[i] == "W":
            solveMaze(next_x,next_y,aSpaces,grid,currentPath)
    currentPath.pop()
    return



drawGrid(n)
carveMazefrom(0,0,grid)
solveMaze(0,0,availableSpaces,grid,[])


def returnTriple(i):
    if(i==0 or i == len(solution)-1):
        return
    p = [solution[i-1][0], solution[i-1][1]]
    x = [solution[i][0], solution[i][1]]
    n = [solution[i+1][0], solution[i+1][1]]
    return p, x, n

def checkforLine(i):
    if returnTriple(i):
        p, x, n = returnTriple(i)
        if p[0] == x[0] and x[0] == n[0]:
            return 1
        if p[1] == x[1] and x[1] == n[1]:
            return 1
        return 0
    else:
        return

def normalise(i):
    if not checkforLine(i) and returnTriple(i):
            p, x, n = returnTriple(i)
            [x[0],x[1]] = [x[0] - p[0], x[1] - p[1]]
            [n[0],n[1]] = [n[0] - p[0], n[1] - p[1]]
            [p[0],p[1]] = [0, 0]

            [x[0],x[1]] = [x[0]/80, x[1]/80]
            [n[0],n[1]] = [n[0]/80, n[1]/80]

            return (p,x,n)

RightTurn = {
    "[1.0, 0.0]":[1.0, 1.0],
    "[0.0, 1.0]":[-1.0, 1.0],
    "[-1.0, 0.0]":[-1.0, -1.0],
    "[0.0, -1.0]":[1.0, -1.0],
}

LeftTurn = {
    "[1.0, 0.0]":[1.0, -1.0],
    "[0.0, 1.0]":[1.0, 1.0],
    "[-1.0, 0.0]":[-1.0, 1.0],
    "[0.0, -1.0]":[-1.0, -1.0],
}

def findTurn(n):
    if n:
        if n[2] == RightTurn.get(str(n[1])):
            #print("right turn")
            return "[0][255][255][0]"
        elif n[2] == LeftTurn.get(str(n[1])):
            #print("left turn")
            return "[255][0][0][255]"
        else:
            print("error")
            pass
    else:
        return

def instructionCodes(i):
    str = ""
    if i == len(solution)-1:
        str = "[0][0][0][0]"
        return str
    if findTurn(normalise(n)):
        sendMessage(findTurn(normalise(n)))
        return "[0][255][0][255]"
    else:
        return "[0][255][0][255]"


n=0
for i in solution:
    pygame.draw.circle(screen, [255,0,0],[ i[0]+(w/2) , i[1]+(h/2)],10)
    pygame.display.update()
    sendMessage(instructionCodes(n))
    n+=1
    time.sleep(0.5)
sendMessage("stop")
conn.close()

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
