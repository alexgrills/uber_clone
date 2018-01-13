import uuid
import hashlib


def get_salt(email):
    pass


def check_if_account_exists(email):
    pass


def store_account(email, hashed_password):
    pass


def authenticate(email, password):
    db_password, salt = get_salt(email).split(':')
    salted_password = password.encode() + salt.encode()
    hashed_password = hashlib.sha256(salted_password).hexdigest()
    return db_password == hashed_password


def create_account(email, password):
    if not check_if_account_exists(email):
        salt = uuid.uuid4().hex
        salted_password = password.encode() + salt.encode()
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        db_password = hashed_password + ":" + salt
        response = store_account(email, db_password)
        return response
    return False
