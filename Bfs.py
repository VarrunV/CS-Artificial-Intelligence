#Implementation of Breadth First Search algorithm

import time
import queue
import itertools

# Enable debugging output

DEBUG = False
#DEBUG = True

# Breadth-First Search (uninformed)

def breadthFirstSearch(initialstate,goaltest):
    statExpansions = 0 # number of expanded states
    statVisits = 0 # number of encountered states

    starttime = time.process_time()

    if(goaltest(initialstate)):
       print("Initial state is a goal state, terminating...")
       return

    visited = dict() # dictionary (hash table) for holding visited states
    predecessor = dict() # dictionary (hash table) for holding predecessors

    Q = queue.Queue(maxsize=0) # first-in-first-out queue

    print("BFS: Initial state is " + str(initialstate))
    Q.put( (initialstate,[]) ) # Insert the initial state in the queue
    visited[initialstate] = 1

    while not Q.empty():
        state,path = Q.get() # Next un-expanded state from the queue
        if DEBUG:
            print("Expanding state " + str(state))
        statExpansions += 1
        for aname,s,cost in state.successors(): # Go through all successors of state
            if s not in visited: # Is state in the dictionary?
                predecessor[s] = state
                if DEBUG:
                    print("New state " + str(s))
                statVisits += 1
                if goaltest(s):
                    print("Goal state " + str(s) + " reached")
                    endtime = time.process_time()
                    print(str(statExpansions) + " expansions, " + str(statVisits) + " visits " + str(len(path + [aname])) + " actions in solution path")
                    print(path + [aname])
                    print("Elapsed time ",str(endtime-starttime))
                    print()
                    return
                visited[s] = 1
                Q.put( (s,path + [aname] ) )
    print("All states visited")
