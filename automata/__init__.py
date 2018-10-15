

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

    # Operators

    def __eq__(self, other):
        return self.equivalent(other) 

    
