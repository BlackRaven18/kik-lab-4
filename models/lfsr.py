class LFSR:
    def __init__(self, initial_state, m, feedback_taps):
        self.initial_state = initial_state
        self.initial_state.reverse()

        if len(initial_state) != m:
            raise ValueError("Długość stanu początkowego musi być równa stopniowi rejestru (m).")
        self.m = m

        self.feedback_taps = feedback_taps

    def generate_output(self, output_length):
        state = self.initial_state[:]
        output = []  
        
        for _ in range(output_length):
            
            output.append(state[-1])
            
            new_bit = 0
            for tap in self.feedback_taps:
                new_bit ^= state[self.m - tap - 1] 
            
            state = [new_bit] + state[:-1]
        
        return output
