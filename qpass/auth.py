from getpass import getpass
from .crypto import decrypt_password, encrypt_password, derive_key
from .session_configs import SESSION, TIME_OUT
from cryptography.fernet import Fernet, InvalidToken
from getpass import getpass
import time
from datetime import datetime

def authenticate_master_pass(db, master_password):

    config = db.config.find_one({"type": "master_config"})
    encrypted_check = config['verification']
    salt = config['salt']

    try:
        decrypted = decrypt_password(master_password, encrypted_check, salt)

        if decrypted == "verified":
            return True
        else:
            return False

    except Exception:
        return False


def login(db): 

    check_conf = SESSION["key"]

    if check_conf: 
        print("You are already logged in..")
        return 
    

    
    master_pass = getpass("Enter master password: ")
    if not authenticate_master_pass(db, master_pass): 
        print("Authentication failed..")
        return 
    
    master = db.config.find_one({"type":"master_config"})
    salt = master["salt"]

    key = derive_key(master_pass, salt)
    time_s = time.time()
    SESSION['key'] = key 
    SESSION['expires_at'] = time_s + TIME_OUT 

    print("Login Successful..")
    

def logout():
    
    if not SESSION['key']:
        print("You have already logged out..")
        return 
    
    SESSION['key'] = None
    SESSION['expires_at'] = None
    
    print("Logged out successfully..")
