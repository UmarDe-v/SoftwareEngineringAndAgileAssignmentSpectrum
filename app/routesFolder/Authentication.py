from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime, timedelta
import re
from typing import Union

from app import models, schemas, auth, security
from app.security import get_password_hash
from app.db import get_db
from app.schemas import UserCreate


from app.Exceptions.exceptions import (
    UserAlreadyLoggedInException,
    PermissionDeniedException,
    InvalidCredentialsException,
    ExistingUserException,
    InvalidEmailException,
    InvalidUsernameException,
    InvalidCompanyException
)

router = APIRouter()


# ----------------------------------------------
# Route: POST /register
# Description:
# - Registers a new user with email, username, company, and password
# - Validates that no logged-in user is currently present (disallows registration if logged in)
# - Checks if email, username, or company already exist in DB to avoid duplicates
# - Validates email format, username format and length, and company length
# - Validates password complexity: min length 8, contains uppercase, lowercase, and digit
# - Hashes password before saving
# - Sets last_login to current UTC time and IP as placeholder (127.0.0.1)
# - Adds user to database, commits and returns success message with new user ID
# ----------------------------------------------


@router.post("/register", summary="Register Route")
async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: Union[models.User, models.Admin, None] = Depends(auth.get_current_user),
):
    # If current_user is found (logged in), block registration
    if current_user:
        raise UserAlreadyLoggedInException()

    existing_user = db.query(models.User).filter(
        (models.User.email == user.email) |
        (models.User.username == user.username) |
        (models.User.company == user.company)
    ).first()

    if existing_user:
        raise ExistingUserException()
    
    admin_with_email = db.query(models.Admin).filter(models.Admin.email == user.email).first()
    if admin_with_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, user.email):
        raise InvalidEmailException()

    if not user.username.isalnum() or not (3 <= len(user.username) <= 30):
        raise InvalidUsernameException()

    if not (2 <= len(user.company) <= 50):
        raise InvalidCompanyException()

    password = user.password
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one digit.")

    hashed_password = get_password_hash(user.password)

    new_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        last_login=datetime.utcnow(),
        last_login_ip="127.0.0.1",
        company=user.company
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id}



# ----------------------------------------------
# Route: POST /login
# Description:
# - General user login endpoint to obtain JWT access token
# - Checks if an access token cookie already exists and raises error if user is logged in
# - Verifies username and password credentials against database
# - Creates JWT token with username subject and expiry from config
# - Updates user's last login timestamp and IP address (from request client host)
# - Commits user info update to database
# - Returns JSON response with login success message, access token, and token type
# - Sets the JWT token in a secure, HTTP-only cookie with 1-hour expiry
# - Deletes any existing access token cookie before setting new one
# ----------------------------------------------

@router.post("/login", response_model=schemas.Token, summary="User only Login (no admin)",)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    token = request.cookies.get("access_token")
    if token:
        raise UserAlreadyLoggedInException()

    user = auth.get_user(db, username=form_data.username)

    if not user or not security.pwd_context.verify(form_data.password, user.hashed_password):
        raise InvalidCredentialsException()

    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    

    user.last_login = func.now()
    user_ip = request.client.host
    user.last_login_ip = user_ip

    db.commit()
    db.refresh(user) 

    #bubble test
    # Create response and set cookie
    response = JSONResponse(content={
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    })

    response.delete_cookie("access_token")  # clear old token first

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,           # Set to False only if you're not using HTTPS (for local dev)
        samesite="Strict",
        max_age=3600,          # 1 hour
        path="/"
    )

    return response



# ----------------------------------------------
# Route: POST /logout
# Description:
# - General user logout endpoint
# - Checks if an "access_token" cookie exists; raises error if not (user not logged in)
# - Deletes the "access_token" cookie to log the user out
# - Returns JSON response confirming successful logout
# ----------------------------------------------


@router.post("/logout",summary = "All User's Logout")
async def logout(request: Request):

    token = request.cookies.get("access_token")
    
    if not token:

        raise PermissionDeniedException()
    

    response = JSONResponse(content={"message": "Logout successful"})
    response.delete_cookie("access_token")
    return response



