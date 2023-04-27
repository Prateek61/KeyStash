from typing import Optional

from models import Site
from database import SESSION

def main() -> None:

    master = SESSION.query(Site).filter(Site.master == 1).first()
    if master is None:
        print("No master password set. Please set a master password.")
        username = input("Enter username: ")
        password = input("Enter password: ")

        master_site = Site("master", password, username, True)
        SESSION.add(master_site)
        SESSION.commit()   
    else:
        password = input("Enter master password: ")
        while not master.check_password(password):
            password = input("Incorrect password. Enter master password: ")

    # TODO


if __name__ == "__main__":
    main()