# Ustawienia klucza publicznego
e = 26743
n = 31571

# Funkcja do przekształcania wiadomości na postać numeryczną
def text_to_numbers(text):
    return [ord(char) for char in text]

# Funkcja do szyfrowania wiadomości
def rsa_encrypt(message, e, n):
    numeric_message = text_to_numbers(message)
    encrypted_message = [pow(num, e, n) for num in numeric_message]
    return encrypted_message

# Wiadomość do zaszyfrowania
message = "test"

# Zaszyfrowanie wiadomości
encrypted_message = rsa_encrypt(message, e, n)
print("Zaszyfrowana wiadomość:", encrypted_message)
