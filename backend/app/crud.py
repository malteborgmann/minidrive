from datetime import datetime, timezone
from typing import List

from sqlalchemy.orm import Session

from app.auth import get_password_hash
from app.pydantic_schema import schema
from app.sql_schema import models


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_contact(db: Session, contact_id: int, user_id: int):
    return (
        db.query(models.Contact)
        .filter(models.Contact.id == contact_id, models.Contact.owner_id == user_id)
        .first()
    )


def get_contacts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Contact)
        .filter(models.Contact.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_contact(db: Session, contact: schema.ContactCreate, user_id: int):
    now = datetime.now(timezone.utc)
    db_contact = models.Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        company=contact.company,
        notes=contact.notes,
        address=contact.address,
        created=now,
        modified=now,
        owner_id=user_id,
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)

    if contact.communications:
        for comm in contact.communications:
            db_comm = models.Communication(
                contact_id=db_contact.id,
                comm_type=comm.comm_type,
                label=comm.label,
                value=comm.value,
            )
            db.add(db_comm)
        db.commit()
        db.refresh(db_contact)

    return db_contact


def update_contact(
    db: Session, contact_id: int, contact: schema.ContactUpdate, user_id: int
):
    db_contact = get_contact(db, contact_id=contact_id, user_id=user_id)
    if not db_contact:
        return None

    update_data = contact.model_dump(exclude_unset=True, exclude={"communications"})

    for key, value in update_data.items():
        setattr(db_contact, key, value)

    db_contact.modified = datetime.now(timezone.utc)

    if contact.communications is not None:
        db.query(models.Communication).filter(
            models.Communication.contact_id == contact_id
        ).delete()

        for comm in contact.communications:
            db_comm = models.Communication(
                contact_id=contact_id,
                comm_type=comm.comm_type,
                label=comm.label,
                value=comm.value,
            )
            db.add(db_comm)

    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int, user_id: int):
    db_contact = get_contact(db, contact_id=contact_id, user_id=user_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


def create_contacts_from_vcard(
    db: Session, contacts: List[schema.ContactCreate], user_id: int
):
    created_contacts = []
    try:
        for contact in contacts:
            print(contact)
            now = datetime.now(timezone.utc)
            db_contact = models.Contact(
                first_name=contact.first_name,
                last_name=contact.last_name,
                company=contact.company,
                notes=contact.notes,
                address=contact.address,
                created=now,
                modified=now,
                owner_id=user_id,
            )
            db.add(db_contact)

            if contact.communications:
                for comm in contact.communications:
                    db_comm = models.Communication(
                        contact_id=db_contact.id,
                        comm_type=comm.comm_type,
                        label=comm.label,
                        value=comm.value,
                    )
                    db.add(db_comm)

            created_contacts.append(contact.model_dump())
    except Exception:
        raise RuntimeError("Error creating contacts")

    db.commit()
    db.refresh(db_contact)

    return created_contacts
