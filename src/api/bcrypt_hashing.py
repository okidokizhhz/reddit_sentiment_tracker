# ~/reddit_sentiment_tracker/src/api/bcrypt_hashing.py

import bcrypt

def hash_password(password: str) -> str:
    """ Hashes password and returns it as hashed_password - typecasts bytearray into bytes (bcrypt expect bytes) """

    # generating salt
    salt = bcrypt.gensalt()
    # encoding password to bytes
    password_bytes = password.encode('utf-8')
    # hashing password
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    # decoding bytes to utf-8
    hashed_password = hashed_password.decode('utf-8')

    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    """ Verifies if password was derived from hashed_password. Returns True/False """

    # encoding password to bytes
    password_bytes = password.encode('utf-8')
    # encoding hashed_password to bytes
    hashed_password_bytes = hashed_password.encode('utf-8')

    if bcrypt.checkpw(password_bytes, hashed_password_bytes):
        return True
    else:
        return False
