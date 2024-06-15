import paho.mqtt.client as mqtt
import os
import db
from rsa import generate_keys
from user import register, login

broker = 'test.mosquitto.org'
port = 1883
public_key = None
private_key = None
n = None
recipient_public_key = None
recipient_n = None

def encrypt(ascii):
    global recipient_public_key, recipient_n
    encrypted_message_list = []

    for char in ascii:
        encrypted = pow(char, recipient_public_key, recipient_n)
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

    db.add_keys(username, public_key, n)

    print(f"Connected to chat as {username}. Type 'exit' to quit.")
    recipient = input("Enter the recipient's username: ")

    user = db.get_keys(recipient)
    if(user == None):
        print("User is not active yet")
        db.delete_keys(username)
        menu()
        
    global recipient_public_key, recipient_n
    recipient_public_key = int(user[1])
    recipient_n = int(user[2])

    print("Enter your message:")
    message = input("")
    
    while True:
        if message.lower() == 'exit':            
            db.delete_keys(username)
            break

        encrypted_message = to_number(message)
        client.publish(f"chat/{recipient}", f"{encrypted_message}")
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
               os.system('cls')
               start_chat(username)
       elif choice == '3':
           break
       else:
           print("Invalid choice. Please try again.")


def main():
    os.system('cls')
    print("Welcome to Secure Communicator\n")
    menu()

if __name__ == "__main__":
    main()