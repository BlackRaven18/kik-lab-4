import argparse

from services.register import lfsr, calculate_tabs
from services.stream_cipher import encrypt_decrypt, text_to_bits, recover_key

from algorithms.berlekamp_massey import calculate_register_parameters

from utils.file import read_file, write_file

def parse_args():
    parser = argparse.ArgumentParser(
        description="Parametry programu"
    )
    parser.add_argument('--test_register', action='store_true', help='Test register')
    parser.add_argument('-e', '--encrypt', action='store_true', help='Encrypt message')
    parser.add_argument('-a', '--attack', action='store_true', help='Encrypt message')

    parser.add_argument('-is', '--initial_state', type=str, help='Initial state as comma-separated bits (e.g., 1,0,1).')
    parser.add_argument('-ft', '--feedback_taps', type=str, help='Feedback taps as comma-separated indices (e.g., 1,3).')
    parser.add_argument('-m', type=int, help='Degree of the register (number of states).')
    parser.add_argument('-ol', '--output_length', type=int, help='Length of the output bit stream.')

    parser.add_argument('-i', '--i', type=str, help='Input file.')
    parser.add_argument('-s', '--szyfrogram', type=str, help='Secret file.')
    parser.add_argument('-o', '--o', type=str, help='Output file.')

    args = parser.parse_args()

    return args

def main():
    args = parse_args()

    if args.test_register:
        initial_state = [int(bit) for bit in args.initial_state.split(',')]
        initial_state.reverse()

        feedback_taps = [int(tap) for tap in args.feedback_taps.split(',')]
        m = args.m

        output_length = args.output_length
        output_stream = lfsr(initial_state, m, feedback_taps, output_length)
        print("output_stream:", output_stream)

    elif args.encrypt:
        initial_state = [int(bit) for bit in args.initial_state.split(',')]
        initial_state.reverse()

        feedback_taps = [int(tap) for tap in args.feedback_taps.split(',')]
        m = args.m

        input_text = read_file(args.i, True)
        print("")
        output_length = len(text_to_bits(input_text))  # Liczba bitów potrzebnych do zaszyfrowania wiadomości
        key_stream = lfsr(initial_state, m, feedback_taps, output_length)


        encrypted_message, encypted_bits = encrypt_decrypt(input_text, key_stream)
        print("Zaszyfrowana wiadomość:")
        print(encrypted_message)

        write_file(args.o, ",".join(str(element) for element in encypted_bits))
        write_file("files/key_stream.txt", ",".join(str(element) for element in key_stream))

        # # Deszyfrowanie wiadomości
        # decrypted_message = encrypt_decrypt(encrypted_message, key_stream)
        # print("Odszyfrowana wiadomość:")
        # print(decrypted_message)

    elif args.attack:
        input_text = read_file(args.i, True)
        cipher_text = read_file(args.szyfrogram)
        cipher_bits = [int(bit) for bit in cipher_text.split(',')]

        recovered_key = recover_key(input_text, cipher_bits)
        print("Odszyfrowany klucz:")
        print(recovered_key)

        C, L = calculate_register_parameters(recovered_key)
        print("C:", C)
        print("L:", L)

        # creating new cryptosystem
        initial_state = recovered_key[:L]
        initial_state.reverse() # !!! important

        print("New initial state:")
        print(initial_state)

        taps = calculate_tabs(C.copy())

        print('Taps:', taps)
        
        new_key = lfsr(initial_state, L, taps, len(recovered_key))

        print("recovered_key:", recovered_key)
        print("new_key:      ", new_key)




    else:
        raise Exception("Nie wybrano trybu: --test_register, --decrypt")


if __name__ == "__main__":
    main()
