import json 
from crypto import encrypt_password, decrypt_password, decrypt_data, encrypt_data
from bson import ObjectId
from session_configs import SESSION
from cryptography.fernet import Fernet, InvalidToken

def create_vault(db): 
    
    vault = db.config.find_one({"type":"vault"})
    if vault: 
        print("Vault is already created..")
        return 

    db.config.insert_one(
        {
            "type" : "vault",
            "data" : []
        }
    )

    print("Vault Successfully Created!")

def load_vault(db): 
    vault = db.config.find_one({"type":"vault"})
    if not vault: 
        print("Please create a vault using 'create_vault' ")
    
    else:

        master = db.config.find_one({"type":"master_config"})
        salt = master['salt']
        del vault["_id"]      
        data = vault["data"]
        if not data : 
            return data
        
        else: 
            decrypted_data = decrypt_data(data)
            print("Vault loaded..")
            return decrypted_data
        


def save_vault(data, db): 

    vault = []
    vault.extend(data)
    salt = db.config.find_one({"type":"master_config"})["salt"]
    encrypted_vault_data = encrypt_data(vault)
    vault_id = db.config.find_one({"type":"vault"})["_id"]
    
    db.config.update_one(
        {"_id" : ObjectId(vault_id) } , 
        {"$set" : {"data" : encrypted_vault_data}}
    )

    print("Vault saved...")



