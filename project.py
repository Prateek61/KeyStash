#test master key='CK5VN-kImuXPKaOZy9wczEXr9-bHExfD48RwNCSEes8='
from cryptography.fernet import Fernet
from sqlalchemy import create_engine,Column,String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
Base=declarative_base()
class Asite(Base):
    __tablename__="data"
    site=Column("site",String,primary_key=True)
    email=Column("email",String)
    username=Column("username",String)
    password=Column("password",String)

    def __init__(self,**kwargs):
        self.site=kwargs["site"]
        self.email=kwargs["email"]
        self.username=kwargs["username"]
        self.password=kwargs["password"]

    def __repr__(self):
        return f"<Asite(site='{self.site}', email='{self.email}', username='{self.username}', password='{self.password}')>"



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

def new_password():
    key=get_key()
    f = Fernet(key)
    engine = create_engine("sqlite:///data.db", echo=True)
    Base.metadata.create_all(bind=engine)
    Session=sessionmaker(bind=engine)
    session=Session() 
    while True:
        site=f.encrypt(get_site().encode())
        email=f.encrypt(get_email().encode())
        password=f.encrypt(get_password().encode())
        username=f.encrypt(get_username().encode())
        asite=Asite(site=site,email=email,password=password,username=username)
        session.add(asite)
        session.commit()


def saved_password():
    key=get_key()
    f = Fernet(key)
    engine = create_engine("sqlite:///data.db", echo=True)
    Base.metadata.create_all(bind=engine)
    Session=sessionmaker(bind=engine)
    session=Session() 
    vals=session.query(Asite).all()
    for val in vals:
        print("site=",f.decrypt(val.site).decode())
        print("email=",f.decrypt(val.email).decode())
        print("username=",f.decrypt(val.username).decode())
        print("password=",f.decrypt(val.password).decode())


    

def main() -> None:
    x=input("n=new-password s=saved-password ")
    if x=="n":
        new_password()

    if x=="s":
        saved_password()
    



if __name__ == "__main__":
    main()