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

        self.keys_l = list(self.letters.keys())
        self.keys_n = list(self.number.keys())
        self.l_to_n = dict(zip(self.keys_l, self.keys_n))  # letters to number
        self.n_to_l = dict(zip(self.keys_n, self.keys_l))  # number to letters

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
            self.grid[i][j] = self.l_to_n[l]
            self.grid[i-1][j] = l
            self.letters[l] = (i-1, j)
        elif d == 'down':
            self.grid[i][j] = self.l_to_n[l]
            self.grid[i+1][j] = l
            self.letters[l] = (i+1, j)
        elif d == 'left':
            self.grid[i][j] = self.l_to_n[l]
            self.grid[i][j-1] = l
            self.letters[l] = (i, j-1)
        elif d == 'right':
            self.grid[i][j] = self.l_to_n[l]
            self.grid[i][j+1] = l
            self.letters[l] = (i, j+1)

        return State(self.grid)


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
        for l in self.letters:
            i, j = self.letters[l]
            x, y = self.number[self.l_to_n[l]]
            h += abs(i - x) + abs(j - y)
        return h

    def load(path):
        with open(path, 'r') as f:
            lines = f.readlines()

        state = State.from_string(''.join(lines))
        return SoftFlow(state)


#ICI IL Y A L'IDEE MAIS CA NE MARCHE PAS
