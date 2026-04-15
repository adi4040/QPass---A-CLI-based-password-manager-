from getpass import getpass
from crypto import decrypt_password, encrypt_password

def authenticate_master_pass(db, master_password): 
        

        
        config = db.config.find_one({"type" : "master_config"})
        master = config['verification']
        salt = config['salt']
        
        try: 
            master = decrypt_password(master_password, master, salt)
        except Exception as e: 
              print(f"Wrong password")

        return master
