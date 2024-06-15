import db

def register():
    username = input("Username: ")
    password = input("Password: ")
    db.add_user(username, password)
    
def login():
    username = input("Username: ")
    password = input("Password: ")
    user = db.get_user(username, password)
    if(user):
        return username
    else:
        print("Incorrect login or password")
        return None