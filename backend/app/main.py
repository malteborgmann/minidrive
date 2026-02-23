from datetime import timedelta
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud
from app.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
    verify_password,
)
from app.database import SessionLocal, engine
from app.pydantic_schema import schema
from app.sql_schema import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Minidrive Contacts API")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register", response_model=schema.UserResponse)
def register_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.post("/token", response_model=dict)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
def read_root():
    return {"message": "Welcome to Minidrive Contacts"}


@app.post("/contacts/", response_model=schema.ContactResponse)
def create_contact(
    contact: schema.ContactCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_contact(db=db, contact=contact, user_id=current_user.id)


@app.get("/contacts/", response_model=List[schema.ContactResponse])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    contacts = crud.get_contacts(db, skip=skip, limit=limit, user_id=current_user.id)
    return contacts


@app.get("/contacts/{contact_id}", response_model=schema.ContactResponse)
def read_contact_by_id(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_contact = crud.get_contact(db, contact_id=contact_id, user_id=current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.put("/contacts/{contact_id}", response_model=schema.ContactResponse)
def update_contact_by_id(
    contact_id: int,
    contact: schema.ContactUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_contact = crud.update_contact(
        db, contact_id=contact_id, contact=contact, user_id=current_user.id
    )
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.delete("/contacts/{contact_id}", response_model=schema.ContactResponse)
def delete_contact_by_id(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_contact = crud.delete_contact(db, contact_id=contact_id, user_id=current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact
