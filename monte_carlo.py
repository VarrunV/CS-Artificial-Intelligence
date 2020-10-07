# Monte Carlo search: randomly choose actions

import random

def monteCarloTrial(player,state,stepsLeft):

  #Perform recursive Mote Carlo Trials, transitioning between states by randomly
  #choosing among available actions.

  #Performs at most stepsLeft moves, if stepsLeft = 0 or if there are no
  #applicable actions for `player` in `state`, it will return the state value.

  if stepsLeft==0:
    return state.value()
  actions = state.applicableActions(player)
  if not len(actions):
    return state.value()
  else:
   s = state.successor(player, random.choice(actions))
  return monteCarloTrial(-player + 1, s, stepsLeft - 1)

def monteCarloSearch(player,state,trials):

  #Repeated MC Trials to return avg value.

  sum = 0
  for x in range(0,trials):
    sum += monteCarloTrial(player,state,20)
  return sum / trials

# Game played alternating each player
# choosing best action

def executeWithMC(player,state,stepsLeft,trials):

  #Play game using MCS recursively printing state values
  #Function alternates between players.

  if stepsLeft==0:
    return
  state.show()
  if player==0:
    bestScore = float("inf") # Default score for minimizing player
  else:
    bestScore = 0-float("inf") # Default score for maximizing player
  actions = state.applicableActions(player)
  if actions==[]:
    return
  for action in actions:
    state0 = state.successor(player,action)
    v = monteCarloSearch(1-player,state0,trials)
    if player==1 and v > bestScore: # Maximizing player chooses highest score
      bestAction = action
      bestScore = v
    if player==0 and v < bestScore: # Minimizing player chooses lowest score
      bestAction = action
      bestScore = v
  state2 = state.successor(player,bestAction)
  executeWithMC(1-player,state2,stepsLeft-1,trials)
