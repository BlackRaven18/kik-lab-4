import argparse

from models.lfsr import LFSR
from services.stream_cipher import encrypt_decrypt, text_to_bits

from algorithms.berlekamp_massey import calculate_register_parameters

from utils.lfsr import calculate_tabs
from utils.file import read_file

def parse_args():
    parser = argparse.ArgumentParser(
        description="Parametry programu"
    )
    parser.add_argument('--test_register', action='store_true', help='Test register')
    parser.add_argument('-d', '--decrypt', action='store_true', help='Decrypt message')
    parser.add_argument('-BM', '--Berlekamp-Massey', action='store_true', help='Use Berlekamp-Massey method')

    parser.add_argument('-is', '--initial_state', type=str, help='Initial state as comma-separated bits (e.g., 1,0,1).')
    parser.add_argument('-ft', '--feedback_taps', type=str, help='Feedback taps as comma-separated indices (e.g., 1,3).')
    parser.add_argument('-m', type=int, help='Degree of the register (number of states).')
    parser.add_argument('-ol', '--output_length', type=int, help='Length of the output bit stream.')

    parser.add_argument('-i', '--i', type=str, help='Input file.')
    parser.add_argument('-seed', type=str, help='Seed input file (for Berlekamp-Massey method).')
    parser.add_argument("-taps", type=str, help="Feedback taps input file (for Berlekamp-Massey method).")

    args = parser.parse_args()

    return args

def main():
    args = parse_args()

    if args.test_register:
        initial_state = [int(bit) for bit in args.initial_state.split(',')]

        feedback_taps = [int(tap) for tap in args.feedback_taps.split(',')]
        m = args.m

        output_length = args.output_length

        register = LFSR(initial_state, m, feedback_taps)

        output_stream = register.generate_output(output_length)
        print("output_stream:", output_stream)

    elif args.decrypt:
        initial_state = [int(bit) for bit in args.initial_state.split(',')]

        feedback_taps = [int(tap) for tap in args.feedback_taps.split(',')]
        m = args.m

        input_text = read_file(args.i, True)
        print("")
        output_length = len(text_to_bits(input_text))  # Liczba bitów potrzebnych do zaszyfrowania wiadomości

        register = LFSR(initial_state, m, feedback_taps)

        key_stream = register.generate_output(output_length)


        encrypted_message = encrypt_decrypt(input_text, key_stream)
        print("Zaszyfrowana wiadomość:")
        print(encrypted_message)

        # Deszyfrowanie wiadomości
        decrypted_message = encrypt_decrypt(encrypted_message, key_stream)
        print("Odszyfrowana wiadomość:")
        print(decrypted_message)

    elif args.Berlekamp_Massey:
        seed_raw = read_file(args.seed)

        seed = [int(bit) for bit in seed_raw.split(',')]

        C, L = calculate_register_parameters(seed)
        print("taps:", calculate_tabs(C))

    else:
        raise Exception("Nie wybrano trybu: --test_register, --decrypt")


if __name__ == "__main__":
    main()
