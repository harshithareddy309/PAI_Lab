import heapq

MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def get_input(name):
    print(f"\nEnter the {name} state (use 0 for blank):")
    puzzle = []
    for i in range(3):
        puzzle.append(tuple(map(int, input(f"Row {i + 1}: ").split())))
    return tuple(puzzle)


def manhattan(state, goal):
    goal_pos = {}
    for i in range(3):
        for j in range(3):
            goal_pos[goal[i][j]] = (i, j)

    h = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                gx, gy = goal_pos[val]
                h += abs(i - gx) + abs(j - gy)
    return h


def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j


def get_neighbors(state):
    x, y = find_blank(state)
    neighbors = []

    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [list(row) for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(tuple(tuple(row) for row in new_state))

    return neighbors


def print_state(state):
    for row in state:
        print(row)
    print()


def a_star_verbose(start, goal):
    pq = []
    visited = set()
    g_cost = {start: 0}

    h_start = manhattan(start, goal)
    f_start = h_start
    heapq.heappush(pq, (f_start, 0, start))

    step = 0

    while pq:
        f, g, current = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        h = manhattan(current, goal)

        print(f"STEP {step}")
        print("Chosen because it has the lowest f(n)")
        print(f"g(n) = {g}, h(n) = {h}, f(n) = {f}")
        print_state(current)

        if current == goal:
            print("🎯 Goal state reached!")
            return

        print("Possible moves:")

        for neighbor in get_neighbors(current):
            if neighbor in visited:
                continue

            new_g = g + 1
            new_h = manhattan(neighbor, goal)
            new_f = new_g + new_h

            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                heapq.heappush(pq, (new_f, new_g, neighbor))

            print("Next state:")
            print_state(neighbor)
            print(f"g(n) = {new_g}, h(n) = {new_h}, f(n) = {new_f}")
            print("-" * 40)

        print("=" * 60)
        step += 1

    print("❌ No solution found.")


# -------- MAIN --------
initial_state = get_input("INITIAL")
goal_state = get_input("GOAL")

a_star_verbose(initial_state, goal_state)
