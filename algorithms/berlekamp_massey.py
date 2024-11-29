from typing import List

def calculate_register_parameters(seed: List[int]) -> tuple[List[int], int]:
    n = len(seed)
    C = [1]
    B = [1]
    L = 0
    m = -1

    for N in range(n):
        d = seed[N]
        for i in range(1, L + 1):
            d ^= C[i] * seed[N - i]

        if d == 0:
            continue

        T = C[:]
        delta = N - m

        if len(C) <= len(B) + delta:
            C.extend([0] * (len(B) + delta - len(C)))

        for i in range(len(B)):
            C[i + delta] ^= B[i]

        if 2 * L <= N:
            L = N + 1 - L
            B = T
            m = N

    return C, L