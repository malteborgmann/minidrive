import os
from typing import List

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app import crud
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


@app.get("/")
def read_root():
    return {"message": "Welcome to Minidrive Contacts"}


@app.post("/contacts/", response_model=schema.ContactResponse)
def create_contact(contact: schema.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db=db, contact=contact)


@app.get("/contacts/", response_model=List[schema.ContactResponse])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return contacts


@app.get("/contacts/{contact_id}", response_model=schema.ContactResponse)
def read_contact_by_id(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.put("/contacts/{contact_id}", response_model=schema.ContactResponse)
def update_contact_by_id(
    contact_id: int, contact: schema.ContactUpdate, db: Session = Depends(get_db)
):
    db_contact = crud.update_contact(db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.delete("/contacts/{contact_id}", response_model=schema.ContactResponse)
def delete_contact_by_id(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.delete_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


# https://fastapi.tiangolo.com/tutorial/request-files/#define-file-parameters
@app.post("/files/")
async def upload_file(file: UploadFile = File(...)):
    # Erst einmal nur lokal im Endpunkt verarbeiten, wie gewünscht
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {
        "filename": file.filename,
        "status": "uploaded",
        "saved_path": file_path,
        "size_bytes": len(content),
    }
