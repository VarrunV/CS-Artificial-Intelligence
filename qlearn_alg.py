 #Q-Learning Algorithm

 # Implementation of the Q for MDPs.
 # The Q-values are represented as a Python dict Q[s,a],
 # which is a mapping from the state indices s=0..stateMax to
 # and actions a to the Q-values.


import random

from qlearnexamples import *
def bestActionFor(mdp, state, Q):
    list = []
    applicable_actions = []
    for a in mdp.applicableActions(state):
        values = Q.get((state, a))
        list.append(list)
        applicable_actions.append(a)
    return applicable_actions[list.index(max(list))]
    # valueOfBestAction gives the value of best action for 'state'


def valueOfBestAction(mdp, state, Q):
    max_action = bestActionFor(mdp, state, Q)
    return Q.get((state, max_action))

    # Returns a tuple (s2,r), where s2 is the successor state and r is
    # the reward that was obtained.

def execute(mdp, s, a):
    succ = mdp.successors(s, a)  # successor,probability,reward
    probs = []
    for tri in succ:
        probs.append(tri[1])
    random_st = random.choices(succ, probs)[0]
    return((random_st[0], random_st[2]))

# Qlearning returns the Q-value function after performing the given number of iterations

def Qlearning(mdp, gamma, lambd, iterations):

    # The Q-values are a real-valued dictionary Q[s,a] where s is a state and a is an action.

    state = 0  # Always start from state 0
    Q = dict()
    for state_num in range(mdp.stateMax + 1):  # Q INITIALIZATION
        for act in mdp.applicableActions(state_num):
            Q[(state_num, act)] = 0

    for _ in range(iterations):
        # bestActionFor(mdp, state, Q)
        act = random.choice(mdp.applicableActions(state_num))
        state_dash, r = execute(mdp, state, act)
        values = ((1 - lambd) * Q.get((state, act))) + (lambd * (r + gamma * valueOfBestAction(mdp, state_dash, Q)))
        Q[(state, act)] = values
        state = state_dash
    return Q

# makePolicy constructs a policy,  a mapping from state to actions,
# given a Q-value function as produced by Qlearning.


def makePolicy(mdp, Q):
    # A policy is an action-valued dictionary P[s] where s is a state
    probs = dict()
    values = dict()

    for (state_num, act) in Q:
        values = Q[(state_num, act)]
        if state_num in probs:
            if list[state_num] < values:
                probs[state_num] = act
                list[state_num] = values
        else:
            probs[state_num] = act
            list[state_num] = values
    return probs


# makeValues constructs the value function, a mapping from states to values,
# given a Q-value function as produced by Qlearning.

def makeValues(mdp, Q):
    # A value function is a real-valued dictionary V[s] where s is a state
    V = dict()
    probs = dict()
    for state_num in range(mdp.stateMax + 1):
        V.update({state_num: 0})

    for (state, action) in Q.keys():
        values = Q[(state, action)]
        if state in probs:
            if V[state] < values:
                probs[state] = action
                V[state] = values
        else:
            probs[state] = action
            V[state] = values
    print(V)
    return V
