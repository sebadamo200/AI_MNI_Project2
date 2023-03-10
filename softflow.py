from search import *
from copy import deepcopy
import time

#################
# Problem class #
#################

dic_let_to_num = {'a': '0', 'b': '1', 'c': '2', 'd': '3',
                  'e': '4', 'f': '5', 'g': '6', 'h': '7', 'i': '8', 'j': '9'}


class SoftFlow(Problem):

    def process_grid(self, grid, nbc, nbr):
        letters = {}
        number = {}
        for i in range(nbr):
            for j in range(nbc):
                if grid[i][j] != '#' and grid[i][j] != ' ':
                    # if it's a letter a to j
                    if ord(grid[i][j]) >= 97 and ord(grid[i][j]) <= 106:
                        letters[grid[i][j]] = (i, j)
                    # if it's a box 0 to 9
                    elif ord(grid[i][j]) >= 48 and ord(grid[i][j]) <= 57:
                        number[grid[i][j]] = (i, j)
        dict(sorted(letters.items()))
        dict(sorted(number.items()))
        return letters, number

    def process_grid_letters(self, grid, nbc, nbr):
        letters = {}
        for i in range(nbr):
            for j in range(nbc):
                if grid[i][j] != '#' and grid[i][j] != ' ':
                    # if it's a letter a to j
                    if ord(grid[i][j]) >= 97 and ord(grid[i][j]) <= 106:
                        letters[grid[i][j]] = (i, j)
        dict(sorted(letters.items()))
        return letters

    # this is for finding the key of letter to value of number
    # ex: a -> 0 something like converter
    def dic_l_n(self, letters, number):
        list_l = list(letters.keys())
        list_n = list(number.keys())
        return dict(zip(list_l, list_n))

    # this is for finding the key of number to value of letter
    # ex: 0 -> a something like converter
    def dic_n_l(self, number, letters):
        list_l = list(letters.keys())
        list_n = list(number.keys())
        return dict(zip(list_n, list_l))

    def __init__(self, initial):
        self.initial = initial
        l, n = self.process_grid(
            self.initial.grid, self.initial.nbc, self.initial.nbr)
        self.goal = n

    def actions(self, state):
        actions = []
        letters = self.process_grid_letters(state.grid, state.nbc, state.nbr)
        for l in letters:
            i, j = letters[l]
            # move up
            if i > 0 and state.grid[i-1][j] == ' ':
                actions.append(((i, j), (i-1, j)))
            # move down
            if i < state.nbr-1 and state.grid[i+1][j] == ' ':
                actions.append(((i, j), (i+1, j)))
            # move left
            if j > 0 and state.grid[i][j-1] == ' ':
                actions.append(((i, j), (i, j-1)))
            # move right
            if j < state.nbc-1 and state.grid[i][j+1] == ' ':
                actions.append(((i, j), (i, j+1)))
        return actions

    # will try only with state if works
    def result(self, state, action):
        new_state = deepcopy(state)
        # get letter
        letter = new_state.grid[action[0][0]][action[0][1]]
        # position of letter
        i, j = action[0]
        # next position of letter
        i1, j1 = action[1]

        # move letter
        new_state.grid[i][j] = dic_let_to_num[letter]
        new_state.grid[i1][j1] = letter

        # Distance Manhattan
        num = dic_let_to_num[letter]
        num_i, num_j = self.goal[num]
        Distance = abs(i1 - num_i) + abs(j1 - num_j)
        if Distance <= 1:
            new_state.grid[i1][j1] = dic_let_to_num[letter]
        return new_state

    def goal_test(self, state):
        letters, number = self.process_grid(state.grid, state.nbc, state.nbr)
        C = len(letters.keys()) == 0
        return C

    def h(self, node):
        h = 0.0
        letters = self.process_grid_letters(
            node.state.grid, node.state.nbc, node.state.nbr)
        # using manhattan distance
        for l in letters:
            x1, y1 = letters[l]
            n = dic_let_to_num[l]
            # position of number from goal
            x2, y2 = self.goal[n]
            h += abs(x1-x2) + abs(y1-y2)
        return h

    def load(path):
        with open(path, 'r') as f:
            lines = f.readlines()

        state = State.from_string(''.join(lines))
        return SoftFlow(state)


###############
# State class #
###############

class State:

    def __init__(self, grid):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def __eq__(self, other_state):
        return hash(str(self)) == hash(str(other_state))

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        return hash(str(self)) < hash(str(other))

    def from_string(string):
        lines = string.strip().splitlines()
        return State(list(
            map(lambda x: list(x.strip()), lines)
        ))


#####################
# Launch the search #
#####################
problem = SoftFlow.load(sys.argv[1])
start_time = time.time()
node = astar_search(problem)
end_time = time.time()
# example of print
path = node.path()
print('Number of moves: ', str(node.depth))
for n in path:
    # assuming that the _str_ function of state outputs the correct format
    print(n.state)
    print()

print('Time: ', str(end_time - start_time))
