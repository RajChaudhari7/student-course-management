import bcrypt


def hash_password(password):
    password = password.encode("utf-8")
    return bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")


def verify_password(password, hashed_password):
    password = password.encode("utf-8")
    hashed_password = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password, hashed_password)