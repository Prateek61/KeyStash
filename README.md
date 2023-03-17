# KeyStash

A password manager to store and secure your passwords.

# To generate master key
from cryptography.fernet import Fernet
key = Fernet.generate_key()