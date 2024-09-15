# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Union
from fastapi.middleware.cors import CORSMiddleware

import models
from database import SessionLocal, engine

app = FastAPI()

# Allow CORS from your frontend
origins = [
    "http://localhost:3000",  # React frontend or other client
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for input validation and response formatting
class UserBase(BaseModel):
    first_name: str
    last_name: str
    age: float
    is_active: bool
    gender: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class SuccessResponse(BaseModel):
    status: str
    data: Union[List[UserOut], UserOut, dict]

# 1. List all users
@app.get("/users/", response_model=SuccessResponse)
async def list_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        return {"status": "error", "data": {}}
    return {"status": "success", "data": users}

# 2. Get a user by ID
@app.get("/users/{user_id}", response_model=SuccessResponse)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "data": user}

# 3. Create a new user
@app.post("/users/", response_model=SuccessResponse)
async def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    user = models.User(**new_user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"status": "success", "data": user}

# 4. Update a user by ID
@app.put("/users/{user_id}", response_model=SuccessResponse)
async def update_user(user_id: int, updated_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updated_data.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return {"status": "success", "data": user}

# 5. Delete a user by ID
@app.delete("/users/{user_id}", response_model=SuccessResponse)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"status": "success", "data": {}}
