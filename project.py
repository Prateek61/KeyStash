from typing import Optional

import typer
from rich import print as rprint, prompt
import pyperclip

from models import Account
from helper import SESSION, ARGS, get_master_password, generate_password, new_password, MASTER_ARG
from werkzeug.security import check_password_hash, generate_password_hash

app = typer.Typer()

@app.command()
def setup(
    username: str = typer.Argument("master", help = "Username for master password"),
    generate: bool = typer.Option(False, help="Generate password", show_choices=True)
) -> None:
    """Sets up master password"""
    master = SESSION.query(Account).filter(Account.master == 1).first()
    if master:
        print("Master password already set.")
        return
    else:
        master_password = new_password(generate=generate)

        master_account = Account(site="master", password=generate_password_hash(master_password), username=username, master=True)
        SESSION.add(master_account)
        SESSION.commit()

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
    master: Optional[str] = MASTER_ARG
) -> None:
    """Sets password for a account"""
    master_password = get_master_password(master=master)

    account = SESSION.query(Account).filter(Account.site == site, Account.username == username).first()
    if account:
        # Ask if user wants to update password
        if update or typer.confirm("Account already set. Do you want to update it?"):
            password = new_password(generate=generate, password=password)
            account.password = password
            SESSION.commit()
        else:
            return
    else:
        password = new_password(generate=generate, password=password)
        new_account = Account(site=site, password=new_password(generate=generate), username=username)
        SESSION.add(new_account)
        SESSION.commit()

    rprint(f"[bold green]Password set:[/bold green] {password}")


@app.command()
def get(
    username: str = typer.Argument(..., help="username or email for the account"),
    site: str = typer.Argument("EMAIL", help="Name of the site the account is for"),
    master: Optional[str] = MASTER_ARG,
    copy: bool = typer.Option(False, help="Copy password to clipboard", show_choices=True),
    show: bool = typer.Option(False, help="Show password")
) -> None:
    """Gets password for a account"""
    master_password = get_master_password(master=master)

    account = SESSION.query(Account).filter(Account.site == site, Account.username == username).first()
    if account:
        if copy:
            pyperclip.copy(account.password)
            rprint("[bold green]Password copied to clipboard[/bold green]")
            if show:
                rprint(f"[bold green]Password:[/bold green] {account.password}")
        else:
            rprint(f"[bold green]Password:[/bold green] {account.password}")
    else:
        rprint("[bold red]Account not set[/bold red]")

@app.command()
def check() -> None:
    """Checks if master password is set"""
    password = get_master_password()
    print(password)


def main() -> None:
    app()


if __name__ == "__main__":
    main()