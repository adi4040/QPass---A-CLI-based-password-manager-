import json 
from crypto import encrypt_password, decrypt_password, decrypt_data, encrypt_data
from bson import ObjectId

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

def load_vault(db, master_pass): 

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
            decrypted_data = decrypt_data(master_pass, data, salt)
            print("Vault loaded..")
            return decrypted_data

def save_vault(data, db, master_password): 

    vault = []
    vault.extend(data)
    salt = db.config.find_one({"type":"master_config"})["salt"]
    encrypted_vault_data = encrypt_data(master_password, vault, salt)
    vault_id = db.config.find_one({"type":"vault"})["_id"]
    
    db.config.update_one(
        {"_id" : ObjectId(vault_id) } , 
        {"$set" : {"data" : encrypted_vault_data}}
    )

    print("Vault saved...")


# def save_vault(db): 
#     pass


