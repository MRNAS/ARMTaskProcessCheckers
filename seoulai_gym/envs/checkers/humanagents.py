"""
Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
Modified by Manuel Retana. mretana@nevada.unr.edu
2020
"""
from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Tuple
from typing import Dict
from typing import Optional
import random

from seoulai_gym.envs.checkers.base import Constants
from seoulai_gym.envs.checkers.rules import Rules
from seoulai_gym.envs.checkers.utils import generate_random_move


class Agent(ABC, Constants, Rules):
    @abstractmethod
    def __init__(
        self,
        name: str,
        ptype: int,
    ):
        self._ptype = ptype
        self._name = name

    @abstractmethod
    def act(
        self,
        obs,
    ):
        pass

    @abstractmethod
    def consume(
        self,
        obs,
        reward: float,
        done: bool,
    ) -> None:
        pass

    @property
    def ptype(self):
        return self._ptype

    @ptype.setter
    def ptype(self, _ptype):
        if _ptype == self.DARK or _ptype == self.LIGHT:
            return _ptype
        else:
            raise ValueError("Invalid piece type.")

    @property
    def name(self):
        if self.ptype == self.DARK:
            return f"DARK {self._name}"
        elif self.ptype == self.LIGHT:
            return f"LIGHT {self._name}"

    def __str__(self):
        return self._name


class Agent(Agent):
    def __init__(
        self,
        ptype: int,
    ):
        """Initialize random agent.

        Args:
            name: name of agent.
            ptype: type of piece that agent is responsible for.
        """
        if ptype == Constants().DARK:
            name = "HumanDark"
        elif ptype == Constants().LIGHT:
            name = "HumanLight"
        else:
            raise ValueError

        super().__init__(name, ptype)

    def act(
        self,
        board: List[List],
        flag,
        humanflag
    ) -> Tuple[int, int, int, int]:
        """
        Choose a piece and its possible moves randomly.
        Pieces and moves are chosen from all current valid possibilities.

        Args:
            board: information about positions of pieces.

        Returns:
            Current and new location of piece.
        """
        #Decision between DP human and Random Human 50 % optimality
        #this could be edited to adjust levels of optimality
        decision = random.choice([0,1])
        if decision <0.5:
            print("random move human")
            rand_from_row, rand_from_col, rand_to_row, rand_to_col = generate_random_move(
                board,
                self.ptype,
                len(board),
            )
        else:
            print("DP move human")    
            rand_from_row, rand_from_col, rand_to_row, rand_to_col = generate_dynamic_move(
                board,
                self.ptype,
                len(board),
                flag,
                humanflag,
            )
        return rand_from_row, rand_from_col, rand_to_row, rand_to_col

    def consume(
        self,
        obs: List[List],
        reward: float,
        done: bool,
    ) -> None:
        """Agent processes information returned by environment based on agent's latest action.
        Random agent does not need `reward` or `done` variables, but this method is called anyway
        when used with other agents.

        Args:
            board: information about positions of pieces.
            reward: reward for perfomed step.
            done: information about end of game.
        """
        pass


class HumanLight(Agent):
    def __init__(
        self,
    ):
        super().__init__(Constants().LIGHT)


class HumanDark(Agent):
    def __init__(
        self,
    ):
        super().__init__(Constants().DARK)

#this class is used by the search algorithm to define search nodes consisting
#of the state of the node, the action taken to reach the node, and its parent
#node
class SearchNode:
    def __init__(self, action, state, parent):
        self.state = state
        self.action = action
        self.parent = parent
        
    #this method determines the path taken to reach the particular node
    def path(self):
        if self.parent == None:
            return [(self.action, self.state)]
        else:
            return self.parent.path() + [(self.action, self.state)]

    #this method determines whether a node with state s is anywhere in the
    #path of the particular node
    def inPath(self, s):
        if s == self.state:
            return True
        elif self.parent == None:
            return False
        else:
            return self.parent.inPath(s)

#this class is used by a depth-first search algorithm to construct a stack
#(last in, first out)
class Stack:
    def __init__(self):
        self.data = []
    def push(self, item):
        self.data.append(item)
    def pop(self):
        return self.data.pop()
    def isEmpty(self):
        return self.data == []

#this class is used by a breadth-first search algorithm to construct a queue
#(first in, first out)
class Queue:
    def __init__(self):
        self.data = []
    def push(self, item):
        self.data.append(item)
    def pop(self):
        return self.data.pop(0)
    def isEmpty(self):
        return self.data == []

#this general search algorithm takes as input an initial state, a 
#goalTest function for determining if the goal state has been reached, a list
#of possible actions, a successor function for determining what node will be
#reached when performing a particular action, a variable for switching between
#breadth-first and depth-first search, a variable for switching dynamic
#programming on and off, and a variable for determining the maximum number of
#nodes that can be constructed
def search(initialState, goalTest, actions, successor, depthFirst = False, \
           DP = True, maxNodes = 10000):
    if depthFirst:
        agenda = Stack()
    else:
        agenda = Queue()

    #the starting node has no parent and wasn't reached via an action
    startNode = SearchNode(None, initialState, None)
    if goalTest(initialState):
        return startNode.path()
    agenda.push(startNode)
    #with dynamic programming turned on, we ignore paths to states that have
    #already been visited via another path
    if DP: visited = {initialState: True}
    #count is used to make sure the maximum number of nodes isn't breached
    count = 1
    while not agenda.isEmpty() and maxNodes > count:
        #parent is the next node on the agenda to be expanded via possible
        #actions
        parent = agenda.pop()
        newStates = []
        #here we loop through the available actions, determining the resulting
        #state and resulting node
        for a in actions:
            newS = successor(parent.state, a)
            newN = SearchNode(a, newS, parent)
            #if we've reached our goal via this action, the path to it is
            #returned
            if goalTest(newS):
                return newN.path()
            #if the new state is one we can already reach via another action,
            #we ignore this action
            elif newS in newStates:
                pass
            #if the new state is already in the current path or if DP is on
            #and the new state has already been visited on some path, we ignore
            #this action
            elif ((not DP) and parent.inPath(newS)) or (DP and newS in visited):
                pass
            #otherwise we add the resulting node to the agenda of nodes to be
            #expanded
            else:
                count += 1
                if DP: visited[newS] = True
                newStates.append(newS)
                agenda.push(newN)
    return None




#standard class definition for general state machine
class SM:
    #particular machines are initialized with a startState, which this method
    #sets the machine's state to
    def start(self):
        self.state = self.startState
        
    #uses machine's getNextValues method to update the state on input inp and 
    #return output
    def step(self, inp):
        (s, o) = self.getNextValues(self.state, inp)
        self.state = s
        return o
    
    #some machines include a done method, which returns True when the machine 
    #is finished; here the default method always returns False
    def done(self, state):
        return False
    
    #this method runs the machine (from its start state) on a list of inputs, 
    #until the machine reaches its done state (if ever), returning the list of
    #outputs
    def transduce(self, inputs):
        self.start()
        return [self.step(inp) for inp in inputs if not self.done(self.state)]
    
    #this method runs the machine on n inputs of None, returning the list of 
    #outputs
    def run(self, n = 10):
        return self.transduce([None] * n)
    
    #the default startState is None
    startState = None
    
    #the default getNextValues method uses the machine's getNextState method, 
    #which is useful for defining machines whose next state and output are 
    #identical
    def getNextValues(self, state, inp):
        nextState = self.getNextState(state, inp)
        return (nextState, nextState)



#here we convert the search algorithm into an algorithm that runs on state
#machines, searching for the shortest sequence of legal inputs from the initial
#state of the machine to its goal state (determined by the machine's done
#method)
def smSearch(smToSearch, initialState = None, goalTest = None, maxNodes \
             = 10000, depthFirst = False, DP = True,):
    if initialState == None:
        initialState = smToSearch.startState
    if goalTest == None:
        goalTest = smToSearch.done
    return search(initialState, goalTest, smToSearch.legalInputs, \
                  lambda s, a: smToSearch.getNextValues(s, a)[0], \
                  maxNodes = maxNodes, depthFirst = depthFirst, DP = DP)

#here we define a state machine that takes a legal chess move for a knight as
#input and outputs the resulting position of the knight, where the goal is to
#reach the top-right position of the chessboard (see README for details)
class KnightMoves(SM):
    global x
    global y
    # x=eval(input("What is the goal x position  coordinate?4"))
    # y=eval(input("What is the goal y position  coordinate?1"))
    # print(SM)
    legalInputs = ['ul', 'ur', 'dl', 'dr'] #checkers
    def __init__(self, s, flag):
        self.startState = s
        self.flag = flag
        # print(self.flag)

    def getNextValues(self, state, inp):
        if inp == 'ul' and state[0] > 0 and state[1] < 6:
            nextState = (state[0] - 1, state[1] + 1)
            # print((1))
            return (nextState, nextState)
        elif inp == 'ur' and state[0] < 7 and state[1] > 1:
            nextState = (state[0] + 1, state[1] - 1)
            # print((2))
            return (nextState, nextState)
        elif inp == 'dl' and state[0] > 0 and state[1] > 1:
            nextState = (state[0] - 1, state[1] - 1)
            # print((3))
            return (nextState, nextState)
        elif inp == 'dr' and state[0] < 7 and state[1] < 6:
            nextState = (state[0] + 1, state[1] + 1)
            # print((4))
            return (nextState, nextState)
        else:
            # print((5))
            return (state, state)

    def done(self, state):
        flag = self.flag
        # print(flag, "flag in DP")
        if flag == True:
            # print("human seeking 6,3")
            # White Goal
            x = 6
            y = 3
        else:
            # print("human seeking 6,3")
            # Black Goal
            x = 6  
            y = 3
        goal=()
        goal=(x,y)
        return state == goal #goal state

def generate_dynamic_move(board: List[List],ptype: int,board_size: int,flag,humanflag,)-> Dict[Tuple[int, int], List[Tuple[int, int]]]:
    """Generate dynamic programming move from all `ptype` valid moves but does not execute it.

    Args:
    board: (List[List[Piece]]) State of the game.
    ptype: (int) type of piece for which random move will be generated
    board_size: (int) size of board
    """
    valid_moves = Rules.generate_valid_moves(board, ptype, board_size)
    #chooses random piece from pieces available
    dyn_from_row, dyn_from_col = random.choice(list(valid_moves.keys()))
    
    print('starting x:',dyn_from_row)
    print('starting y:',dyn_from_col)
 
    knight = smSearch(KnightMoves((dyn_from_row,dyn_from_col),flag)) #current position
    print(knight, "human")
    print(valid_moves, "valid moves for human")
    next_move=knight[1][1]
    dyn_to_row = next_move[0]
    dyn_to_col = next_move[1]
    #if next move is invalid move randomly
    validlist = valid_moves[(dyn_from_row, dyn_from_col)]
    print("valid list:",validlist)
    for i in range(len(validlist)):
        if (dyn_to_row,dyn_to_col) == validlist[i]:
            print("valid move within DP guidelines")
            return dyn_from_row, dyn_from_col, dyn_to_row, dyn_to_col #new position
        elif i == len(validlist):
            #if piece will eat the other piece move randomly even if DP agent
            print("DP move about to eat other piece so valid random move")
            dyn_to_row, dyn_to_col = random.choice(valid_moves[(dyn_from_row, dyn_from_col)])
            return dyn_from_row, dyn_from_col, dyn_to_row, dyn_to_col

    
    