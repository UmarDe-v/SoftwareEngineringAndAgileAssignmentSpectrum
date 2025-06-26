# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from datetime import datetime

# from app import models
# from app.db import get_db
# from app.security import get_password_hash


# router = APIRouter(prefix="/testing", tags=["testing"])

# @router.post("/register")
# def register_admin(email: str, username: str, password: str, db: Session = Depends(get_db)):
#     existing_admin = db.query(models.Admin).filter(models.Admin.email == email).first()
#     if existing_admin:
#         raise HTTPException(status_code=400, detail="Admin with this email already exists.")
    
#     hashed_password = get_password_hash(password)
    
#     new_admin = models.Admin(
#         email=email,
#         username=username,
#         hashed_password=hashed_password,
#         last_login=datetime.utcnow(),
#         last_login_ip="127.0.0.1"
#     )

#     db.add(new_admin)
#     db.commit()
#     db.refresh(new_admin)

#     return {"message": "Admin registered successfully", "admin_id": new_admin.id}
