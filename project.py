from typing import Optional

import typer
from rich import print as rprint
import pyperclip
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import Account, Base
from werkzeug.security import check_password_hash, generate_password_hash


# Main typer app
app = typer.Typer()

# Create sqlalchemy engine
engine: Engine = create_engine("sqlite:///data.db")

# Create tables
Base.metadata.create_all(bind=engine)

# Create session
session: Session = sessionmaker(bind=engine)()


def prompt_master_password(master: Optional[str] = None) -> Optional[str]:
    master_account = session.query(Account).filter(Account.master == 1).first()

    if not master_account:
        return None
    
    while True:
        if master:
            password = master
            master = None
        else:
            password = typer.prompt("Enter master password", hide_input=True)
        if check_password_hash(master_account.password, password):
            return password


def get_fernet_engine(master: Optional[str] = None) -> Fernet:
    """Gets master password"""
    master_password = prompt_master_password(master=master)

    if not master_password:
        rprint("[bold red]Master password not set[/bold red]")
        rprint("[bold red]Run: [/bold red][bold green]setup[/bold green]")
        raise typer.Exit()

    # For fernet
    salt = b'\xe7\x96\xdc2A\x15\xcd\xc9\x87\x90;\x06\xbb\xee\x16\x94'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    f = Fernet(key)
    return f


def generate_password(length: int = 16) -> str:
    """Generates password"""
    import random
    import string

    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(chars) for _ in range(length))

    return password


def new_password(generate: bool = True, password: Optional[str] = None) -> str:
    """Asks user for new password"""
    if password:
        return password
    if generate:
        password = generate_password()
    else:
        password = typer.prompt("Enter password", hide_input=True, confirmation_prompt=True)

    return password


@app.command()
def setup(
    username: str = typer.Argument("master", help = "Username for master password"),
    generate: bool = typer.Option(False, help="Generate password", show_choices=True),
    master_password: Optional[str] = typer.Option(None, "--master", "-m", help="Master password")
) -> None:
    """Sets up master password"""
    master_account = session.query(Account).filter(Account.master == 1).first()
    if master_account:
        print("Master password already set.")
        return
    else:
        if not master_password:
            master_password = new_password(generate=generate)

        master_account = Account(site="master", password=generate_password_hash(master_password), username=username, master=True)
        session.add(master_account)
        session.commit()

        if not generate:
            rprint("[bold green]Master password set[/bold green]")
        else:
            rprint(f"[bold green] Master password set(do not forget it):[/bold green] [bold red]{master_password}[/bold red]")


@app.command()
def set(
    username: str = typer.Argument(..., help="username or email for the account"), 
    site: str = typer.Argument("EMAIL", help="Name of the site the account is for"), 
    generate: bool = typer.Option(True, help="Generate password", show_choices=True),
    update: bool = typer.Option(False, help="Update password for the site", show_choices=True),
    password: Optional[str] = typer.Option(None, "--password", "-p", help="Password for the site"),
    master: Optional[str] = typer.Option(None, "--master", "-m", help="Master password", envvar="MASTER_PASSWORD")
) -> None:
    """Sets password for a account"""
    fernet_engine = get_fernet_engine(master=master)

    account = session.query(Account).filter(Account.site == site, Account.username == username).first()
    if account:
        # Ask if user wants to update password
        if update or typer.confirm("Account already set. Do you want to update it?"):
            _password = new_password(generate=generate, password=password)
            account.password = fernet_engine.encrypt(_password.encode())
            session.commit()
        else:
            return
    else:
        _password = new_password(generate=generate, password=password)
        new_account = Account(site=site, password=fernet_engine.encrypt(_password.encode()), username=username)
        session.add(new_account)
        session.commit()

    rprint(f"[bold green]Password set:[/bold green] {_password}")


@app.command()
def get(
    username: str = typer.Argument(..., help="username or email for the account"),
    site: str = typer.Argument("EMAIL", help="Name of the site the account is for"),
    master: Optional[str] = typer.Option(None, "--master", "-m", help="Master password", envvar="MASTER_PASSWORD"),
    copy: bool = typer.Option(False, help="Copy password to clipboard", show_choices=True),
    show: bool = typer.Option(False, help="Show password")
) -> None:
    """Gets password for a account"""
    fernet_engine = get_fernet_engine(master=master)

    account = session.query(Account).filter(Account.site == site, Account.username == username).first()
    if account:
        password = fernet_engine.decrypt(account.password).decode()
        if copy:
            pyperclip.copy(password)
            rprint("[bold green]Password copied to clipboard[/bold green]")
            if show:
                rprint(f"[bold green]Password:[/bold green] {password}")
        else:
            rprint(f"[bold green]Password:[/bold green] {password}")
    else:
        rprint("[bold red]Account not set[/bold red]")


@app.command()
def check() -> None:
    """Checks if master password is set"""
    fernet_engine = get_fernet_engine()

    rprint("Helo!")


def main() -> None:
    app()

if __name__ == "__main__":
    main()

def create_test_session() -> None:
    """Creates test session"""
    global session

    test_engine: Engine = create_engine("sqlite:///test.db", echo=True)
    Base.metadata.create_all(test_engine)

    session = sessionmaker(bind=test_engine)()
