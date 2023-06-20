# KeyStash

## About

KeyStash is a password manager that allows users to store their passwords in a secure manner. The passwords are encrypted using AES-256 encryption and stored in a local database. The user can then retrieve their passwords by entering the master password. The master password is hashed using SHA-256 and stored in the database. The user can also generate a random password using the password generator.

## How to Run

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Program

```bash
python project.py --help
```

## How to Use

### Create a Master Account

```bash
python project.py setup
```

### Add a account

```bash
python project.py set --help
```

### Get a account

```bash
python project.py get --help
```

## Description

This program is made with python typer which is a library that allows you to create command line interfaces. The program uses a sqlite database to store the passwords. Program uses the cryptography library to encrypt and decrypt the passwords. The program also uses sqlite3 library to interact with the database. The program has 3 main commands: setup, set, and get. The setup command is used to create a master account. The set command is used to add a new account. The get command is used to retrieve a password.

### Setup

The setup command is used to create a master account. The user can also optionally provide a username. The user is prompted to enter a master password. The master password is then hashed using SHA-256 and stored in the database. The user is then prompted to enter the master password again to confirm. If the passwords match, the user is notified that the master account has been created. If the passwords do not match, the user is notified that the passwords do not match and the master account is not created. The user can also opt to generate a random password for the master password.

### Set

The set command is used to add a new account. The user need to provide a username/email for the first argument, user can also provide a site the account is for which defaults to EMAIL if none is provided. The user is then prompted to enter the master password and a password is automatically generated, encrypted and stored in the database. The user can opt to provide a password with `--no-generate` flag. 

### Get

The get command is used to retrieve a password. The user need to provide a username/email for the first argument, user can also provide a site the account is for which defaults to EMAIL if none is provided. The user is then prompted to enter the master password. The password is then decrypted and displayed to the user. If the password does not exist, the user is notified that the password does not exist. The user can also opt to copy the password to the clipboard with `--copy` flag.


## Technical Overview

The user's master password is hashed using SHA-256 and stored in the database. The user's passwords are encrypted using AES-256 encryption and stored in the database. The user's passwords are encrypted using a key derived from the master password. 

During the set and get commands, the user is prompted for the master password to derive the key for encryption and decryption. After the user is authorized, the program then encrypts or decrypts the password using the key. The program then stores the encrypted password in the database or displays the decrypted password to the user.
