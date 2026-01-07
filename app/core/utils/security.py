import hashlib

## create hash password
def hash_password(password: str) -> str:

    #generate sha 256 hash
    return hashlib.sha256(password.encode()).hexdigest()
