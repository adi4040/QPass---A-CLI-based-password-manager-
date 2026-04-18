from crypto import encrypt_password, decrypt_password
from getpass import getpass
from auth import authenticate_master_pass
from vault import load_vault, save_vault


def find_by_site(site, db): 
    vault = db.config.find_one({"type":"vault"})
    data = vault["data"]

    found = False
    for d in data : 
        for k in d.keys(): 
            if k == site: 
                return True
    
    return found
            
    

def check_if_vault(db): 

    vault = db.config.find_one({"type":"vault"})
    if vault : return True
    else: return False

def add_details(args, db): 

    vault = check_if_vault(db)
    
    if not vault : 
        print("Vault is not created, use 'create_vault' to create one.")
        return
    
    site_to_add = args.site
    if find_by_site(site_to_add, db):
        print("Site already exists..")
        return 

    loaded_data = load_vault(db)
    new_data = {
        args.site : args.password
    }

    loaded_data.append(new_data)
    save_vault(loaded_data, db)



def get_details(db): 

    vault = check_if_vault(db)
    
    if not vault : 
        print("Vault is not created, use 'create_vault' to create one.")
        return
    
    loaded_data = load_vault(db)
    print(loaded_data)


def get_vault_details(args, db):

    vault = check_if_vault(db)
    
    if not vault : 
        print("Vault is not created, use 'create_vault' to create one.")
        return
     
    loaded_data = load_vault(db)
    site = args.site
 
    if not loaded_data: 
        print("Vault is empty")
        return 
    
    found = False

    for d in loaded_data:



        for key in d.keys(): 
            
            if key == site:
                for k,v in d.items():
                    found = True  
                    print(f"{k}:{v}")
                    break

    if found == False: 
        print("Site doesn't exists..")
        return    


def delete_details(args, db): 

    vault = check_if_vault(db)
    
    if not vault : 
        print("Vault is not created, use 'create_vault' to create one.")
        return
    
    site_to_del = args.site
    if not find_by_site(site_to_del, db):
        print("Site doesn't exists..")
        return 

    # master_pass = getpass("Enter master password: ")

    db.config.update_one(
        {"type":"vault"}, 
        {
            "$pull": {
                "data" : { site_to_del : {"$exists" : True}}
            }
        }
    )

    print(f"Details for site \"{site_to_del}\" deleted successfully!")
