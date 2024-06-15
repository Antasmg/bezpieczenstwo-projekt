import paho.mqtt.client as mqtt
from rsa import generate_keys
from user import register, login


broker = 'test.mosquitto.org'
port = 1883
public_key = None
private_key = None
n = None

def encrypt(ascii):
    global public_key, n #będziemy szyfrować kluczem publicznym drugiej osoby
    encrypted_message_list = []

    for char in ascii:
        encrypted = pow(char, public_key, n)
        encrypted_message_list.append(str(encrypted))

    encrypted_message = ','.join(encrypted_message_list)
    return encrypted_message

def to_number(message):
    to_ascii = []
    for letter in message:
        letter_code = ord(letter)
        to_ascii.append(letter_code)
    encrypted_message = encrypt(to_ascii)
    return encrypted_message

def decode(num):
    global private_key, n
    d = private_key
    num = int(num)
    decrypted = pow(num, d, n)
    return decrypted

def decoder(message):
    message_tab = message.split(",")
    message = ''
    for num in message_tab:
        message += chr(decode(num))
    return message

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    decoded_message = decoder(message)

    print(f"{msg.topic}: {decoded_message}")

def start_chat(username):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message

    client.connect(broker, port, 60) 

    topic = f"chat/{username}"
    client.subscribe(topic)

    client.loop_start()
    global public_key, private_key, n
    public_key, private_key, n = generate_keys()

    #TODO: Dodać jak Kacper to doda
    #upload_public_key(public_key)

    print(f"Connected to chat as {username}. Type 'exit' to quit.")
    recipient = input("Enter the recipient's username: ")
    #TODO: Dodać jak Kacper doda baze danych
    #recipient_public_key = get_public_key()

    print("Enter your message:")
    message = input("")
    
    while True:
        if message.lower() == 'exit':
            
            #TODO: Dodać jak Kacper doda
            #delete_public_key()
            
            break

        encrypted_message = to_number(message)
        client.publish(f"chat/{recipient}", f"{username}: {encrypted_message}")
        message = input("")

    client.loop_stop()
    client.disconnect()

def menu():
    while True:
       choice = input("1. Register\n2. Login\n3. Exit\nChoose an option: ")
       if choice == '1':
           result = register()
       elif choice == '2':
           username = login()
           if username:
               start_chat(username)
       elif choice == '3':
           break
       else:
           print("Invalid choice. Please try again.")


def main():
    print("Welcome to Secure Communicator\n")
    menu()

if __name__ == "__main__":
    main()