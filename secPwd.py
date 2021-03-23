import secrets, string, base64, os
from crypt import *
encode = True
def banner():
    print(f"""
    ______             ____  ___                                  
    | ___ \           | |  \/  |                                  
    | |_/ /_      ____| | .  . | __ _ _ __   __ _  __ _  ___ _ __ 
    |  __/\ \ /\ / / _` | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
    | |    \ V  V / (_| | |  | | (_| | | | | (_| | (_| |  __/ |   
    \_|     \_/\_/ \__,_\_|  |_/\__,_|_| |_|\__,_|\__, |\___|_|   
                                               __/ |          
                  Copyright by LukeProducts   |___/           

    """)
def Convert(Lst):
    return {Lst[i]: Lst[i + 1] for i in range(0, len(Lst), 2)}
def generate_rand():
    return "".join(secrets.choice(string.digits + string.ascii_letters + string.punctuation) for i in range(40))
def process_up():
    if not os.path.exists("encrypted_passwds/encrypted-passwds.txt"):
        if not os.path.exists("passwds.txt"):
            with open("passwds.txt", 'x') as f:
                f.write(f"{base64.b64encode('username'.encode('utf-8')).decode('utf-8')}\n{base64.b64encode('password'.encode('utf-8')).decode('utf-8')}")
        encrypt(gather_key(input("Enter key for SHA256 File Encryption [GENERAL MAIN ACCESS KEY]\n: ")), "passwds.txt")
    try:
        with open("passwds.txt", 'x') as f:
            f.write(f"{base64.b64encode('username'.encode('utf-8')).decode('utf-8')}\n{base64.b64encode('password'.encode('utf-8')).decode('utf-8')}")
            return False
    except:
        with open("passwds.txt") as f:
            unconverted = f.read().split('\n')
            if unconverted != ['']:
                converted = [base64.b64decode(ch.encode('utf-8')).decode('utf-8') for ch in unconverted]
                print(f"Actual saved Passwords: {int(int(len(converted)) / 2) -1}")
                return Convert(converted)
            else:
                with open("passwds.txt", 'w') as f:
                    f.write(f"{base64.b64encode('username'.encode('utf-8')).decode('utf-8')}\n{base64.b64encode('password'.encode('utf-8')).decode('utf-8')}")
            return False
def make_new(username, password):
    with open("passwds.txt", 'a') as f:
        data = f"\n{base64.b64encode(username.encode('utf-8')).decode('utf-8')}\n{base64.b64encode(password.encode('utf-8')).decode('utf-8')}"
        f.write(data)
        return True
def encode_again():
    encrypt(gather_key(cryptopass), "passwds.txt")
    os.remove("passwds.txt")
def delete():
    global encode
    encode = False
    os.remove("encrypted_passwds/encrypted-passwds.txt")
    os.remove('passwds.txt')
    print("Successfully deleteed this databench")
    exit(0)
banner()
process_up()
try:
    cryptopass = input("Enter Cryptopass: ")
    try:
        decrypt(gather_key(cryptopass), "encrypted_passwds/encrypted-passwds.txt")
        content = process_up()
        try:
            do = int(input("read[1],write[2], list saved[3], or delete the databench to add a new one[4]\n: "))
            if do == 1:
                if content:
                    try:
                        print("Password:", content[input("Username: ")])
                    except:
                        print("no such User saved")
                else:
                    print("no saved passwords")
            elif do == 2:
                try:
                    rand_or_not = int(
                        input("Generate random Password[1](very secure with 40 random digits); enter yourself[2]\n: "))
                    if rand_or_not == 1:
                        random_pass = generate_rand()
                        if make_new(input("Username: "), random_pass):
                            print(f"Process finished successfully! and created random Password: {random_pass}")
                        else:
                            print("an error occurred!")
                    elif rand_or_not == 2:
                        if make_new(input("Username: "), input("Password: ")):
                            print("Process finished successfully!")
                        else:
                            print("an error occurred!")

                except:
                    print("no valid arg given!")
            elif do == 3:
                print("Usernames:")
                for user in content:
                    if user != "username":
                        print(user)
            elif do == 4:
                delete()
            else:
                print("no valid arg given!")
        except:
            if do > 4:
                print("no valid arg given!")
    except:
        print("Encryption Password Incorrect!")
        try:
            os.remove('passwds.txt')
        except:
            pass
        encode = False
        content = False
except:
    content = False
    pass
if encode:
    encode_again()
