

# Implementation of the moves of knights on chess board

# The state consists of the locations of one or more
# knights. The possible moves of the knight in the cell (x,y) are
# to cells that add +1 or -1 to x and +2 or -2 to y, or that add
# +1 or -1 to y and +2 or -2 to x, and the resulting coordinates
# are within the 8 X 8 grid with coordinates 0..7 and 0..7.



import time
import queue


class KnightState:

    # Construct the canonical state, with knights' coordinates
    # ordered lexicographically.

    def canonize(self):
        self.occupied.sort(key=lambda t: t[0] * 1000 + t[1])

    # Creating a state:
    # initialLocations is a list of triples (x,y,b), where
    # (x,y) is the coordinates of a knight, and b is 'true'
    # iff the knight is black.

    def __init__(self, initialLocations):
        self.occupied = initialLocations
        self.canonize()

    # Construct a string representing a state.

    def __repr__(self):
        s = ""
        for x, y, b in self.occupied:
            if b:
                color = "B"
            else:
                color = "W"
            s = s + "(" + str(x) + "," + str(y) + "," + color + ")"
        return s

    # The hash function for states, mapping each state to an integer

    def __hash__(self):
        h = 0
        for x, y, b in self.occupied:
            h = 2 * (h * 64 + x + 8 * y) + b
        return h

    # Equality of states. Here we assume that 'canonize' has been
    # applied when creating each state.

    def __eq__(self, other):
        return (self.occupied == other.occupied)

    # All successor states w.r.t. a legal knight move




    def successors(self):
        positions = [[2, 1], [-2, 1], [-2, -1], [2, -1], [1, 2], [-1, 2], [-1, -2], [1, -2]]
        final = []
        for knight in self.occupied:
            for position in positions:
                temp_position = (position[0] + knight[0], knight[1] + position[1], knight[2])
                temp_position_not = (position[0] + knight[0], knight[1] + position[1], (not knight[2]))
                if 0 <= temp_position[0] <= 7 and 0 <= temp_position[1] <= 7:
                    if (temp_position not in self.occupied) and (temp_position_not not in self.occupied):
                        final.append(["new_state", KnightState([temp_position])])
        return final
# reaches a goal state.

DEBUG = False


def breadthFirstSearch(initialstate, goaltest):
    statExpansions = 0  # number of expanded states
    statVisits = 0  # number of encountered states

    starttime = time.process_time()

    visited = dict()  # dictionary (hash table) for holding visited states

    Q = queue.Queue(maxsize=0)  # first-in-first-out queue for breadth-first search

    print("Initial state is " + str(initialstate))
    Q.put((initialstate, []))  # Insert the initial state in the queue

    while not Q.empty():
        state, path = Q.get()  # Next un-expanded state from the queue
        if DEBUG:
            print("Expanding state " + str(state))
        statExpansions += 1
        for aname, s in state.successors():  # Go through all successors of state
            if s not in visited:  # Is state in the dictionary?
                if DEBUG:
                    print("New state " + str(s))
                statVisits += 1
                if goaltest(s):
                    print("Goal state " + str(s) + " reached")
                    endtime = time.process_time()
                    print(str(statExpansions) + " expansions, " + str(statVisits) + " visits")
                    print(path + [aname])
                    print("Elapsed time ", str(endtime - starttime))
                    print()
                    return
                visited[s] = 1
                Q.put((s, path + [aname]))
    print("All states visited")


# The following code runs the breadth-first search algorithm with
# different initial states and goal states.
# The goal states are represented by an unnamed function that
# returns 'true'if the given state is a goal state. All of
# the functions below have a unique goal state, so the test
# is simply whether the given state equals the goal state.
#
# The last two problem instances take a long time to compute,
# in the order of 1/2 hour or more. You might want to skip them.

# Swap the locations of two knights
#
# ........ ........
# ........ ........
# ........ ........
# ........ ........
# ........ ........
# ........ ........
# ........ ........
# WB...... BW......

breadthFirstSearch(KnightState([(0, 0, False), (0, 1, True)]),
                   lambda state: (state.occupied == [(0, 0, True), (0, 1, False)]))

# Move four knights in a 2 by 2 formation 2 steps diagonally
#
# ........ ........
# ........ ........
# ........ ........
# ........ ........
# ........ ..BB....
# ........ ..BB....
# BB...... ........
# BB...... ........

breadthFirstSearch(KnightState([(0, 0, True), (0, 1, True), (1, 0, True), (1, 1, True)]),
                   lambda state: (state.occupied == [(2, 2, True), (2, 3, True), (3, 2, True), (3, 3, True)]))

# Move five knights in a 3+2 formation 2 steps diagonally
#
# ........ ........
# ........ ........
# ........ ........
# ........ ........
# ........ ..BB....
# ........ ..BBB...
# BB...... ........
# BBB..... ........

print("This probably takes about 20 seconds to solve.\n")

breadthFirstSearch(KnightState([(0, 0, True), (0, 1, True), (0, 2, True), (1, 0, True), (1, 1, True)]),
                   lambda state: (state.occupied == [(2, 2, True), (2, 3, True), (2, 4, True), (3, 2, True),
                                                     (3, 3, True)]))

# Move six knights in a 3 by 2 formation 2 steps up and 1 step right
#
# ........ ........
# ........ ........
# ........ ........
# ........ ........
# ........ .BBB....
# ........ .BBB....
# BBB..... ........
# BBB..... ........

print("This probably takes about 5 seconds to solve.\n")

breadthFirstSearch(KnightState([(0, 0, True), (0, 1, True), (0, 2, True), (1, 0, True), (1, 1, True), (1, 2, True)]),
                   lambda state: (
                               state.occupied == [(2, 1, True), (2, 2, True), (2, 3, True), (3, 1, True), (3, 2, True),
                                                  (3, 3, True)]))

# Move six knights in a 3 by 2 formation 2 steps diagonally
#
# ........ ........
# ........ ........
# ........ ........
# ........ ........
# ........ ..BBB...
# ........ ..BBB...
# BBB..... ........
# BBB..... ........

print("This probably takes about one minute to solve.\n")

breadthFirstSearch(KnightState([(0, 0, True), (0, 1, True), (0, 2, True), (1, 0, True), (1, 1, True), (1, 2, True)]),
                   lambda state: (
                               state.occupied == [(2, 2, True), (2, 3, True), (2, 4, True), (3, 2, True), (3, 3, True),
                                                  (3, 4, True)]))

# Move six knights in a 3 by 2 formation 3 steps diagonally
#
# ........ ........
# ........ ........
# ........ ........
# ........ ...BBB..
# ........ ...BBB..
# ........ ........
# BBB..... ........
# BBB..... ........

# print("This will probably take more than 40 minutes to solve.\n")
#
# breadthFirstSearch(KnightState([(0,0,True),(0,1,True),(0,2,True),(1,0,True),(1,1,True),(1,2,True)]),
#                   lambda state: (state.occupied == [(3,3,True),(3,4,True),(3,5,True),(4,3,True),(4,4,True),(4,5,True)]))

# Move nine knights in a 3 by 3 formation 2 steps up and 1 step left
#
# ........ ........
# ........ ........
# ........ ........
# ........ .BBB....
# ........ .BBB....
# BBB..... .BBB....
# BBB..... ........
# BBB..... ........

# print("This will take more than 16 hours and over 200 of GB of memory to solve.\n")
#
# breadthFirstSearch(KnightState([(0,0,True),(0,1,True),(0,2,True),(1,0,True),(1,1,True),(1,2,True),(2,0,True),(2,1,True),(2,2,True)]),
#                   lambda state: (state.occupied == [(1,2,True),(2,2,True),(3,2,True),(1,3,True),(2,3,True),(3,3,True),(1,4,True),(2,4,True),(3,4,True)]))
