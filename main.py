from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

from app.routesFolder import Authentication
from app.routesFolder import AdminOnly
from app.routesFolder import UserOnly
#from app.routesFolder import testing

from app import models
from app.db import engine


from app.Exceptions.exceptions import (
    TokenExpiredException,
    InvalidTokenException,
    UserAlreadyLoggedInException,
    PermissionDeniedException,
    UsernameAlreadyRegisteredException,
    EmailAlreadyRegisteredException,
    InvalidCredentialsException,
    AdminNotfound,
    UserNotfound,
    PasswordSame,
    NoSprectrumLicense,
    InvalidEmailException,
    InvalidUsernameException,
    InvalidCompanyException,
    ConfirmException,
    SpectrumLicensesFound,
    ExistingUserException,
    SubbandRangeException,
    PowerLevelException,
    GeographicalAreaException,
    LicenceAlreadyRevokedException
)

from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
)

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(Authentication.router, prefix="/auth", tags=["General Authentication Routes"])
app.include_router(AdminOnly.router, prefix="/admin", tags=["Admin Routes"])
app.include_router(UserOnly.router, prefix="/user", tags=["user"])
#app.include_router(testing.router, prefix="/testing", tags=["testing"])

#if token expired exception is raised, redirect to login page and delete the expired token cookie
@app.exception_handler(TokenExpiredException)
async def invalid_token_exception_handler(request: Request, exc: TokenExpiredException):
    return JSONResponse(
        status_code=HTTP_401_UNAUTHORIZED,
        content={"detail": "Token Expired"}
    )

@app.exception_handler(InvalidTokenException)
async def invalid_token_exception_handler(request: Request, exc: InvalidTokenException):
    return JSONResponse(
        status_code=HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid token. Please log in again."}
    )

@app.exception_handler(UserAlreadyLoggedInException)
async def user_already_logged_in_exception_handler(request: Request, exc: UserAlreadyLoggedInException):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "User is already logged in. Please log out first."}
    )

@app.exception_handler(PermissionDeniedException)
async def permission_denied_exception_handler(request: Request, exc: PermissionDeniedException):
    return JSONResponse(
        status_code=HTTP_403_FORBIDDEN,
        content={"detail": "You do not have permission to access this resource."}
    )

@app.exception_handler(UsernameAlreadyRegisteredException)
async def username_already_registered_exception_handler(request: Request, exc: UsernameAlreadyRegisteredException):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "Username already registered."}
    )

@app.exception_handler(EmailAlreadyRegisteredException)
async def email_already_registered_exception_handler(request: Request, exc: EmailAlreadyRegisteredException):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "Email already registered."}
    )

@app.exception_handler(InvalidCredentialsException)
async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=HTTP_401_UNAUTHORIZED,
        content={"detail": "Incorrect username or password"},
        headers={"WWW-Authenticate": "Bearer"},
    )

@app.exception_handler(AdminNotfound)
async def admin_not_found_exception_handler(request: Request, exc: AdminNotfound):
    return JSONResponse(
        status_code=HTTP_200_OK,
        content={
            "success": True,
            "data": [],
            "message": "No admins found."
        }
    )

@app.exception_handler(UserNotfound)
async def admin_not_found_exception_handler(request: Request, exc: AdminNotfound):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "User not found."}
    )

@app.exception_handler(PasswordSame)
async def password_same_exception_handler(request: Request, exc: PasswordSame):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "New password cannot be the same as the current password."}
    )


@app.exception_handler(NoSprectrumLicense)
async def password_same_exception_handler(request: Request, exc: NoSprectrumLicense):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "No spectrum license found "}
    )

@app.exception_handler(InvalidEmailException)
async def password_same_exception_handler(request: Request, exc: InvalidEmailException):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "Invalid Email format. Please provide a valid email address."}
    )

@app.exception_handler(InvalidUsernameException)
async def password_same_exception_handler(request: Request, exc: InvalidUsernameException):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "Username must be 3–30 characters and alphanumeric."}
    )

@app.exception_handler(InvalidCompanyException)
async def password_same_exception_handler(request: Request, exc: InvalidCompanyException):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "Invalid Company, company already registered/Minimum 2 characters and maximum 50 characters."}
    )

@app.exception_handler(ConfirmException)
async def password_same_exception_handler(request: Request, exc: ConfirmException):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "Please press confim before continuing your request."}
    )

@app.exception_handler(SpectrumLicensesFound)
async def password_same_exception_handler(request: Request, exc: SpectrumLicensesFound):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "Cannot delete user: they have associated spectrum license(s)."}
    )


@app.exception_handler(ExistingUserException)
async def password_same_exception_handler(request: Request, exc: ExistingUserException):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "Email, username, or company already exists."}
    )


@app.exception_handler(SubbandRangeException)
async def password_same_exception_handler(request: Request, exc: SubbandRangeException):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "Subband range must be between 100 and 6000 MHz."}
    )


@app.exception_handler(PowerLevelException)
async def password_same_exception_handler(request: Request, exc: PowerLevelException):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "Power level must be between 0 and 100 dBm."}
    )


@app.exception_handler(GeographicalAreaException)
async def password_same_exception_handler(request: Request, exc: GeographicalAreaException):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "Geographical area must be a valid UK location: england, scotland, wales, northern ireland, london, manchester, birmingham, glasgow, edinburgh, belfast"}
    )

@app.exception_handler(LicenceAlreadyRevokedException)
async def password_same_exception_handler(request: Request, exc: LicenceAlreadyRevokedException):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "License is already revoked."}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)



# ----------------------
# FastAPI App Entry Point
# ----------------------
# - Initializes the FastAPI app
# - Creates DB tables from SQLAlchemy models
# - Includes routers for auth, admin, user, and testing
# - Registers custom exception handlers for clean error responses
# - Runs the app using Uvicorn when executed directly
