#value iteration algorithm on markov descision processes




def value_of(mdp, s, a, v, gamma):

#Implementation of function computing sum and return a float


    successor = mdp.successor_states(s, a)
    value = 0
    for ss in successor:
        value += mdp.P(s, a, ss) * (mdp.R(s, a, ss) + gamma * v[ss])
    return value


def value_iteration(mdp, gamma, epsilon=0.001):

# Performing value iteration of Markov Descision Process MDP.


    limit = (epsilon * (1 - gamma)) / (2 * gamma)
    states = mdp.states()
    diff = {}
    values_n = dict(zip(states, [0, ] * len(states)))
    values_n1 = dict(zip(states, [0, ] * len(states)))
    while True:
        for s in states:
            tmp = []
            for a in mdp.applicable_actions(s):
                tmp.append(value_of(mdp, s, a, values_n, gamma))
            values_n1[s] = max(tmp)
            diff[s] = abs(values_n1[s] - values_n[s])
        values_n = values_n1.copy()
        if diff[argmax(diff)] < limit:
            break
    return values_n1


def argmax(d):

#Return key corresponding to maximum value in dictionary `d`

    return max(d, key=lambda k: d[k])


def make_policy(mdp, optimal_values, gamma):

#Compute policy given optimal values for all states.

    return {s1: argmax({a: value_of(mdp, s1, a, optimal_values, gamma)
                        for a in mdp.applicable_actions(s1)})
            for s1 in mdp.states()}


if __name__ == "__main__":
    # Very basic examples.
    #
    # For more and tests with automatic compariason run test_valueiteration.py

    from gridmdp import GridMDP

    print("--- Example 1 ------------------")
    # A grid with two walls (#), one positive reward (+)
    # and one negative (-). (.) denotes neutral (0.0).
    gdp = GridMDP([".+.",
                   "-.#",
                   "#.."])

    print("Input GridMDP:")
    print(gdp)

    gamma = 0.8
    epsilon = 0.01
    v = value_iteration(gdp, gamma, epsilon)
    pi = make_policy(gdp, v, gamma)

    print("Computed values and policy")
    for s in sorted(gdp.states()):
        print("Location: {0} \t | Value: {1} \t | Policy: {2}".format(s, v[s], pi[s]))
    print(
        """
CORRECT VALUES (Policy may differ if multiple actions has the same value)
Location: (0, 0)         | Value: 2.166637350797169      | Policy: East
Location: (0, 1)         | Value: 1.8238205241911116     | Policy: East
Location: (0, 2)         | Value: 2.29341219866735       | Policy: West
Location: (1, 0)         | Value: 1.5860931388905264     | Policy: North
Location: (1, 1)         | Value: 2.1666373507971692     | Policy: North
Location: (2, 1)         | Value: 2.29341219866735       | Policy: South
Location: (2, 2)         | Value: 1.7940038893976213     | Policy: South
""")
    print("--- Example 2 ------------------")
    gdp = GridMDP(["...+",
                   ".#.-",
                   "...."])
    print("Input GridMDP:")
    print(gdp)
    gamma = 0.8
    epsilon = 0.01
    v = value_iteration(gdp, gamma, epsilon)
    pi = make_policy(gdp, v, gamma)
    print("Computed values and policy")
    for s in sorted(gdp.states()):
        print("Location: {0} \t | Value: {1} \t | Policy: {2}".format(s, v[s], pi[s]))
    print(
        """
CORRECT VALUES (Policy may differ if multiple actions has the same value)
Location: (0, 0)         | Value: 2.1870595721840265     | Policy: West
Location: (0, 1)         | Value: 1.6360669646671202     | Policy: East
Location: (0, 2)         | Value: 2.1870595721840265     | Policy: East
Location: (0, 3)         | Value: 1.7541002681521682     | Policy: North
Location: (1, 0)         | Value: 1.601186507019843      | Policy: North
Location: (1, 2)         | Value: 1.601186507019843      | Policy: North
Location: (1, 3)         | Value: 2.1785706078376768     | Policy: North
Location: (2, 0)         | Value: 1.7072985613492146     | Policy: West
Location: (2, 1)         | Value: 1.329565025014288      | Policy: East
Location: (2, 2)         | Value: 1.7072985613492149     | Policy: East
Location: (2, 3)         | Value: 2.195548536530376      | Policy: South
""")

    print("--- Example 3 ------------------")
    print("Example using a basic two-state machine.")

    from twostatemachine import TwoStateMachine

    tsm = TwoStateMachine()
    gamma = 0.5
    epsilon = 0.01
    vi = value_iteration(tsm, gamma, epsilon)
    va = tsm.analytic(gamma)
    print("""(using gamma = {0}, epsilon = {1})

Iterated values
---------------
upright: {2}
prone  : {3}

Theoretical values
------------------
upright: {4}
prone  : {5}

""".format(gamma, epsilon,
           vi[TwoStateMachine.States.upright],
           vi[TwoStateMachine.States.prone],
           va[TwoStateMachine.States.upright],
           va[TwoStateMachine.States.prone]
           ))
