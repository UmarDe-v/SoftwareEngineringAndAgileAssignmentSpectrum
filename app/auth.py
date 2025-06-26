from fastapi import Request, Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app import models, security
from app.db import get_db
from .security import *


from app.Exceptions.exceptions import (
    PermissionDeniedException,
    TokenExpiredException,
    InvalidTokenException
)
# ----------------------------------------------
# Function: get_admin_user
# Description:
# - Fetches an admin user from the database by their username
# - Queries the Admin table for a record matching the given username
# - Returns the Admin model instance if found, otherwise returns None
# - Used to authenticate or retrieve admin user details based on username
# ----------------------------------------------

def get_admin_user(db: Session, username: str):
     return db.query(models.Admin).filter(models.Admin.username == username).first()

# ----------------------------------------------
# Function: get_user
# Description:
# - Retrieves a regular user from the database by username
# - Queries the User table for a record matching the provided username
# - Returns the User model instance if found, else returns None
# - Commonly used during login or user validation processes
# ----------------------------------------------

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# ----------------------------------------------
# Async function: get_current_user
# Purpose:
# - Extracts the JWT token from the request cookies
# - Validates and decodes the JWT to extract the username ("sub" claim)
# - Handles JWT errors, including token expiration and invalid tokens
# - Queries the database to find a matching User or Admin by username
# - Adds a 'user_type' attribute to distinguish between User and Admin
# - If an Admin is found, also sets 'is_admin' to True
# - Raises PermissionDeniedException if no matching user or admin is found
# Usage:
# - Typically used as a FastAPI dependency to identify the currently authenticated user
# ----------------------------------------------

async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
):

    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        # Decode JWT token
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise InvalidTokenException()
    except JWTError as e:
        if "Signature has expired" in str(e):
            raise TokenExpiredException()
        raise InvalidTokenException()

    # 3. Find user based on JWT username
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        user.user_type = "user"
        return user

    # If no user, check if it's an admin
    admin = db.query(models.Admin).filter(models.Admin.username == username).first()
    if admin:
        admin.user_type = "admin"
        admin.is_admin = True
        return admin

    raise PermissionDeniedException()