from random import sample

N, S, E, W, V = 1, 2, 4, 8, 16
opposite = {N:S, S:N, E:W, W:E}
move = {N: lambda x, y: (x, y-1),
        S: lambda x, y: (x, y+1),
        E: lambda x, y: (x+1, y),
        W: lambda x, y: (x-1, y)}
directions = lambda: sample((N, S, E, W), 4)

def maze_generation(width, height):
    maze = [[0] * width for i in range(height)]
    total_cells = width * height
    x, y = 0, 0

    while total_cells > 1:
        for direction in directions():
            nx, ny = move[direction](x, y)
            if not 0 <= nx < width or not 0 <= ny < height:
                continue
            elif maze[ny][nx] == 0:
                maze[y][x] |= direction
                maze[ny][nx] |= opposite[direction]
                x, y = nx, ny
                break

        else:
            for direction in directions():
                nx, ny = move[direction](x, y)
                if (not 0 <= nx < width
                 or not 0 <= ny < height
                 or not maze[ny][nx] & V == 0):
                    continue
                elif not maze[ny][nx] & opposite[direction] == 0:
                    maze[y][x] |= V
                    total_cells -= 1
                    x, y = nx, ny
                    break

    return maze

def draw_maze(maze):
    #print(maze)
    start = False
    finish = False
    width = len(maze[0])
    height = len(maze)
    with open('Maps/level_1.goose', 'w') as f:
        print('1' * (width*2+1), file=f)

        for i in range(height*2):
            line = ['1']
            for j in range(width*2):
                if i % 2 == 0 and j % 2 == 0:
                    if start == False:
                        line.append('3')
                        start = True
                    else:
                        line.append('0')

                elif i % 2 == 0 and j % 2 != 0:
                    if not maze[i//2][j//2] & E == 0:
                        line.append('0')

                    else:
                        line.append('1')
                elif i % 2 != 0 and j % 2 == 0:
                    if not maze[i//2][j//2] & S == 0:
                        #if finish == False and i>height*1.1 and j>width*1.1:
                            #line.append('2')
                           # finish = True
                        #else:
                        line.append('0')    
                    else:
                        line.append('1')
                else:
                    line.append('0')
            print(''.join(line),file=f)
        print('1'*12+'0'*2+'2', file=f)    

# Edit the values to change the height and width of the labyrinth
#draw_maze(maze_generation(8,6))