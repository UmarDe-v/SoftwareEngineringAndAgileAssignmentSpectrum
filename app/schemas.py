from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

###################################### Normal Users #######################################################################


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    company: str
    last_login: Optional[datetime]
    last_login_ip: Optional[str] = None

    class Config:
        orm_mode = True


#user only register schema
class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    company: str


class UserUpdateUsers(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

    class Config:
        orm_mode = True 

###################################### Normal Users #######################################################################


###################################### Admin Users #######################################################################

# Schema for Updating a Normal User for admins
class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    company: Optional[str] = None
    password: Optional[str] = None  # Added password here



class UserInDBBase(UserCreate):
    id: int
    is_admin: bool
    is_superadmin: bool
    company: Optional[str] = None

    class Config:
        orm_mode = True

###################################### Admin Users #######################################################################


###################################### Token JWT Verifications #######################################################################


class TokenData(BaseModel):
    username: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

###################################### Token JWT Verifications #######################################################################



###################################### License Keys #######################################################################

class DecisionAction(str, Enum):
    accept = "accept"
    decline = "decline"
    revoke = "revoke"

class LicenseStatus(str, Enum):
    application_submitted = "application submitted"
    license_active = "license active"
    declined = "declined"
    revoked = "revoked"


class SpectrumLicenseCreate(BaseModel):
    description: Optional[str] = None
    subband_range: Optional[int] = None
    power_level: Optional[int] = None
    geographical_area: Optional[str] = None
    
class SpectrumLicenseResponse(BaseModel):
    license_id: int
    user_id: int
    is_active: bool
    created_at: datetime
    expires_at: Optional[datetime]
    description: Optional[str]
    current_status: str
    subband_range: Optional[str]
    power_level: Optional[str]
    geographical_area: Optional[str]

    class Config:
        orm_mode = True


class RevokedLicenseResponse(BaseModel):
    id: int
    user_email: str
    license_key: str
    reason: str
    revoked_at: datetime

    class Config:
        orm_mode = True


#This file defines all the data validation schemas using Pydantic for different parts of the application. 
# These are used for input validation, output formatting, and internal logic for normal users, admins, JWT tokens, 
# and spectrum licences. The models help make sure that only valid data is passed into the system, and that responses 
# follow a clear structure.