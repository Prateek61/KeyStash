from models import Site, get_session

SESSION = get_session()



def get_key():
    return input("Enter master key ")
def get_site():
    return input("Enter site name ")
def get_email():
    return input("Enter email ")
def get_password():
    return input("Enter password ")
def get_username():
    return input("Enter username ")

def add_password(site: str, email: str, username: str, password: str):
    SESSION.add(Site(site=site, password=password, username=username, email=email))
    SESSION.commit()

def get_passwords():
    return SESSION.query(Site).all()

def new_password():
    site = get_site()
    email = get_email()
    username = get_username()
    password = get_password()

    # Add the data to the database
    session = get_session()
    session.add(Site(site=site, password=password, username=username, email=email))
    session.commit()


def saved_password():
    return None


    

def main() -> None:
    new_password()
    return
    x=input("n=new-password s=saved-password ")
    if x=="n":
        new_password()

    if x=="s":
        saved_password()
    



if __name__ == "__main__":
    main()