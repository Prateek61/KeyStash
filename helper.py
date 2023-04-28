from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database
from models import Base, Account
from typer import Argument, Option
import typer
from rich import print as rprint
from werkzeug.security import check_password_hash

from typing import Optional

# Creates engine
engine: Engine = create_engine("sqlite:///data.db")

# Creates database if it doesn't exist
if not database_exists(engine.url):
    create_database(engine.url)

# Creates tables
Base.metadata.create_all(bind=engine)

# Creates session
SESSION: Session = sessionmaker(bind=engine)()

# Argument for master password
MASTER_ARG = Option(None, "--master", "-m", help="Master password", envvar="MASTER_PASSWORD")

def get_master_password(master: Optional[str] = None) -> str:
    master_account = SESSION.query(Account).filter(Account.master == 1).first()

    if not master_account:
        rprint("[bold red]Master password not set[/bold red]")
        rprint("[bold red]Run: [/bold red][bold green]setup[/bold green]")
        raise typer.Exit()
    
    while True:
        if master:
            password = master
            master = None
        else:
            password = typer.prompt("Enter master password", hide_input=True)
        if check_password_hash(master_account.password, password):
            return password
        else:
            rprint("[bold red]Incorrect password[/bold red]")


def generate_password() -> str:
    import random
    import string

    length = 16
    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(chars) for _ in range(length))

    return password


def new_password(generate: bool = True, password: Optional[str] = None) -> str:
    if password:
        return password
    if generate:
        password = generate_password()
    else:
        password = typer.prompt("Enter password", hide_input=True, confirmation_prompt=True)

    return password
