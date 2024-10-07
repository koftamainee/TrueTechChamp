import numpy as np
from libs.utils import normalize_angle

def show_maze(arr, type=2):
    l = len(arr)
    print("  ", end="")
    for i in range(l):
        print(i, end=(" " * (3 - len(str(i)))))
    print("\n")
    
    ch = lambda x: "* " if x else "  "
    for i in range(l):
        index = str(l - i - 1)
        index = index + (" " * (2 - len(str(index))))
        if type == 1:
            print(index, arr[i], index, end="\n")
        else:
            print(index, *list(map(ch, arr[i])), index, end="\n")

    print("  ", end="")
    for i in range(l):
        print(i, end=(" " * (3 - len(str(i)))))
    print("\n")

def update_maze(data, position, maze):
    print("Walls:")
    yaw = normalize_angle(position[2])
    yaw //= 90

    x = (position[0]) * 2 + 1
    y = (15 - position[1]) * 2 + 1

    wf = [1, 4, 3, 2]
    wr = [2, 1, 4, 3]
    wb = [3, 2, 1, 4]
    wl = [4, 3, 2, 1]

    if not data[wf[yaw]]:
        maze[y - 1][x] = 1
        maze[y - 1][x - 1] = 1
        maze[y - 1][x + 1] = 1
        print("wall forward")
    
    if not data[wb[yaw]]:
        maze[y + 1][x] = 1
        maze[y + 1][x + 1] = 1
        maze[y + 1][x - 1] = 1
        print("wall backward")
    
    if not data[wl[yaw]]:
        maze[y][x - 1] = 1
        maze[y + 1][x - 1] = 1
        maze[y - 1][x - 1] = 1
        print("wall left")
    
    if not data[wr[yaw]]:
        maze[y][x + 1] = 1
        maze[y + 1][x + 1] = 1
        maze[y - 1][x + 1] = 1
        print("wall right")
    
    print()

def processing_maze_data(maze):
    result_maze = [[0]*16]*16
    result_maze = np.array(result_maze)
    for i in range(1, 32, 2):
        for j in range(1, 32, 2):
            dt = [maze[i-1][j], maze[i][j+1], maze[i+1][j], maze[i][j-1]]
            ri = int(i/2)
            rj = int(j/2)
            res = -1
            if (sum(dt) == 0):
                res = 0
            elif (sum(dt) == 1 and dt[3] == 1):
                res = 1
            elif (sum(dt) == 1 and dt[0] == 1):
                res = 2
            elif (sum(dt) == 1 and dt[1] == 1):
                res = 3
            elif (sum(dt) == 1 and dt[2] == 1):
                res = 4

            elif (sum(dt) == 2 and dt[2] == 1 and dt[3] == 1):
                res = 5
            elif (sum(dt) == 2 and dt[2] == 1 and dt[1] == 1):
                res = 6
            elif (sum(dt) == 2 and dt[0] == 1 and dt[1] == 1):
                res = 7
            elif (sum(dt) == 2 and dt[0] == 1 and dt[3] == 1):
                res = 8

            elif (sum(dt) == 2 and dt[3] == 1 and dt[1] == 1):
                res = 9
            elif (sum(dt) == 2 and dt[0] == 1 and dt[2] == 1):
                res = 10

            elif (sum(dt) == 3 and dt[3] == 0):
                res = 11
            elif (sum(dt) == 3 and dt[2] == 0):
                res = 12
            elif (sum(dt) == 3 and dt[1] == 0):
                res = 13
            elif (sum(dt) == 3 and dt[0] == 0):
                res = 14

            elif (sum(dt) == 4):
                res = 15

            result_maze[ri][rj] = res

    return result_maze
