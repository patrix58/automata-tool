

"""A class representing a finite automata.
"""
class Automata(object):
    def __init__(self, states, start_states, end_states, transitions):
        self.states = states
        self.start_states = start_states
        self.end_states = end_states
        self.transitions = transitions
        if not self.validate():
            raise RuntimeError('Automatic: input error')

    def validate(self):
        # TODO validate the input
        return True

    def equivalent(self, other):
        # TODO check the equality of the automatas
        return True


    # Operators

    def __eq__(self, other):
        return self.equivalent(other) 

    
