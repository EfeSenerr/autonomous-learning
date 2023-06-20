def detect_wall(maze, current_position, direction):
    x, y = current_position
    if direction == 'up':
        return maze[x][y + 1] == 0
    elif direction == 'down':
        return maze[x][y - 1] == 0
    elif direction == 'left':
        return maze[x + 1][y] == 0
    else:  # direction == 'right'
        return maze[x - 1][y] == 0

def drive_forward(maze, current_position, direction, result): # or go_forward
    x, y = current_position
    if direction == 'up' and not detect_wall(maze, current_position, 'up'):
        current_position = (x, y + 1)
        result.append(current_position)
    elif direction == 'down' and not detect_wall(maze, current_position, 'down'):
        current_position = (x, y - 1)
        result.append(current_position)
    elif direction == 'left' and not detect_wall(maze, current_position, 'left'):
        current_position = (x + 1, y)
        result.append(current_position)
    elif direction == 'right' and not detect_wall(maze, current_position, 'right'): 
        current_position = (x - 1, y)
        result.append(current_position)
    return current_position

def turn_left(direction):
    if direction == 'up':
        return 'left'
    elif direction == 'down':
        return 'right'
    elif direction == 'left':
        return 'down'
    else:  # direction == 'right'
        return 'up'

def turn_right(direction):
    if direction == 'up':
        return 'right'
    elif direction == 'down':
        return 'left'
    elif direction == 'left':
        return 'up'
    else:  # direction == 'right'
        return 'down'

def shortest_path(maze, start, end):
    parent = {}
    maze = maze[0]['map']
    rows, cols = len(maze), len(maze[0])
    queue = [start]
    visited = [[0]*cols for _ in range(rows)]  # 2D list to keep track of visited cells
    visited[start[0]][start[1]] = 1  # Mark the start cell as visited

    while queue:
        x, y = queue.pop(0)

        if (x, y) == end:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parent[(x, y)]
            path.append(start)
            return path[::-1]

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1 and visited[nx][ny] == 0:
                visited[nx][ny] = 1  # Mark the cell as visited
                queue.append((nx, ny))
                parent[(nx, ny)] = (x, y)


def judge_path(maze, start, end, path_taken):
    
    shortest = shortest_path(maze, start, end)

    if shortest is None:
        return "No path found."
    elif len(shortest) < len(path_taken):
        return f"You could have taken a {len(path_taken)-len(shortest)} steps shorter path! Do you want to try again?"
    elif len(shortest) == len(path_taken):
        return "You have taken the optimal path!! Amazing, you are doing great!"
    else:
        return "You took a shorter path than the shortest path! Wow?!?!"
