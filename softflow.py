from search import *
from copy import deepcopy

#################
# Problem class #
#################


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

    def actions(self, state):
        actions = []
        letters, number = self.process_grid(state.grid, state.nbc, state.nbr)
        for l in letters:
            i, j = letters[l]
            # move up
            if i > 0 and state.grid[i-1][j] == ' ':
                actions.append((l, 'up'))
            # move down
            if i < state.nbr-1 and state.grid[i+1][j] == ' ':
                actions.append((l, 'down'))
            # move left
            if j > 0 and state.grid[i][j-1] == ' ':
                actions.append((l, 'left'))
            # move right
            if j < state.nbc-1 and state.grid[i][j+1] == ' ':
                actions.append((l, 'right'))
        return actions

    # will try only with state if works
    def result(self, state, action):
        new_state = deepcopy(state)
        letters, number = self.process_grid(
            new_state.grid, new_state.nbc, new_state.nbr)
        l_to_n = self.dic_l_n(letters, number)  # letter to number converter

        l, d = action       # l = letter, d = direction
        i, j = letters[l]   # position of the letter

        if d == 'up':
            new_state.grid[i][j] = l_to_n[l]
            new_state.grid[i-1][j] = l
        elif d == 'down':
            new_state.grid[i][j] = l_to_n[l]
            new_state.grid[i+1][j] = l
        elif d == 'left':
            new_state.grid[i][j] = l_to_n[l]
            new_state.grid[i][j-1] = l
        elif d == 'right':
            new_state.grid[i][j] = l_to_n[l]
            new_state.grid[i][j+1] = l
        print(new_state)
        return new_state

    def goal_test(self, state):
        letters, number = self.process_grid(state.grid, state.nbc, state.nbr)
        l_posi = list(letters.values())
        n_posi = list(number.values())
        return l_posi == n_posi

    def h(self, node):
        h = 0.0
        letters, number = self.process_grid(node.state.grid, node.state.nbc, node.state.nbr)
        l_to_n = self.dic_l_n(letters, number)
        n_to_l = self.dic_n_l(number, letters)
        # using manhattan distance
        for l in letters:
            x1, y1 = letters[l]
            n = l_to_n[l]
            x2, y2 = number[n]
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

node = astar_search(problem)
# example of print
path = node.path()
print('Number of moves: ', str(node.depth))
for n in path:
    # assuming that the _str_ function of state outputs the correct format
    print(n.state)
    print()
