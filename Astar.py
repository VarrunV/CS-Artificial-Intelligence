
#Implementation of A-star algorithm
#Returns a pair of (plan,cost)

import time
import queue
import itertools

DEBUG=False
#DEBUG=True

# A*

def ASTAR(initialstate,goaltest,h):
    if goaltest(initialstate):
        return (initialstate,0)
    g = dict() # dictionary for holding cost-so-far
    possible_states = dict()
    parent = dict()
    target_best = float('inf')
    target_best_goal = None

    g[initialstate] = 0

    q = queue.PriorityQueue()
    q.put( (g[initialstate]+h(initialstate), initialstate) )

    while not q.empty():
        f,state = q.get()
        if f>=target_best:
            # return the original path, along with the cost
            s=target_best_goal
            path = [s]
            while s!=initialstate:
                path.append(parent[s])
                s=parent[s]
            path.append(s)
            path.reverse()
            return (path,target_best)


        # if DEBUG:
        #     print("next popped state: ", state.show())
        possible_states[state] = 1
        for aname,s,cost in state.successors():
            if goaltest(s):
                target_best = min(target_best, g[state]+cost)
                target_best_goal = s
            if s not in possible_states:
                possible_states[s] = 1
                parent[s] = state
                assert(g.get(s,None)==None)
                g[s] = g[state]+cost
                q.put( (g[s]+h(s), s) )
    # print("all state possible_states")
