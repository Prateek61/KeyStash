from typer.testing import CliRunner
from project import create_test_session

create_test_session()
runner = CliRunner()

from project import session, app
from project import generate_password_hash
from project import generate_password, new_password, prompt_master_password
from models import Account

# Remove all accounts
session.query(Account).delete()
session.commit()

def set_master_account():
    return runner.invoke(app, ["setup", "--master", "grass"])

def clear_database():
    session.query(Account).delete()
    session.commit()

# Tests for projects
def test_generate_password():
    assert len(generate_password()) == 16
    assert len(generate_password(32)) == 32
    assert len(generate_password(64)) == 64

# Tests for new_password
def test_new_password():
    assert new_password(password="Hello") == "Hello"

# Tests for prompt_master_password
def test_prompt_master_password():
    assert prompt_master_password(master="grass") == None # No master account set
    master_account = Account("master", generate_password_hash("grass"), username="master", master=True)
    session.add(master_account)
    assert prompt_master_password(master="grass") == "grass" # Master account set

# Test for app setup
def test_setup():
    session.rollback()
    # Invalid command
    result = runner.invoke(app, ["setup", "--invalid"])
    assert result.exit_code == 2
    # Set master account
    result = set_master_account()
    assert result.exit_code == 0
    assert "Master password set" in result.stdout
    # Try to set master account again
    result = set_master_account()
    assert result.exit_code == 0
    assert "Master password already set" in result.stdout

# Test for app add
def test_set():
    # Delete all accounts
    clear_database()

    # Set master account
    set_master_account()

    # Invalid command
    result = runner.invoke(app, ["set", "--invalid"])
    assert result.exit_code == 2
    # Add account with password
    result = runner.invoke(app, ["set","prateekpoudel61@gmail.com", "EMAIL", "--master", "grass", "-p", "password123"])
    assert result.exit_code == 0
    assert "Password set" in result.stdout
    assert "password123" in result.stdout
    clear_database()

# Test for app get
def test_get():
    # Delete all accounts
    clear_database()

    # Set master account
    set_master_account()

    # Add account
    result = runner.invoke(app, ["set","prateekpoudel61@gmail.com", "EMAIL", "--master", "grass", "-p", "password123"])
    assert result.exit_code == 0

    # Invalid command
    result = runner.invoke(app, ["get", "--invalid"])
    assert result.exit_code == 2
    # Get account
    result = runner.invoke(app, ["get", "prateekpoudel61@gmail.com", "EMAIL", "--master", "grass"])
    assert "password123" in result.stdout
    assert result.exit_code == 0
    