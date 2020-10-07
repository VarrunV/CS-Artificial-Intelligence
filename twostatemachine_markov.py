#Markov process- Machine with two states

import mdp
from enum import Enum

class TwoStateMachine(mdp.MDP):

#Markov Process with two states and two actions

    Actions = Enum("Actions", "stand walk")
    States = Enum("States", "upright prone")

    def __init__(self):
        # self._rewards is a dictionary mapping from a triplet of (state, action, state)
        # to a reward.
        self._rewards = {
            # Encodes the reward (0) of arc upright -> prone by action walk.
            #Rewards encoded in dictionary
            (TwoStateMachine.States.upright,
             TwoStateMachine.Actions.walk,
             TwoStateMachine.States.prone): 0,

            (TwoStateMachine.States.upright,
             TwoStateMachine.Actions.walk,
             TwoStateMachine.States.upright): 20,
            (TwoStateMachine.States.prone,
             TwoStateMachine.Actions.stand,
             TwoStateMachine.States.upright): 0,
        }

        # Likewise self._probs is a dictionary from (state,action,state) to a probability.
        self._probs = {
            #Encode the probabilities described in TwoStateMachine.pdf as (state, action, state) : probability

            (TwoStateMachine.States.upright,
             TwoStateMachine.Actions.walk,
             TwoStateMachine.States.prone): 0.1,
            (TwoStateMachine.States.upright,
             TwoStateMachine.Actions.walk,
             TwoStateMachine.States.upright): 0.9,
            (TwoStateMachine.States.prone,
             TwoStateMachine.Actions.stand,
             TwoStateMachine.States.upright): 1,
        }

    def R(self, s1, a, s2):
        #Get reward
        return self._rewards[(s1, a, s2)]

    def P(self, s1, a, s2):
        #Get probability
        return self._probs[(s1, a, s2)]

    def applicable_actions(self, s):

        aa = []
        for s2 in TwoStateMachine.States:
            for a in TwoStateMachine.Actions:
                if (s, a, s2) in self._rewards:
                    aa.append(a)

        return set(aa)

    def successor_states(self, s, a):

        #Get states reachable from state s using action a.

        # A successor state of s given action a is any state which can be
        # reached from s using action a.

        ss = []
        #Update the list ss with all successor states to state s

        for k in self._probs.keys():
            start, act, end = k
            if start == s and act == a:
                ss.append(end)

        return set(ss)

    def states(self):

        return set(self.States)

    def analytic(self, gamma):

        #Compute solution using analytic formula.
        # Calculate values
        p11 = self._probs[(TwoStateMachine.States.upright,
                           TwoStateMachine.Actions.walk,
                           TwoStateMachine.States.upright)]
        r11 = self._rewards[(TwoStateMachine.States.upright,
                             TwoStateMachine.Actions.walk,
                             TwoStateMachine.States.upright)]
        p12 = self._probs[(TwoStateMachine.States.upright,
                           TwoStateMachine.Actions.walk,
                           TwoStateMachine.States.prone)]
        v1 = p11 * r11 / (p11 * gamma - p12 * gamma * gamma)
        v2 = gamma * v1
        # Create a dictionary with value in each of the two possible states.
        return {TwoStateMachine.States.upright: v1,
                TwoStateMachine.States.prone: v2}
