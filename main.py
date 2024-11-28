import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Parametry programu"
    )
    parser.add_argument('-is', '--initial_state', type=str, required=True, help='Initial state as comma-separated bits (e.g., 1,0,1).')
    parser.add_argument('-ft', '--feedback_taps', type=str, required=True, help='Feedback taps as comma-separated indices (e.g., 1,3).')
    parser.add_argument('-m', type=int, required=True, help='Degree of the register (number of states).')
    parser.add_argument('-ol', '--output_length', type=int, required=True, help='Length of the output bit stream.')

    args = parser.parse_args()

    return args

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
        print("state:", state)
    
    return output

def main():
    args = parse_args()

    initial_state = [int(bit) for bit in args.initial_state.split(',')]
    initial_state.reverse()
    print(initial_state)

    feedback_taps = [int(tap) for tap in args.feedback_taps.split(',')]
    output_length = args.output_length

    output_stream = lfsr(initial_state, args.m, feedback_taps, output_length)
    print(output_stream)

if __name__ == "__main__":
    main()
