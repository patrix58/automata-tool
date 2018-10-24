from graphviz import Digraph
import copy
"""A class representing a finite automata.
"""
class Automata(object):
    def __init__(self, states, abc, start_states, end_states, transitions):
        # Init members
        self.states = states
        self.abc = abc
        self.start_states = start_states
        self.end_states = end_states
        self.transitions = transitions
        if not self.validate():
            raise RuntimeError('Automata: input error')
        
        # For bfs
        self.analyze_reachability_called = False
        self.analyze_productivity_called = False
        self.reachable = None
        self.productive = None

    
    def validate(self):
        # TODO validate the input
        return True

    def equivalent(self, other):
        # TODO check the equality of the automatas
        return True


    def recognizes(self, word):
        for state in self.start_states:
            if self._recognizes(word, state):
                return True
        return False


    def _recognizes(self, word, actual_state):
        if not word:
            return actual_state in self.end_states
        letter = word[0]
        filtered_transitions = filter(lambda tran: tran[0] == actual_state and tran[1] == letter, self.transitions)
        for fitting_transition in filtered_transitions:
            if self._recognizes(word[1:], fitting_transition[2]):
                return True
        return False 

    def analyze_reachability(self):
        if not self.analyze_reachability_called:
            self.analyze_reachability_called = True
            self.reachable = {state:False for state in self.states}
            for state in self.start_states:
                self._bfs_reachability(state)

    def _bfs_reachability(self, actual_state):
        if self.reachable[actual_state]:
            return
        self.reachable[actual_state] = True
        filtered_transitions = filter(lambda tran: tran[0] == actual_state, self.transitions)
        for transition in filtered_transitions:
            self._bfs_reachability(transition[2])

    def analyze_productivity(self):
        if not self.analyze_productivity_called:
            self.analyze_productivity_called = True
            self.productive = {state:False for state in self.states}
            for state in self.end_states:
                self._bfs_productivity(state)

    def _bfs_productivity(self, actual_state):
        if self.productive[actual_state]:
            return
        self.productive[actual_state] = True
        filtered_transitions = filter(lambda tran: tran[2] == actual_state, self.transitions)
        for transition in filtered_transitions:
            self._bfs_productivity(transition[0])
    
    def only_reachable(self):
        self.analyze_reachability()
        is_reachable = lambda state: self.reachable[state]
        at = Automata(
            list(filter(is_reachable, self.states)),
            copy.deepcopy(self.abc),
            list(filter(is_reachable, self.start_states)),
            list(filter(is_reachable, self.end_states)),
            list(filter(lambda tran: is_reachable(tran[0]) and is_reachable(tran[2]), self.transitions))
        )
        at.analyze_reachability_called = True
        at.reachable = {k:v for k, v in self.reachable.items() if v}
        return at

    def only_productive(self):
        self.analyze_productivity()
        is_productive = lambda state: self.productive[state]
        at = Automata(
            list(filter(is_productive, self.states)),
            copy.deepcopy(self.abc),
            list(filter(is_productive, self.start_states)),
            list(filter(is_productive, self.end_states)),
            list(filter(lambda tran: is_productive(tran[0]) and is_productive(tran[2]), self.transitions))
        )
        at.analyze_productivity_called = True
        at.productive = {k:v for k, v in self.productive.items() if v}
        return at

    def show(self):
        dot = Digraph()
        dot.attr(rankdir='LR')
        for start_state in self.start_states:
            inv_node_name = 's' + start_state
            dot.node(inv_node_name, style='invis')
            dot.edge(inv_node_name, start_state)
        for end_state in self.end_states:
            dot.node(end_state, end_state, shape='doublecircle')
        for state in self.states:
            dot.node(state, state)
        for transition in self.transitions:
            dot.edge(transition[0], transition[2], transition[1])
        return dot  

    # Operators

    def __eq__(self, other):
        return self.equivalent(other) 

    
