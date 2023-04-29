# KeyStash

Video Demo: <https://youtu.be/j5a0jTc9S10>

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

