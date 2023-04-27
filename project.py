from typing import Optional

import typer
from rich import print as rprint

from models import Site
from database import SESSION
from werkzeug.security import check_password_hash

app = typer.Typer()


def get_master_password() -> str:
    master = SESSION.query(Site).filter(Site.master == 1).first()

    if not master:
        rprint("[bold red]Master password not set[/bold red]")
        rprint("[bold red]Run: [/bold red][bold green]setup[/bold green]")
        raise typer.Exit()
    
    while True:
        password = typer.prompt("Enter master password", hide_input=True)
        if check_password_hash(master.password, password):
            return password
        else:
            typer.echo("Incorrect password")


@app.command()
def setup():
    master = SESSION.query(Site).filter(Site.master == 1).first()
    if master:
        print("Master password already set.")
        return
    else:
        username = typer.prompt("Enter master username")
        password = typer.prompt("Enter master password", hide_input=True)

        master_site = Site(site="master", password=password, username=username, master=True)
        SESSION.add(master_site)
        SESSION.commit()


#@authentication_required
@app.command()
def check():
    password = get_master_password()
    print(password)


def main() -> None:
    app()


if __name__ == "__main__":
    main()