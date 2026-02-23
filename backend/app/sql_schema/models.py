from app.database import Base
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship


class Contact(Base):
    """Most basic contact information"""

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    company = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    # Metadata
    modified = Column(DateTime, nullable=True)
    created = Column(DateTime, nullable=True)

    # Either Name, Last Name or Company must be set.
    # Constraint is checked by the database. Advantage if backend makes mistake :)
    __table_args__ = (
        CheckConstraint(
            "first_name IS NOT NULL OR last_name IS NOT NULL OR company IS NOT NULL",
            name="check_contact_has_identifier",
        ),
    )

    address = Column(String, nullable=True)  # TODO: Address should be a separate table

    communications = relationship(
        "Communication", back_populates="contact", cascade="all, delete-orphan"
    )


class Communication(Base):
    """Communication information"""

    __tablename__ = "communications"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"))

    comm_type = Column(String, nullable=False)
    label = Column(String, nullable=True)
    value = Column(String, nullable=False)

    contact = relationship("Contact", back_populates="communications")
