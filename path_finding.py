import numpy as np

maze = np.zeros((5, 5))
maze[1][0] = 1
maze[1][4] = 1
maze[2][2] = 1
maze[3][3] = 1
maze[4][3] = 1


class Env:
    def __init__(self, maze):
        self.maze = maze
        self.top = 0
        self.bottom = maze.shape[0] - 1
        self.left = 0
        self.right = maze.shape[1] - 1

    def reward(self, current, direction):
        if direction == 'up':
            if current[0] - 1 < self.top:
                return (current[0] - 1, current[1]), -100
            else:
                if maze[current[0] - 1][current[1]] == 1:
                    return (current[0] - 1, current[1]), -100
                return (current[0] - 1, current[1]), 10
        elif direction == 'right':
            if current[1] + 1 > self.right:
                return (current[0], current[1] + 1), -100
            else:
                if maze[current[0]][current[1] + 1] == 1:
                    return (current[0], current[1] + 1), -100
                else:
                    return (current[0], current[1] + 1), 10
        elif direction == 'left':
            if current[1] - 1 < self.left:
                return (current[0], current[1] - 1), -100
            else:
                if maze[current[0]][current[1] - 1] == 1:
                    return (current[0], current[1] - 1), -100
                else:
                    return (current[0], current[1] - 1), 10
        elif direction == 'down':
            if current[0] + 1 > self.bottom:
                return (current[0] + 1, current[1]), -100
            else:
                if maze[current[0] + 1][current[1]] == 1:
                    return (current[0] + 1, current[1]), -100
                else:
                    return (current[0] + 1, current[1]), 10


class State:
    def __init__(self, position, previous_state):
        self.position = position
        self.previous_state = previous_state
        self.next_states = []
        self.is_visited = False
        self.reward = 0

    def update_reward(self, reward):
        self.reward += reward

    def add_next_state(self, state):
        self.next_states.append(state)

    def update_location(self, state):
        to_update = list(filter(lambda a: a.position == state.position, self.next_states))[0]
        self.next_states.remove(to_update)
        to_update.is_visited = True
        self.next_states.append(to_update)


class Agent:
    def __init__(self, env, start_point, reward_point):
        self.env = env
        self.start_point = start_point
        self.reward_point = reward_point

    def move(self):
        done = False
        steps = ['up', 'down', 'right', 'left']
        current_state = State(self.start_point, None)
        iterations = 0
        visited_nodes = {current_state.position: 0}
        while not done:

            iterations += 1
            current_state.is_visited = True
            next_state_exists = False
            if len(current_state.next_states) == 0:
                for idx, step in enumerate(steps):
                    new_position, reward = self.env.reward(current_state.position, step)

                    if new_position == self.reward_point:
                        print(f'Go to {current_state.position} -> {new_position}')
                        print(f'Iterations = {iterations}')
                        print('Treasure found')
                        done = True
                        break

                    state = State(new_position, current_state)
                    try:
                        visited_nodes[new_position]
                    except:
                        visited_nodes[new_position] = current_state.reward + reward
                    state.update_reward(visited_nodes[new_position])
                    current_state.add_next_state(state)

            if not done:
                for idx, next_state in enumerate(current_state.next_states):
                    if next_state.reward >= current_state.reward and next_state.is_visited == False:
                        print(f'Go to {current_state.position} -> {next_state.position}')
                        current_state = next_state
                        next_state_exists = True
                        break

                if next_state_exists:
                    continue

                if current_state.previous_state.is_visited:
                    print(f'Back {current_state.position} -> {current_state.previous_state.position}')
                    current_state.previous_state.update_location(current_state)
                    current_state = current_state.previous_state


env = Env(maze)
start_point = (4, 2)
reward_point = (4, 0)
agent = Agent(env, start_point, reward_point)
print(env.maze)
agent.move()
