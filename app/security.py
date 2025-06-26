from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
import secrets

SECRET_KEY = "vN7K9sT3bX2fQpW6zR0yLmC8hJdVxUgM"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 25

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if the provided plain password matches the hashed password stored in the database.
    """
    return pwd_context.verify(plain_password, hashed_password)  # Compare the plain password with the hashed password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def generate_license_key():
    """Generate a secure random license key."""
    return secrets.token_urlsafe(32)

def hash_license_key(license_key: str) -> str:
    """Hash the license key using bcrypt."""
    return pwd_context.hash(license_key)

def verify_license_key(plain_key: str, hashed_key: str) -> bool:
    """Verify a plain license key against its hashed version."""
    return pwd_context.verify(plain_key, hashed_key)


#This file provides the security and authentication utilities for the application. It handles password hashing
# and verification, access token generation using JWT (JSON Web Tokens), and secure license key creation for spectrum 
# licences. These functions help enforce user identity, protect passwords and sensitive tokens, and provide cryptographically 
# secure license management.

#Password Security
#pwd_context is a context from Passlib that uses bcrypt, a strong, slow hashing algorithm designed to protect 
# passwords even if the database is compromised.

#get_password_hash(password: str)
#This function securely hashes a plain-text password before storing it in the database. Hashing ensures the actual
#  password is never saved directly.

#verify_password(plain_password: str, hashed_password: str)
#This compares a user’s login input with the stored hashed password. It’s used during login to authenticate users.

#This design follows best practices for password storage — hashing (with salt), not encryption or plain-text storage.

#JWT Access Token Handling
#create_access_token(data: dict, expires_delta: Optional[timedelta] = None)
#This generates a JWT token, which encodes user data (like username or ID) and an expiry timestamp using a secret 
# key and algorithm (HS256). The token is used for authenticating API requests.

#If no expiry time is provided, it defaults to 25 minutes.

#This helps ensure sessions time out appropriately, improving security.

#SECRET_KEY, ALGORITHM, and ACCESS_TOKEN_EXPIRE_MINUTES define the encoding logic for tokens. This setup enables
#  stateless user sessions.

# License Key Security
#generate_license_key()
#Uses secrets.token_urlsafe() to create a cryptographically random and URL-safe license key. These keys are secure 
# and unpredictable, ideal for license generation.

#hash_license_key(license_key: str)
#Just like passwords, license keys are hashed before storage. This way, even if the database is leaked, the original 
# license key cannot be reverse-engineered.

#verify_license_key(plain_key: str, hashed_key: str)
#Used when validating if a provided license key matches the hashed version stored in the database. This ensures the 
# system can still verify access without ever revealing the original key.