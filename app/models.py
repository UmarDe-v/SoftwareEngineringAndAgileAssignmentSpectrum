from sqlalchemy import Column, Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    last_login = Column(DateTime, default=func.now(), onupdate=func.now())
    last_login_ip = Column(String)
    company = Column(String, unique=True, index=True)

    licenses = relationship("SpectrumLicense", back_populates="user")

    class Config:
        orm_mode = True



class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, default=func.now(), onupdate=func.now())
    last_login_ip = Column(String)

    class Config:
        orm_mode = True


class SpectrumLicense(Base):
    __tablename__ = "spectrum_licenses"

    license_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


    license_key = Column(String, unique=True, index=True, nullable=False)


    is_active = Column(Boolean, default=False)  # start inactive until approved
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=True)
    description = Column(String, nullable=True)

    # Track application workflow state (e.g., "application submitted", "approved")
    current_status = Column(String, nullable=False, default="application submitted")

    # Optional fields for detailed license info
    subband_range = Column(String, nullable=True)
    power_level = Column(String, nullable=True)
    geographical_area = Column(String, nullable=True)

    user = relationship("User", back_populates="licenses")

    class Config:
        orm_mode = True



#This file sets up the three main database models used in the application: User, Admin, and 
# SpectrumLicense. Each of these corresponds to a table in the PostgreSQL database.

#The User model represents a person or company applying for a spectrum licence. Each user has a 
# unique ID, email, username, and company name. The fields last_login and last_login_ip help track 
# when and where they last accessed the system. A key feature of this #model is its relationship with 
# the SpectrumLicense table — one user can have multiple licences. This is done through SQLAlchemy’s 
# relationship() function, and the reverse is declared in the SpectrumLicense model.

#The Admin model is a simpler table used to manage admin accounts who have access to manage licences 
# and users. Like users, admins also have unique email and username fields, along with password and 
# login tracking info. Admins don’t have a direct relationship to #licences in this setup, because 
# they don’t apply for them — they only manage them.

#The SpectrumLicense model stores each licence issued or requested. Every licence must be tied to a 
# user, which is enforced by the user_id field and its foreign key constraint linking it to the users 
# table. Each licence has a unique key (license_key) and includes #extra optional details like power 
# level, frequency subbands, and geographical coverage area. The current_status field is used to track 
# where the licence is in its approval process (e.g., pending, approved, revoked).

#Altogether, these models define a clear one-to-many relationship: one user can own many licences, 
# and licences cannot exist without being tied to a user. Admins sit separately, handling approvals and 
# management, but not owning licences themselves. The structure #is clean, normalized, and ready for role-based Acess Control