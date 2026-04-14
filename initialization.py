from getpass import getpass
import os
from crypto import encrypt_password


def is_initialized(db): 
    if db.config.find_one({"type":"master_config"}):
        return True
    else: 
        return False


def set_master_password(db): 
    master_password = getpass("Set master Password: ")    
    salt = os.urandom(16)

    encrypted_check = encrypt_password(master_password, "verified", salt)

    db.config.insert_one(
        {
            "type" : "master_config", 
            "salt" : salt, 
            "verification" : encrypted_check
        }
    )

