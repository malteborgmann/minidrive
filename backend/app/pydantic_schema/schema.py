from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class CommunicationBase(BaseModel):
    comm_type: str
    label: Optional[str] = None
    value: str


class CommunicationCreate(CommunicationBase):
    pass


class Communication(CommunicationBase):
    id: int
    contact_id: int

    model_config = ConfigDict(from_attributes=True)


class ContactBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    notes: Optional[str] = None
    address: Optional[str] = None


class ContactCreate(ContactBase):
    communications: Optional[List[CommunicationCreate]] = []


class ContactUpdate(ContactBase):
    communications: Optional[List[CommunicationCreate]] = []


class ContactResponse(ContactBase):
    id: int
    modified: Optional[datetime] = None
    created: Optional[datetime] = None
    communications: List[Communication] = []

    model_config = ConfigDict(from_attributes=True)
