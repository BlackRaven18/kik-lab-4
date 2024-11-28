
def lfsr(initial_state, m, feedback_taps, output_length):

    if len(initial_state) != m:
        raise ValueError("Długość stanu początkowego musi być równa stopniowi rejestru (m).")
    
    state = initial_state[:]
    output = []  
    
    for _ in range(output_length):
        
        output.append(state[-1])
        
        new_bit = 0
        for tap in feedback_taps:
            new_bit ^= state[m - tap - 1] 
        
        state = [new_bit] + state[:-1]
    
    return output