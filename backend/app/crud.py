from datetime import datetime, timezone

from app.pydantic_schema import schema
from app.sql_schema import models
from sqlalchemy.orm import Session


def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()


def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contact).offset(skip).limit(limit).all()


def create_contact(db: Session, contact: schema.ContactCreate):
    now = datetime.now(timezone.utc)
    db_contact = models.Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        company=contact.company,
        notes=contact.notes,
        address=contact.address,
        created=now,
        modified=now,
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


def update_contact(db: Session, contact_id: int, contact: schema.ContactUpdate):
    db_contact = get_contact(db, contact_id=contact_id)
    if not db_contact:
        return None

    update_data = contact.model_dump(exclude_unset=True, exclude={"communications"})

    # TODO: Implement update logic for communication
    # Communication will be handled separately. For now it's just a list.

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


def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id=contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact
