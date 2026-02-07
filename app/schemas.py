from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# Organization schemas
class OrganizationBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# User schemas
class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    role: Optional[str] = "member"


class UserCreate(UserBase):
    organization_id: Optional[int] = None


class UserResponse(UserBase):
    id: int
    organization_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
