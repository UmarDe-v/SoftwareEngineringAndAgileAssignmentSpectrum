from datetime import datetime, timedelta
import re
from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app import auth, models, schemas, security
from app.db import get_db

from app.Exceptions.exceptions import (
    UserAlreadyLoggedInException,
    PermissionDeniedException,
    UsernameAlreadyRegisteredException,
    EmailAlreadyRegisteredException,
    InvalidCredentialsException,
    PasswordSame,
    NoSprectrumLicense,
    UserNotfound,
    InvalidEmailException,
    InvalidUsernameException,
    InvalidCompanyException,
    ConfirmException,
    SpectrumLicensesFound
)

router = APIRouter()




# ----------------------------------------------
# Admin Login Route /login
# ----------------------------------------------
# - Prevents login if admin is already authenticated (via cookie)
# - Validates credentials using hashed password check
# - Generates JWT access token (1 hour expiry)
# - Updates admin's last login time and IP address
# - Sets access token as an HTTP-only cookie for secure session
# - Returns success message on login

@router.post("/login", response_model=schemas.Token, summary="Admin - Login",)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    token = request.cookies.get("access_token")

    if token:
        raise UserAlreadyLoggedInException()

    user = auth.get_admin_user(db, username=form_data.username)

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

    response = JSONResponse(content={"message": "Login successful"})

    # Delete the existing access token cookie if it exists
    response.delete_cookie("access_token")

    # Set the new access token in the cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to False for local HTTP
        samesite="Strict",  # Prevent sending the cookie in cross-site requests
        max_age=3600,  # Expiry time in seconds (1 hour)
        path="/"  # Ensure the cookie is available across the entire app
    )
    
    return response



# ----------------------------------------------
# Route: GET /admin/users
# Description:
# - Allows admin or superadmin to retrieve a list of all users
# - Returns a list of users from the database
# - Raises permission denied error if current user lacks admin privileges
# ----------------------------------------------

@router.get("/admin/users", response_model=List[schemas.UserOut], summary="Admin - Get all users")
async def get_all_users(
    current_user: models.Admin = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if isinstance(current_user, models.Admin) and (current_user.is_admin or current_user.is_superadmin):
        users = db.query(models.User).all()
        return users
    raise PermissionDeniedException()




# ----------------------------------------------
# Route: GET /licenses
# Description:
# - Admin-only route to view spectrum licenses
# - Optional query parameter 'status' to filter licenses by their current status
# - Raises permission denied if user is not an admin
# - Raises NoSprectrumLicense if no licenses found matching the criteria
# ----------------------------------------------

@router.get(
    "/licenses",
    response_model=List[Union[schemas.SpectrumLicenseResponse, schemas.RevokedLicenseResponse]],
    summary="Admin - View spectrum licenses"
)
async def view_licenses(
    status: Optional[schemas.LicenseStatus] = Query(None, description="Filter by status: e.g. 'application submitted', 'license active', 'declined'"),
    current_user: models.Admin = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if not isinstance(current_user, models.Admin) or not current_user.is_admin:
        raise PermissionDeniedException()

    query = db.query(models.SpectrumLicense)
    if status is not None:
        query = query.filter(models.SpectrumLicense.current_status == status.value)

    licenses = query.all()
    if not licenses:
        if status is not None:
            msg += f" with status '{status.value}'"
        raise NoSprectrumLicense()

    return licenses




# ----------------------------------------------
# Route: POST /licenses/{license_id}/decision
# Description:
# - Admin-only route to accept, decline, or revoke a spectrum license by license_id
# - Requires 'action' query parameter: accept, decline, or revoke
# - Updates license status and activity accordingly
# - Checks for license and user existence, raising exceptions if not found
# - Commits changes and returns a confirmation message
# ----------------------------------------------

@router.post("/licenses/{license_id}/decision", summary="Admin - Accept, decline or revoke a license")
async def decide_license(
    license_id: int,
    action: schemas.DecisionAction = Query(..., description="Action to take: accept, decline or revoke"),
    current_user: models.Admin = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if not isinstance(current_user, models.Admin) or not current_user.is_admin:
        raise PermissionDeniedException()

    license = db.query(models.SpectrumLicense).filter(
        models.SpectrumLicense.license_id == license_id
    ).first()

    if not license:
        raise NoSprectrumLicense()

    # Only forbid decline or revoke if license is already declined or revoked
    if action in {"decline", "revoke"} and license.current_status in {"declined", "revoked"}:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot {action} a license that is already '{license.current_status}'."
        )

    if action == "accept":
        license.current_status = "license active"
        license.is_active = True
        license.expires_at = datetime.utcnow() + timedelta(days=30)

    elif action == "decline":

        if license.current_status != "application submitted":
            raise HTTPException(
                status_code=400,
                detail="Only application submitted licenses can be declined."
            )
        
        license.current_status = "declined"
        license.is_active = False
        license.expires_at = None  # Clear expiry date on revoke

    elif action == "revoke":
        license.expires_at = None  # Clear expiry date on revoke
        if license.current_status != "license active":
            raise HTTPException(
                status_code=400,
                detail="Only active licenses can be revoked."
            )

        # Validate user exists
        user = db.query(models.User).filter(models.User.id == license.user_id).first()
        if not user:
            raise UserNotfound()

        license.current_status = "revoked"
        license.is_active = False

    db.commit()
    return {"message": f"License successfully {action}", "license_id": license_id}



# ----------------------------------------------
# Route: PUT /update_user/{user_id}
# Description:
# - Admin-only route to update user information by user_id
# - Validates and updates email, username, company, and password fields, including hashing
# - Checks for email and username uniqueness and valid formats
# - Enforces password complexity and prevents reuse of old password
# - Commits changes and returns the updated user object
# ----------------------------------------------


@router.put("/update_user/{user_id}", response_model=schemas.UserUpdate, summary="Admin - Update User Info")
async def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    current_user: models.Admin = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    

    if not isinstance(current_user, models.Admin) or not current_user.is_admin:
        raise PermissionDeniedException()

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise UserNotfound()

    if user_update.email and user_update.email != db_user.email:
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, user_update.email):
            raise InvalidEmailException()
        
        existing_email = db.query(models.User).filter(models.User.email == user_update.email).first()
        if existing_email:
            raise EmailAlreadyRegisteredException()
        db_user.email = user_update.email

    if user_update.username and user_update.username != db_user.username:
        if not user_update.username.isalnum() or not (3 <= len(user_update.username) <= 30):
            raise InvalidUsernameException()
        
        existing_username = db.query(models.User).filter(models.User.username == user_update.username).first()
        if existing_username:
            raise UsernameAlreadyRegisteredException()
        db_user.username = user_update.username

    if user_update.company and user_update.company != db_user.company:
        if not (2 <= len(user_update.company) <= 50):
            raise InvalidCompanyException()

    if user_update.password:
        if security.verify_password(user_update.password, db_user.hashed_password):
            raise PasswordSame()

        if len(user_update.password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters.")
        if not re.search(r"[A-Z]", user_update.password):
            raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", user_update.password):
            raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter.")
        if not re.search(r"\d", user_update.password):
            raise HTTPException(status_code=400, detail="Password must contain at least one digit.")

        db_user.hashed_password = security.get_password_hash(user_update.password)

    db.commit()
    db.refresh(db_user)
    return db_user



# ----------------------------------------------
# Route: DELETE /delete_user/{user_id}
# Description:
# - Admin-only route to delete a user by user_id
# - Requires explicit confirmation via query parameter `confirm=True`
# - Checks that user exists and has no associated spectrum licenses before deletion
# - Raises appropriate exceptions if checks fail
# - Deletes user and commits transaction
# - Returns Sucess
# ----------------------------------------------

@router.delete("/delete_user/{user_id}", status_code=204, summary="Admin - Delete a User")
async def delete_user(
    user_id: int,
    confirm: bool = Query(False, description="Must be True to confirm deletion"),
    current_user: models.Admin = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    if not isinstance(current_user, models.Admin) or not current_user.is_admin:
        raise PermissionDeniedException()

    if not confirm:
        raise ConfirmException()

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise UserNotfound()

    licenses_count = db.query(models.SpectrumLicense).filter(models.SpectrumLicense.user_id == user_id).count()

    if licenses_count > 0:
        raise SpectrumLicensesFound()

    db.delete(db_user)
    db.commit()

    return {"message": "User deleted successfully"}



























###########################################################################################################################
#test route
# @router.get("/conversation/")
# async def read_conversation(
#     current_user: schemas.UserInDBBase = Depends(auth.get_current_user),  # User is fetched via JWT
# ):
#     # Check if the user is an admin
#     if not current_user.is_admin:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You do not have permission to access this resource",
#         )
    
#     return {
#         "conversation": "This is a secure conversation for admins only",
#         "current_user": current_user.username,
#     }



# #reset normal user password not admin password
# @router.post("/admin/users/{user_id}/reset-password")
# async def reset_user_password(
#     user_id: int,
#     new_password: str,  # The new password to set
#     current_user: schemas.UserInDBBase = Depends(auth.get_current_user),  # Get the current user
#     db: Session = Depends(get_db)  # Dependency to get the database session
# ):
#     # Check if the current user is an admin
#     if not current_user.is_admin:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You do not have permission to access this resource",
#         )

#     # Fetch the user by ID from the database
#     user = db.query(models.User).filter(models.User.id == user_id).first()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )
    
#     #admin cannot change other admin password only superAdmin can do that
#     if user.is_admin:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Admins cannot reset other admins' passwords"
#         )

#     # Hash the new password
#     hashed_password = security.get_password_hash(new_password)

#     # Update the user's password
#     user.hashed_password = hashed_password
#     db.commit()  # Commit the change to the database

#     return {"message": "Password reset successful", "user_id": user_id}


# #edit non admin email username company 
# @router.put(
#     "/admin/users/{user_id}",
#     summary="Update User",
#     description="Admin-only route to update a user's email, username, or company (excluding admins).",
#     tags=["Admin"],
# )
# async def update_user(
#     user_id: int,
#     updated_data: schemas.UserUpdate,
#     db: Session = Depends(get_db),
#     current_user: schemas.UserInDBBase = Depends(auth.get_current_user),
# ):
#     if not current_user.is_admin:
#         raise HTTPException(status_code=403, detail="Not authorized")

#     user = db.query(models.User).filter(models.User.id == user_id).first()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if user.is_admin:
#         raise HTTPException(status_code=403, detail="Cannot edit another admin")

#     updated = False

#     # Email
#     if updated_data.email and updated_data.email != user.email:
#         existing_email = db.query(models.User).filter(models.User.email == updated_data.email).first()
#         if existing_email:
#             raise HTTPException(status_code=400, detail="Email already in use")
#         user.email = updated_data.email
#         updated = True

#     # Username
#     if updated_data.username and updated_data.username != user.username:
#         existing_username = db.query(models.User).filter(models.User.username == updated_data.username).first()
#         if existing_username:
#             raise HTTPException(status_code=400, detail="Username already in use")
#         user.username = updated_data.username
#         updated = True

#     # Company
#     if updated_data.company and updated_data.company != user.company:
#         user.company = updated_data.company
#         updated = True

#     if not updated:
#         raise HTTPException(status_code=400, detail="No changes detected")

#     db.commit()
#     db.refresh(user)

#     return {"message": "User updated successfully", "user": user.id}


# #get all non-admin users by username, email, company, or id (all inputs are optional dfefault shows all users)
# @router.get(
#     "/admin/users/", 
#     response_model=list[schemas.UserInDBBase], 
#     tags=["Admin"],
#     summary="Show all users - Optional Get non-admin users by username, email, company, or id", 
#     description="Retrieve all non-admin users, with optional filtering by username, email, company, or id."
# )
# async def get_users(
#     username: str = Query(None, max_length=100),  # Optional filter by username
#     email: str = Query(None, max_length=100),  # Optional filter by email
#     company: str = Query(None, alias="search_company", max_length=100),  # Optional filter by company
#     user_id: int = Query(None),  # Optional filter by user id
#     current_user: schemas.UserInDBBase = Depends(auth.get_current_user),  # Get the current user from the token
#     db: Session = Depends(get_db),  # Dependency to get DB session
# ):
#     # Check if the current user is an admin
#     if not current_user.is_admin:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You do not have permission to access this resource",
#         )
    
#     # Build the query to filter users
#     query = db.query(models.User).filter(models.User.is_admin == False)  # Only non-admin users

#     if username:
#         query = query.filter(models.User.username.ilike(f"%{username}%"))
    
#     if email:
#         query = query.filter(models.User.email.ilike(f"%{email}%"))
    
#     if company:
#         query = query.filter(models.User.company.ilike(f"%{company}%"))
    
#     if user_id:
#         query = query.filter(models.User.id == user_id)

#     # Execute the query and fetch the results
#     users = query.all()

#     if not users:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="No users found matching the filter"
#         )

#     # Convert SQLAlchemy model(s) to Pydantic model(s)
#     return [schemas.UserInDBBase.from_orm(user) for user in users]

# # PUT - update user info (email, is_admin, etc.)
# #UT /admin/users/{user_id}

# # POST - force reset a user's password
# #POST /admin/users/{user_id}/reset-password