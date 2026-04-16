from crypto import encrypt_password, decrypt_password
from getpass import getpass
from auth import authenticate_master_pass
from vault import load_vault, save_vault


def find_by_email(email, db): 

    qpass = db.passwords.find_one(
        {"gmail" : email}
    )      

    return qpass


def add_details(args, db): 
    
    # check_mail = find_by_email(args.gmail, db)
    # if check_mail : 
    #     print("Mail already exists..")

    # else:   
    #     config = db.config.find_one({"type" : "master_config"})
    #     salt = config['salt']

    #     #for now we'll be asking user the master password everytime he performs the operation
    #     master_password = getpass("Enter master password: ")
    #     master = authenticate_master_pass(db, master_password)
    #     encrypted_password = encrypt_password(master_password, args.password, salt)



    #     if master == "verified" : 
    #         data = {
    #             "gmail" : args.gmail, 
    #             "pass" : encrypted_password
    #         }

    #         db.passwords.insert_one(data)

    #         print(f"QPass: Password added for gmail {args.gmail}")
        
    #     else: 
    #         print("Authentication failed")

    master_pass = getpass("Enter master password: ")

    loaded_data = load_vault(db, master_pass)
    new_data = {
        args.gmail : args.password
    }

    loaded_data.append(new_data)
    save_vault(loaded_data, db, master_pass)


def get_details(db): 
    # check_mail = find_by_email(args.gmail, db) 
    # if check_mail : 

    #     config = db.config.find_one({"type" : "master_config"})
    #     salt = config['salt']

    #     #for now we'll be asking user the master password everytime he performs the operation
    #     master_password = getpass("Enter master password: ")
    #     master = authenticate_master_pass(db, master_password)

    #     if master == "verified" : 
    #         data = db.passwords.find_one(
    #             {
    #                 "gmail" : args.gmail
    #             }
    #         )

    #         password = data['pass']
    #         decrypted_password = decrypt_password(master_password, password, salt)
    #         data['pass'] = decrypted_password
    #         del data["_id"]
    #         print(data)

    #     else: 
    #         print("Authentication failed")

    # else : 
    #     print("Mail doesn't exists..")


    master_pass = getpass("Enter master password: ")
    loaded_data = load_vault(db, master_pass)
    print(loaded_data)




def get_vault_details(args, db): 

    # check_site = find_by_email(args.site, db)

    # if not check_site: 
    #     print("Site doesn't exists..")
    #     return 
    
    master_pass = getpass("Enter master password: ")
    loaded_data = load_vault(db, master_pass)
    site = args.site
    for d in loaded_data:
        for key in d.keys(): 
            if key == site:
                for k,v in d.items():  
                    print(f"{k}:{v}")
    


def delete_details(args, db): 
    
    # check_mail = find_by_email(args.gmail, db)
    # if check_mail : 

    #     master_password = getpass("Enter master password: ")
    #     master = authenticate_master_pass(db, master_password)

    #     if master == "verified" : 
        
    #         try:
    #             db.passwords.delete_one(
    #                 {"gmail":args.gmail}
    #             )
    #             print(f"Details of gmail : {args.gmail} deleted successfully")

    #         except Exception as e: 
    #             print(f"error : {e}")
    #     else: 
    #         print("Authentication failed..!")

    # else: 
    #     print("Mail doesn't exist..!")

    master_pass = getpass("Enter master password: ")
    site_to_del = args.site

    db.config.update_one(
        {"type":"vault"}, 
        {
            "$pull": {
                "data" : { site_to_del : {"$exists" : True}}
            }
        }
    )

    print(f"Details for site \"{site_to_del}\" deleted successfully!")
