def calculate_tabs(C: list) -> list:
    tabs = [i for i, bit in enumerate(reversed(C[:-1]), start=1) if bit == 1]
    return tabs