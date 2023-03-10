from search import *
import time
import math

letters = "abcdefghij"
cables = "0123456789"
letterToInt = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
    "j": 9,
}

#################
# Problem class #
#################


def printGrid(grid):
    for line in grid:
        s = ""
        for e in line:
            s += e
        print(s)
    print()


def getPositionOfExtremities(grid):
    positions = [None for i in range(10)]
    for y, line in enumerate(grid):
        for x, letter in enumerate(line):
            if letter in letters:
                positions[letterToInt[letter]] = (x, y)
    return tuple(positions)


def intToLetter(v):
    return letters[int(v)]


class SoftFlow(Problem):

    def __init__(self, initial):
        self.initial = initial

        _ = [None for i in range(10)]
        for y, line in enumerate(initial[0]):
            for x, value in enumerate(line):
                if value in cables:
                    _[int(value)] = (x, y)
        # position des nnumeros au au debut
        self.goalPosition = _

    def getClosestGoal(self, extremities):
        minDistance = float("inf")
        minGoal = None

        for i, goalPos in enumerate(self.goalPosition):
            if extremities[i] == None:
                continue
            # find the corresponding letter position on the grid
            gX, gY = goalPos
            eX, eY = extremities[i]
            D = abs(gX - eX) + abs(gY - eY)
            if D < minDistance:
                minDistance = D
                minGoal = i

        return minGoal

    def actions(self, state):
        actions = []

        grid = state[0]
        extremities = state[1]

        for intR, extremitie in enumerate(extremities):
            if extremitie == None:
                continue
            x, y = extremitie
            nextPositions = [
                (x-1, y),
                (x+1, y),
                (x, y-1),
                (x, y+1)
            ]
            for nextPosition in nextPositions:
                nX, nY = nextPosition
                if grid[nY][nX] == " ":
                    # can move there!
                    actions.append((
                        (x, y),
                        (nX, nY),
                        intR
                    ))

        return actions

    def result(self, state, action):
        ACT, NEXT, INR = action
        grid, extremities = state

        newGrid = [list(l) for l in grid]  # to check
        newExtremities = list(extremities)

        aX, aY = ACT
        nX, nY = NEXT

        newGrid[aY][aX] = INR
        newGrid[nY][nX] = intToLetter(INR)
        newExtremities[INR] = (nX, nY)

        # Verify if cable connected to out
        gX, gY = self.goalPosition[INR]
        D = abs(nX-gX) + abs(nY-gY)  # manhattan bb

        if D <= 1:
            # we hit the selected goal
            newGrid[nY][nX] = INR
            newExtremities[INR] = None

            """
            minGoal = self.getClosestGoal(newExtremities)
            self.selectedGoal = minGoal

            if minGoal!=None:
                self.selectedGoalPosition = self.goalPosition[minGoal]
            else:
                # goal found
                pass
            """

        RES = (tuple([tuple([str(e) for e in l])
               for l in newGrid]), tuple(newExtremities))

        return RES

    def goal_test(self, state):
        for e in state[1]:
            if e != None:
                return False
        return True

    def h(self, node):
        h = 0

        grid, extremities = node.state
        for i, extremitie in enumerate(extremities):
            if extremitie == None:
                continue
            gX, gY = self.goalPosition[i]
            eX, eY = extremitie
            h += abs(eX-gX) + abs(eY-gY)

        return h

    def h_nn(self, node):

        if (self.selectedGoal == None):
            return -1

        goal = self.selectedGoal
        gX, gY = self.selectedGoalPosition
        eX, eY = self.goalPosition[goal]
        h = abs(gX-eX) + abs(gY-eY)
        return h

    def load(path):
        with open(path, 'r') as f:
            lines = f.readlines()

        grid = tuple([tuple(line.strip()) for line in lines])

        # getgetPositionOfExtremities position des lettres.
        state = (grid, getPositionOfExtremities(grid))
        print(state)
        input()
        return SoftFlow(state)

#####################
# Launch the search #
#####################


def main():
    problem = SoftFlow.load(sys.argv[1])

    start_time = time.time()

    node = astar_search(problem)
    end_time = time.time()

    # example of print
    path = node.path()

    print('Number of moves: ', str(node.depth))
    for n in path:
        # assuming that the _str_ function of state outputs the correct format
        printGrid(n.state[0])
        print()

    print("--- %s seconds ---" % (end_time - start_time))


main()
