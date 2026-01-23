from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import Field, field_validator, HttpUrl
from app.enums.provinces import Provinces
from app.dtos.baseDTO import BaseDTO

class GetProfileByIdDTO(BaseDTO):
    profile_id: UUID = Field(
        title="Profile ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    )
    
class CreateProfileDTO(BaseDTO):
    nickname: str = Field(
        title="Nickname",
        example="Jenix",
    )
    phone_number: str = Field(
        title="Phone Number",
        example="1234567890",
    )
    dob: date = Field(
        title="Date of Birth",
        example="2000-01-01",
    )
    bio: str | None = Field(
        title="bio",
        examples="profile bio",
        default=None,
    )
    avatar_url: HttpUrl | None = Field(
        title="avatar url",
        examples="https://example.com/avatar.jpg",
        default=None,
    )
    address: str | None = Field(
        title="address",
        examples="123 street a, ward b, city c",
        default=None,
    )
    hometown: Optional[str] | None = Field(
        title="hometown",
        examples="Ho Chi Minh City",
        default=None,
    )
    education: str | None = Field(
        title="education",
        examples="university",
        default=None,
    )
    work: str | None = Field(
        title="work",
        examples="developer",
        default=None,
    )
    hobbies: str | None = Field(
        title="hobbies",
        examples="playing game",
        default=None,
    )
    
    @field_validator("dob")
    @classmethod
    def validate_min_age(cls, value: date):
        today = date.today()
        if value > today:
            raise ValueError("Date of birth cannot be in the future")
        
        age = (today.year - value.year - ((today.month, today.day) < (value.month, value.day)))

        if age < 14:
            raise ValueError("User must be at least 14 years old")
        return value
    
    @field_validator("hometown", mode="before")
    @classmethod
    def validate_hometown(cls, value: str | None):
        if value is None:
            return value
        if value not in Provinces.values:
            raise ValueError("Invalid hometown")
        return value
    
    @field_validator("avatar_url", mode="after")
    @classmethod
    def parse_avatar_url(cls, value):
        if value is None:
            return value
        return str(value)
    
class SearchProfilesDTO(CreateProfileDTO):
    is_active: str | None = Field(
        title="",
        default=None,
        example=""
    )
    page: int = Field(
        title="Current Page",
        ge=1,
        default=1, 
        examples=1
    )
    page_size: int = Field(
        title="Page Size",
        ge=5,
        lt=100,
        default=10, 
        examples=10
    )
    @classmethod
    def is_only_pagination(self):
        pagination_fields = {"page", "page_size", "is_active"}

        for field_name, value in self.model_dump().items():
            if field_name not in pagination_fields and value is not None:
                return False
        return True
    
class GetProfileConversationsDTO(BaseDTO):
    account_id: UUID = Field(
        title="Profile ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    )
    is_active: str | None = Field(
        title="",
        default=None,
        example=""
    )
    page: int = Field(
        title="Current Page",
        ge=1,
        default=1, 
        examples=1
    )
    page_size: int = Field(
        title="Page Size",
        ge=5,
        lt=100,
        default=10, 
        examples=10
    )