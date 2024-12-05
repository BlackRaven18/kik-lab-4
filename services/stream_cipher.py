
def text_to_bits(text):
    """
    Funkcja zamienia tekst na listę bitów.
    
    :param text: wejściowy tekst (ciąg znaków)
    :return: lista bitów (0 i 1)
    """
    return [int(bit) for char in text for bit in format(ord(char), '08b')]


def bits_to_text(bits):
    """
    Funkcja zamienia listę bitów na tekst.
    
    :param bits: lista bitów (0 i 1)
    :return: tekst (ciąg znaków)
    """
    chars = [chr(int(''.join(map(str, bits[i:i + 8])), 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)


def encrypt_decrypt(text, lfsr_key_stream) -> tuple[str, list]:
    """
    Funkcja szyfruje lub deszyfruje tekst za pomocą strumienia klucza LFSR.
    Operacja XOR jest symetryczna - ta sama funkcja realizuje szyfrowanie i deszyfrowanie.
    
    :param text: tekst do zaszyfrowania lub odszyfrowania
    :param lfsr_key_stream: strumień klucza w postaci listy bitów
    :return: wynik operacji (ciąg znaków)
    """
    text_bits = text_to_bits(text) 
    key_bits = lfsr_key_stream[:len(text_bits)]
    encrypted_bits = [text_bit ^ key_bit for text_bit, key_bit in zip(text_bits, key_bits)]
    return bits_to_text(encrypted_bits), encrypted_bits