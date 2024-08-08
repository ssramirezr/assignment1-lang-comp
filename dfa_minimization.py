class DFA:
    def __init__(self, states, alphabet, transitions, initial_state, accepting_states):
        # Initialize DFA components
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accepting_states = accepting_states

    def get_transition(self, state, symbol):
        return self.transitions.get((state, symbol), None)

    def minimize(self):
        # Generate pairs of states (p, q)
        pairs = {(p, q) for p in self.states for q in self.states if p < q}
        marked = set()

        # Mark distinguishable pairs
        marked.update((p, q) for p, q in pairs if (p in self.accepting_states) != (q in self.accepting_states))

        # Propagate marks
        changes = True
        while changes:
            changes = False
            new_marked = set(marked)
            for p, q in pairs - marked:
                for symbol in self.alphabet:
                    p_next = self.get_transition(p, symbol)
                    q_next = self.get_transition(q, symbol)
                    if (p_next, q_next) in marked or (q_next, p_next) in marked:
                        new_marked.add((p, q))
                        changes = True
                        break
            marked = new_marked

        # Return equivalent pairs
        return [(p, q) for p, q in pairs if (p, q) not in marked]

def parse_transitions(input_data, headers):
    # Parse transitions from input
    lines = input_data.strip().split('\n')
    transitions = {}

    for line in lines:
        values = line.split()
        state = int(values[0])
        transitions.update({(state, headers[i]): int(values[i + 1]) for i in range(len(headers))})

    return transitions

def result():
    # Read DFA configuration
    states_n = int(input())
    alphabet = input().split()
    accepting_states = set(map(int, input().split()))

    # Initialize DFA
    transitions = "\n".join(input() for _ in range(states_n))
    transitions = parse_transitions(transitions, alphabet)
    initial_state = 0
    states = set(range(states_n))
    dfa = DFA(states, set(alphabet), transitions, initial_state, accepting_states)

    # Minimize DFA and output equivalent pairs
    equivalent_pairs = dfa.minimize()
    output = ' '.join(f"({p},{q})" for p, q in equivalent_pairs)
    print(output)

if __name__ == "__main__":
    # Handle multiple test cases
    cases = int(input())
    for _ in range(cases):
        result()
