from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], default='bcrypt')

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Arguments
    ----------
    password : str
        The password to hash.

    Returns
    -------
    str : The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password.

    Arguments
    ----------
    plain_password : str
        The plain password to verify.
        
    hashed_password : str
        The hashed password to verify against.

    Returns
    -------
    bool : True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)