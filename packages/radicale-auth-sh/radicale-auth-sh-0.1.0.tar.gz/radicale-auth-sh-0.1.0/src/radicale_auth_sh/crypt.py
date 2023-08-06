from argon2 import PasswordHasher


ph = PasswordHasher()


def salt_and_hash(password):
    secret = ph.hash(password)
    assert ph.verify(secret, password), "Password hash cannot be verified!"

    return secret
