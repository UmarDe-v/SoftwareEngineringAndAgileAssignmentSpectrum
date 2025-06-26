from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app import models, schemas, auth
from app.db import get_db

from app.Exceptions.exceptions import (
    NoSprectrumLicense,
    SubbandRangeException,
    PowerLevelException,
    GeographicalAreaException,
    NoSprectrumLicense,
    PermissionDeniedException

)

router = APIRouter()

# ----------------------------------------------
# Route: GET /my_licenses
# Description:
# - Allows a logged-in user to view all their own spectrum licenses
# - Validates that the current user is a regular User (not admin)
# - Queries the database for licenses belonging to the current user
# - Raises an error if no licenses found
# - Returns a list of user's spectrum licenses
# ----------------------------------------------


@router.get("/my_licenses", response_model=List[schemas.SpectrumLicenseResponse], summary="User only - View all spectrum licenses")
async def view_my_licenses(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if not isinstance(current_user, models.User):
        raise PermissionDeniedException()

    licenses = db.query(models.SpectrumLicense).filter(models.SpectrumLicense.user_id == current_user.id).all()

    if not licenses:
        raise NoSprectrumLicense()

    return licenses


# ----------------------------------------------
# Route: POST /apply_spectrum_license
# Description:
# - Allows a logged-in regular user to submit a new spectrum license application
# - Validates user role (must be a User)
# - Validates:
#   - subband_range (100 to 6000 MHz)
#   - power_level (0 to 100 dBm)
#   - geographical_area (must be one of predefined valid UK areas)
# - Generates a unique license_key (UUID)
# - Creates a new SpectrumLicense record with status "application submitted" and inactive
# - Saves to DB and returns confirmation message
# ----------------------------------------------


@router.post("/apply_spectrum_license",summary="User only - Submit spectrum license application workflow", description=("Submit a license application. Note: geographical_area must be one of the valid UK locations: england, scotland, wales, northern ireland london, manchester, birmingham, glasgow, edinburgh, belfast, Power level must be between 0 and 100 dBm, Subband range must be between 100 and 6000 MHz"
    ))

async def apply_spectrum_license(
    license_data: schemas.SpectrumLicenseCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if not isinstance(current_user, models.User):
        raise PermissionDeniedException()

    # ✅ Manual validation
    if license_data.subband_range is not None:
        if not (100 <= license_data.subband_range <= 6000):
            raise SubbandRangeException()

    if license_data.power_level is not None:
        if not (0 <= license_data.power_level <= 100):
            raise PowerLevelException()

    if license_data.geographical_area is not None:

        valid_uk_areas = {
            "england", "scotland", "wales", "northern ireland",
            "london", "manchester", "birmingham", "glasgow", "edinburgh", "belfast"
        }
        if license_data.geographical_area.lower() not in valid_uk_areas:
            raise GeographicalAreaException()

        

    license_key = str(uuid.uuid4())

    new_license = models.SpectrumLicense(
        user_id=current_user.id,
        license_key=license_key,
        description=license_data.description,
        subband_range=license_data.subband_range,
        power_level=license_data.power_level,
        geographical_area=license_data.geographical_area.capitalize(),
        is_active=False,
        current_status="application submitted"
    )

    db.add(new_license)
    db.commit()
    db.refresh(new_license)

    return {"message": "Application submitted. Please wait for admin approval."}



# ----------------------------------------------
# Route: POST /cancel_license/{license_id}
# Description:
# - Allows a logged-in regular user to cancel (revoke) one of their own spectrum licenses by license_id
# - Checks that the license exists and belongs to the current user
# - Raises an error if no such license is found
# - Raises an error if the license is already revoked
# - Updates the license status to "revoked" and sets is_active to False
# - Commits changes to the database and returns the updated license data
# ----------------------------------------------


@router.post("/cancel_license/{license_id}", summary="User only - Cancel (revoke) an owned license")
async def cancel_license(
    license_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if not isinstance(current_user, models.User):
        raise PermissionDeniedException()

    license = db.query(models.SpectrumLicense).filter(
        models.SpectrumLicense.license_id == license_id,
        models.SpectrumLicense.user_id == current_user.id
    ).first()

    if not license:
        raise NoSprectrumLicense()

    if license.current_status not in ["application submitted", "license active"]:
        raise HTTPException(
            status_code=400,
            detail=f"License cannot be cancelled in its current state: {license.current_status}"
        )

    license.is_active = False
    license.current_status = "revoked"
    license.expires_at = None  # Clear expiry date on revoke

    db.commit()
    db.refresh(license)
    return {
        "message": "License successfully cancelled.",
        "license_id": license.license_id,
        "new_status": license.current_status
    }

