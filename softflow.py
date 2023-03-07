from search import *

#################
# Problem class #
#################


class SoftFlow(Problem):

    def __init__(self, initial):
        self.initial = initial  # in string format
        self.grid = initial.grid  # in list format
        self.nbr = initial.nbr  # number of rows
        self.nbc = initial.nbc  # number of columns
        self.letters = {}  # letters positions
        self.number = {}  # number positions
        for i in range(self.nbr):
            for j in range(self.nbc):
                if self.grid[i][j] != '#' and self.grid[i][j] != ' ':
                    # if it's a letter a to j
                    if ord(self.grid[i][j]) >= 97 and ord(self.grid[i][j]) <= 106:
                        self.letters[self.grid[i][j]] = (i, j)
                    # if it's a box 0 to 9
                    elif ord(self.grid[i][j]) >= 48 and ord(self.grid[i][j]) <= 57:
                        self.number[self.grid[i][j]] = (i, j)
        self.letters = dict(sorted(self.letters.items()))
        self.number = dict(sorted(self.number.items()))
        # not so important for the moment
        self.number_of_cables = len(self.letters)

    def actions(self, state):
        actions = []
        # for each letter can move up, down, left or right if not # otherwise nothing
        for l in self.letters:
            i, j = self.letters[l]
            # move up
            if i > 0 and self.grid[i-1][j] == ' ':
                actions.append((l, 'up'))
            # move down
            if i < self.nbr-1 and self.grid[i+1][j] == ' ':
                actions.append((l, 'down'))
            # move left
            if j > 0 and self.grid[i][j-1] == ' ':
                actions.append((l, 'left'))
            # move right
            if j < self.nbc-1 and self.grid[i][j+1] == ' ':
                actions.append((l, 'right'))
        return actions

    def result(self, state, action):
        # if action is taken i have to update position of the letter
        l, d = action
        i, j = self.letters[l]
        if d == 'up':
            self.letters[l] = (i-1,j)
        elif d == 'down':
            self.letters[l] = (i+1,j)
        elif d == 'left':
            self.letters[l] = (i,j-1)
        elif d == 'right':
            self.letters[l] = (i,j+1)
        input()
        pass

    def goal_test(self, state):
        # i think it could be better coded
        l_posi = [self.letters[l] for l in self.letters]
        n_posi = [self.number[n] for n in self.number]
        for i in range(len(l_posi)):
            if l_posi[i] != n_posi[i]:
                return False
        return True

    def h(self, node):
        h = 0.0
        l_posi = [self.letters[l] for l in self.letters]
        n_posi = [self.number[n] for n in self.number]
        for i in range(len(l_posi)):
            x1, y1 = l_posi[i]
            x2, y2 = n_posi[i]
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
input()
# example of print
path = node.path()
print('Number of moves: ', str(node.depth))
for n in path:
    # assuming that the _str_ function of state outputs the correct format
    print(n.state)
    print()
