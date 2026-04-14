from crypto import encrypt_password, decrypt_password
from getpass import getpass
from auth import authenticate_master_pass

def find_by_email(email, db): 

    qpass = db.passwords.find_one(
        {"gmail" : email}
    )      
    return qpass



def add_details(args, db): 
    
    check_mail = find_by_email(args.gmail, db)
    if check_mail : 
        print("Mail already exists..")

    else:   

        config = db.config.find_one({"type" : "master_config"})
        salt = config['salt']

        #for now we'll be asking user the master password everytime he performs the operation
        master_password = getpass("Enter master password: ")
        encrypted_password = encrypt_password(master_password, args.password, salt)

        data = {
            "gmail" : args.gmail, 
            "pass" : encrypted_password
        }

        db.passwords.insert_one(data)

        print(f"QPass: Password added for gmail {args.gmail}")


def get_details(args, db): 
    check_mail = find_by_email(args.gmail, db) 
    if check_mail : 

        config = db.config.find_one({"type" : "master_config"})
        salt = config['salt']

        #for now we'll be asking user the master password everytime he performs the operation
        master_password = getpass("Enter master password: ")
        data = db.passwords.find_one(
            {
                "gmail" : args.gmail
            }
        )

        password = data['pass']
        decrypted_password = decrypt_password(master_password, password, salt)
        data['pass'] = decrypted_password
        del data["_id"]
        print(data)

    else : 
        print("Mail doesn't exists..")


def delete_details(args, db): 
    
    check_mail = find_by_email(args.gmail, db)
    if check_mail : 

        master = authenticate_master_pass(db)

        if master == "verified" : 
        
            try:
                db.passwords.delete_one(
                    {"gmail":args.gmail}
                )
                print(f"Details of gmail : {args.gmail} deleted successfully")
                
            except Exception as e: 
                print(f"error : {e}")
        else: 
            print("Authentication failed..!")

    else: 
        print("Mail doesn't exist..!")
